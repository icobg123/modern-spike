import json
from pprint import pprint
from random import choice, sample
import random
import re
import scrython
from bs4 import BeautifulSoup
import requests
from rq import Queue
from worker import conn
# from test import count_words_at_url
from rq import get_current_job
import time


def is_there_new_data():
    is_new_data = False
    url = 'https://magic.wizards.com/en/content/deck-lists-magic-online-products-game-info'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    latest_modern_tournament = soup.find("h3",
                                         text=re.compile('Modern', flags=re.IGNORECASE))
    # text=re.compile('\bModern\s*(League|Challenge|Preliminary)', flags=re.IGNORECASE))
    # print(latest_modern_tournament)

    if latest_modern_tournament is None:
        data = read_from_file('static/card_data_url.json')
        latest_modern_tournament_url = data['url']
    else:
        latest_modern_tournament_parent = latest_modern_tournament.parent.parent.parent

        latest_modern_tournament_url = 'https://magic.wizards.com' + latest_modern_tournament_parent['href']

    data = read_from_file('static/card_data_url.json')
    if data['url'] != latest_modern_tournament_url:
        is_new_data = True

    return {"is_new_data": is_new_data, "latest_modern_tournament_url": latest_modern_tournament_url}


def scrape_card_data():
    data = read_from_file('static/card_data_url.json')

    if 'card_set' not in data or 'url' not in data:
        raise ValueError("No target in given data")
    else:
        is_new_data = is_there_new_data()['is_new_data']
        latest_modern_tournament_url = is_there_new_data()['latest_modern_tournament_url']
        if is_new_data:
            print('update url')
            cards_from = 'cards from URL'
            print(cards_from)

            # get_new_url = True
            modern_league_url_from_file = latest_modern_tournament_url

            modern_league_url = modern_league_url_from_file
            # modern_league_url = 'https://magic.wizards.com' + modern_league_url_from_file
            pprint(modern_league_url)
            response_league = requests.get(modern_league_url)
            modern_deck_lists = BeautifulSoup(response_league.text, 'html.parser')

            sorted_by_type = modern_deck_lists.findAll('div',
                                                       attrs={'class': re.compile(
                                                           '^sorted-by-(Tribal|Planeswalker|Creature|Sorcery|Land|Enchantment|Artifact|Instant)',
                                                           flags=re.IGNORECASE)})
            # pprint(sorted_by_type)
            card_list = []
            for sorted_by_type in sorted_by_type:
                # print(sorted_by_type.find('h5').string)
                cards_in_decks = sorted_by_type.findAll('a', attrs={'class': 'deck-list-link'})
                for card_name_div in cards_in_decks:
                    dict_to_add = {}
                    card_deck_list_id = card_name_div.parent.parent.parent.parent.parent.parent.parent.get('id')
                    print(card_deck_list_id)
                    card_type = card_name_div.parent.parent.parent.find('h5').string
                    card_type = card_type[:card_type.index(" (")]
                    card_name = card_name_div.string

                    # print(card_name_div.string + ': ' + card_type)
                    # print(div.string + ': ' + str(is_this_a_basic(div.string)))
                    # if ((any(d['name'] == card_name_div.string for d in card_list)) and (
                    #         not is_this_a_basic(card_name_div.string)) or not card_list):
                    card_name_in_list = any(card_name in d for d in card_list)
                    # card_name_in_list = any(d.get('name', 'icara') == card_name for d in card_list)
                    if (not card_name_in_list and (
                            not is_this_a_basic(card_name))):
                        # pprint('')
                        print("{} - not in the list of cards".format(card_name))

                        # if (card_name_div.string not in card_list) and (not is_this_a_basic(card_name_div.string)):
                        if '//' in card_name:
                            split_str = card_name.split('//', 1)
                            for split_card_name in split_str:
                                split_card_name = split_card_name.rstrip().lstrip()
                                dict_to_add = get_single_card_data_from_scryfall(split_card_name)
                                dict_to_add[split_card_name]['type'] = card_type
                                dict_to_add[card_name]['decklist_id'] = card_deck_list_id

                                # card_list.append(correct_answer_name.rstrip().lstrip())
                                # dict_to_add['name'] = correct_answer_name

                                card_list.append(dict_to_add)

                        else:
                            dict_to_add = get_single_card_data_from_scryfall(card_name)
                            # dict_to_add['name'] = card_name_div.string
                            dict_to_add[card_name]['type'] = card_type
                            dict_to_add[card_name]['decklist_id'] = card_deck_list_id

                            card_list.append(dict_to_add)

            # https://stackoverflow.com/questions/11092511/python-list-of-unique-dictionaries
            unique_cards = card_list
            # unique_cards = [dict(s) for s in set(frozenset(d.items()) for d in card_list)]

            dict_to_file = {
                # 'url': '',
                'url': modern_league_url,
                "card_set": unique_cards,
            }
            with open('static/card_data_url.json', 'w') as fp:
                json.dump(dict_to_file, fp, sort_keys=True, indent=4)

        else:
            modern_league_url = data['url']
            cards_from = 'cards from file'
            unique_cards = data['card_set']
            print(cards_from)

    return {
        "modern_league_url": 'https://magic.wizards.com' + modern_league_url,
        "unique_cards": unique_cards,
        "cards_from": cards_from
    }


def replace_card_name_in_oracle(name, oracle_text):
    html = '<span class="badge badge-secondary align-text-top">This card</span>'
    names = name.split("//")

    for name in names:
        name = name.rstrip().lstrip()
        if name in oracle_text:
            # pprint('name after comma oracle')

            oracle_text = oracle_text.replace(name, html)

        if ',' in name:
            name_before_comma = name[:name.index(",")]
            if name_before_comma in oracle_text:
                # pprint('name_before_comma in oracle')
                oracle_text = oracle_text.replace(name_before_comma, html)
    oracle_text = oracle_text.replace('−', '<span class="minus">−</span>')
    return oracle_text


def is_this_a_basic(potential_basic):
    if potential_basic == 'Swamp' or \
            potential_basic == 'Mountain' or \
            potential_basic == 'Island' or \
            potential_basic == 'Plains' or \
            potential_basic == 'Forest' or \
            potential_basic == 'Wastes' or \
            'Snow-Covered' in potential_basic:
        return True

    return False


def replace_symbols_in_text(oracle_text):
    symbols = {
        "{T}": "st",
        "{Q}": "sq",
        "{E}": "se",
        "{0}": "s0",
        "{1}": "s1",
        "{2}": "s2",
        "{3}": "s3",
        "{4}": "s4",
        "{5}": "s5",
        "{6}": "s6",
        "{7}": "s7",
        "{8}": "s8",
        "{9}": "s9",
        "{10}": "s10",
        "{11}": "s11",
        "{12}": "s12",
        "{13}": "s13",
        "{14}": "s14",
        "{15}": "s15",
        "{16}": "s16",
        "{17}": "s17",
        "{18}": "s18",
        "{19}": "s19",
        "{20}": "s20",
        "{W/U}": "swu",
        "{W/B}": "swb",
        "{B/R}": "sbr",
        "{B/G}": "sbg",
        "{U/B}": "sub",
        "{U/R}": "sur",
        "{R/G}": "srg",
        "{R/W}": "srw",
        "{G/W}": "sgw",
        "{G/U}": "sgu",
        "{2/W}": "s2w",
        "{2/U}": "s2u",
        "{2/B}": "s2b",
        "{2/R}": "s2r",
        "{2/G}": "s2g",
        "{W/P}": "swp",
        "{U/P}": "sup",
        "{B/P}": "sbp",
        "{R/P}": "srp",
        "{G/P}": "sgp",
        "{W}": "sw",
        "{U}": "su",
        "{B}": "sb",
        "{R}": "sr",
        "{G}": "sg",
        "{C}": "sc",
        "{S}": "ss",
    }
    for key, value in symbols.items():
        # pprint(key)
        if str(key) in oracle_text:
            oracle_text = oracle_text.replace(str(key), '<span class="mana small align-middle ' + value + '"></span>')

        # oracle_text = oracle_text.replace(key, )

    return oracle_text


def read_from_file(filename):
    with open(filename, 'r') as fp:
        data = json.load(fp)
    return data


def get_single_card_data_from_scryfall(card):
    card_info = scrython.cards.Named(fuzzy=card)
    card_info = vars(card_info)
    card_data, card_oracle_txt, card_img, card_flavor_txt = {}, '', '', card

    if 'card_faces' in card_info['scryfallJson']:
        for card_faces in card_info['scryfallJson']['card_faces']:
            if card in card_faces['name']:
                card_oracle_txt = card_faces['oracle_text']
                if "flavor_text" in card_faces:
                    card_flavor_txt = card_faces['flavor_text']
                if "image_uris" not in card_info['scryfallJson']:
                    card_img = card_faces['image_uris']['art_crop']
                else:
                    card_img = card_info['scryfallJson']['image_uris']['art_crop']

    else:
        card_oracle_txt = card_info['scryfallJson']['oracle_text']
        card_img = card_info['scryfallJson']['image_uris']['art_crop']
        if "flavor_text" in card_info['scryfallJson']:
            card_flavor_txt = card_info['scryfallJson']['flavor_text']

    card_data = {
        card: {
            'name': card,
            'oracle_text': card_oracle_txt,
            'flavor_text': card_flavor_txt,
            'image': card_img
        }}

    # pprint(card_data.keys())
    return card_data


def get_card_data_from_file_modern_json(card):
    # random_card_data = {}

    data_api = read_from_file('static/card_data_url.json')
    card_data_scryfall = data_api['card_set']
    card_data_mtgjson = read_from_file('static/ModernAtomic.json')
    # card_data = json.loads(open("static/ModernAtomic.json", encoding="utf8").read())

    # for card in card:
    # pprint(card)

    card_info = next((item for item in card_data_scryfall if card in item), None)
    # card_name = next((key for key in card_data['data'].keys() if card in key), None)
    card_name = next(
        (key for key in card_data_mtgjson['data'].keys() if
         card in [key.rstrip().lstrip() for key in key.split("//") if string_found(card, key)]), None)

    # pprint(card_info)

    card_data_json = card_data_mtgjson['data'][card_name][0]

    random_card_data = {
        'name': card_name,
        'oracle_text': card_info[card]['oracle_text'],
        'flavor_text': card_info[card]['flavor_text'],
        'decklist_id': card_info[card]['decklist_id'],
        'image': card_info[card]['image']
    }

    # pprint(random_card_data)
    return random_card_data


def string_found(string1, string2):
    if re.search(r"\b" + re.escape(string1) + r"\b", string2):
        return True
    return False


def similar_cards(card_name, not_enough=False):
    # TODO: Fix lands same identity and creature identity

    list_similar_cards = []
    cards = read_from_file('static/ModernAtomic.json')

    card_name = next(
        (key for key in cards['data'].keys() if
         card_name in [key.rstrip().lstrip() for key in key.split("//") if string_found(card_name, key)]), None)
    # pprint(card_name)
    #  card_name = next(
    #     (key for key in cards['data'].keys() if card_name in [key.rstrip().lstrip() for key in key.split("//")]), None)
    #
    # # cards = json.loads(open("static/ModernAtomic.json", encoding="utf8").read())

    card_info = cards['data'][card_name][0]
    card_colors = card_info['colors']
    card_type = card_info['types']
    card_subtypes = card_info['subtypes']
    card_identity = card_info['colorIdentity']
    if 'convertedManaCost' in card_info:
        card_cmc = card_info['convertedManaCost']

    card_subtypes.sort()
    # pprint(card_info)

    for k, v in cards['data'].items():
        # result = all(elem in card_subtypes for elem in v[0]['subtypes'])
        if k != card_name:
            this_type = v[0]['types']
            subtypes = v[0]['subtypes']
            colors = v[0]['colors']
            identity = v[0]['colorIdentity']

            subtypes.sort()
            colors.sort()

            # pprint(v[0]['name'])
            if 'convertedManaCost' in v[0].keys():
                # if this_type != 'Land':
                cmc = v[0]['convertedManaCost']
            if this_type != card_type:
                continue
            if is_this_a_basic(k):
                # pprint(k)
                continue

            if 'Planeswalker' in card_type:
                # if card_type == 'Planeswalker':
                # if not_enough:
                # if len(list_similar_cards)
                if subtypes == card_subtypes:
                    # pprint(k)
                    list_similar_cards.append(k)

            if 'Land' in card_type:
                if not_enough:
                    if identity == card_identity:
                        list_similar_cards.append(k)
                else:
                    if (card_subtypes and subtypes == card_subtypes) or identity == card_identity:
                        list_similar_cards.append(k)
            # if 'Land' in card_type:
            #     if not_enough:
            #         if identity == card_identity:
            #             list_similar_cards.append(k)
            #     else:
            #         if identity == card_identity:
            #             list_similar_cards.append(k)

            if 'Creature' in card_type:
                if not_enough:
                    if colors == card_colors and cmc == card_cmc:
                        list_similar_cards.append(k)
                    elif card_subtypes[0] in subtypes and cmc == card_cmc:
                        list_similar_cards.append(k)

                else:
                    if card_subtypes[0] in subtypes and colors == card_colors and cmc == card_cmc:
                        # if subtypes == card_subtypes and colors == card_colors and cmc == card_cmc:
                        list_similar_cards.append(k)

            if 'Sorcery' in card_type or 'Instant' in card_type:
                if not_enough:
                    if colors == card_colors and not_enough:
                        list_similar_cards.append(k)
                else:
                    if colors == card_colors and cmc == card_cmc:
                        list_similar_cards.append(k)
                # if colors == card_colors and cmc == card_cmc:
                #     # print(cmc, card_cmc)
                #     list_similar_cards.append(k)
                #     continue
                # elif colors == card_colors and not_enough:
                #     list_similar_cards.append(k)
                # else:
                #     continue

            if 'Artifact' in card_type:
                if colors == card_colors and cmc == card_cmc and not not_enough:
                    list_similar_cards.append(k)

                elif cmc == card_cmc:
                    list_similar_cards.append(k)

            if 'Enchantment' in card_type:
                if colors == card_colors and subtypes == card_subtypes and cmc == card_cmc:
                    list_similar_cards.append(k)

            if 'Tribal' in card_type:
                if colors == card_colors:
                    list_similar_cards.append(k)

    # pprint(list_similar_cards)
    # if len(list_similar_cards) < 5:
    #     similar_cards(card_name, True)

    return list_similar_cards

    # elif colors == card_colors:
    #     # print(subtypes)
    #     list_similar_subtype.add(k)

    # if result:
    #     list_similar_subtype.append(k)
    # print(k, v)


def gen_new_cards(*args):
    if not args:
        data = read_from_file('static/card_data_url.json')
        unique_cards = data['card_set']
    else:
        unique_cards = args[0]

    list_card_names = [list(d.keys())[0] for d in unique_cards]

    # random.shuffle(list_card_names)

    # random_card_name = 'Ugin, the Ineffable'
    # random_card_name = 'Klothys, God of Destiny'
    # random_card_name = 'Shefet Dunes'
    # random_card_name = 'Sling-Gang Lieutenant'
    # TODO Darksteel Citadel - Artifact land
    # random_card_name = 'Jace, the Mind Sculptor'
    random_card_name = sample(list_card_names, 1)[0]

    correct_answer = get_card_data_from_file_modern_json(random_card_name)

    list_card_names_with_same_type = similar_cards(random_card_name)
    # random_card_type = [d[random_card_name]['type'] for d in unique_cards if
    #                     random_card_name in list(d.keys())[0]][0]
    #
    # list_card_names_with_same_type = [list(d.keys())[0] for d in unique_cards if
    #                                   random_card_type in d[list(d.keys())[0]]['type']]
    #
    #
    sample_size = len(list_card_names_with_same_type)

    # list_card_names_with_same_type.remove(random_card_name)
    if sample_size < 4:
        list_card_names_with_same_type = similar_cards(random_card_name, True)
        # print(len(list_card_names_with_same_type))
        sample_size = len(list_card_names_with_same_type)
        if sample_size < 4:
            sample_size = len(list_card_names_with_same_type)
        else:
            sample_size = 4
    else:
        sample_size = 4
    # TODO: fix for less than 4 of card type?

    random_cards_name_same_type = sample(list_card_names_with_same_type, sample_size)

    random_cards_name_same_type.append(random_card_name)

    # pprint(random_cards_name_same_type)

    random.shuffle(random_cards_name_same_type)
    # pprint(random_cards_name_same_type)
    # random_cards = sample(list_card_name, 5)

    # Test special Cards
    # random_card_data = ['Vexing Shusher']
    # random_card_data = ['Seal of Fire', 'Shark Typhoon']
    # random_card_data = ['Bonecrusher Giant','Stomp']
    # random_card_data = ['Wear', 'Merchant of the Vale']
    # random_card_data = ['Urza, Lord High Artificer']
    # random_card_data = ['Brimaz, King of Oreskos', 'Keranos, God of Storms']
    # random_card_data = get_card_data(random_card_data)

    # random_card_data = get_card_data_from_file(random_cards_name_same_type)

    # random_card_data = get_card_data(random_card_name)
    # random_card_data = get_card_data(random_cards)

    # correct_answer = random.choice(random_card_data)
    correct_answer_index = random_cards_name_same_type.index(random_card_name) + 1

    correct_answer_oracle_text = correct_answer['oracle_text']
    correct_answer_decklist_id = correct_answer['decklist_id']
    # pprint(correct_answer_oracle_text)
    correct_answer_name = correct_answer['name']
    correct_answer_image = correct_answer['image']
    # pprint(correct_answer_oracle_text)

    if correct_answer['flavor_text']:
        correct_answer_flavor_text = correct_answer['flavor_text']
    else:
        correct_answer_flavor_text = correct_answer

    # new_oracle_text = replace_symbols_in_text(new_oracle_text)
    # new_oracle_text = new_oracle_text.replace()

    correct_answer_oracle_text = replace_card_name_in_oracle(correct_answer_name, correct_answer_oracle_text)

    list_correct_answer_oracle_text = correct_answer_oracle_text.split('\n')
    to_html_list_correct_answer_oracle_text = ""

    for line in list_correct_answer_oracle_text:
        to_html_list_correct_answer_oracle_text += str(
            '<p class="card-text mb-1">' + replace_symbols_in_text(line) + '</p>')

    return {"card_info": random_cards_name_same_type,
            "correct_answer_index": correct_answer_index,
            "correct_answer_oracle_text": to_html_list_correct_answer_oracle_text,
            "correct_answer_flavor_text": correct_answer_flavor_text,
            "correct_answer_decklist_id": correct_answer_decklist_id,
            "correct_answer_image": correct_answer_image,
            "correct_answer_name": correct_answer_name}


def count_words_at_url(seconds):
    job = get_current_job()
    print('Starting task')
    for i in range(seconds):
        job.meta['progress'] = 100.0 * i / seconds
        job.save_meta()
        print(i)
        time.sleep(1)
    job.meta['progress'] = 100
    job.save_meta()
    print('Task completed')
    return {"result": "mn sum lud"}