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


def is_there_new_data() -> dict:
    """
    Checks if new modern tournament decklist data has been published from MTGO
    :return:is_new_data :bool,latest_modern_tournament_url:str
    """
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

        # latest_modern_tournament_url = 'https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-league-2020-07-21'
        latest_modern_tournament_url = 'https://magic.wizards.com' + latest_modern_tournament_parent['href']

    data = read_from_file('static/card_data_url.json')
    if data['url'] != latest_modern_tournament_url:
        is_new_data = True

    return {"is_new_data": is_new_data, "latest_modern_tournament_url": latest_modern_tournament_url}


def scrape_card_data() -> dict:
    """
    Using Beautiful soup scrapes card names,types and decklist_ids and saves that information
    in dict format to a local JSON file

    :return:unique_cards:Dict format card data,modern_league_url:str,cards_from:str
    """
    card_data = read_from_file('static/card_data_url.json')
    # latest_card_names = read_from_file('static/latest_card_names.json')
    existing_card_data = card_data['card_set']
    if 'card_set' not in card_data or 'url' not in card_data:
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
                                                           '^sorted-by-(Tribal|Planeswalker|Creature|Sorcery|Land|Enchantment|Artifact|Instant|Sideboard)',
                                                           flags=re.IGNORECASE)})
            # pprint(sorted_by_type)
            card_list = []  # list of dict items
            new_card_name_list = []  # list of dict items

            for sorted_by_type in sorted_by_type:
                # print(sorted_by_type.find('h5').string)
                cards_in_decks = sorted_by_type.findAll('a', attrs={'class': 'deck-list-link'})
                for card_name_div in cards_in_decks:
                    dict_to_add = {}

                    card_deck_list_id = card_name_div.parent.parent.parent.parent.parent.parent.parent.get('id')
                    if not card_deck_list_id:
                        card_deck_list_id = card_name_div.parent.parent.parent.parent.parent.parent.get('id')
                    print(card_deck_list_id)

                    card_type = card_name_div.parent.parent.parent.find('h5').string
                    card_type = card_type[:card_type.index(" (")]
                    card_name = card_name_div.string

                    # print(card_name_div.string + ': ' + card_type)
                    # print(div.string + ': ' + str(is_this_a_basic(div.string)))
                    # if ((any(d['name'] == card_name_div.string for d in card_list)) and (
                    #         not is_this_a_basic(card_name_div.string)) or not card_list):
                    card_name_in_list = []
                    # card_name_in_list = any(card_name in d for d in card_list)

                    # card_name_in_list = any(d.get('name', 'icara') == card_name for d in card_list)

                    if '//' in card_name:

                        print("// in name {} ".format(card_name))

                        split_str = card_name.split('//', 1)

                        for split_card_name in split_str:
                            split_card_name = split_card_name.rstrip().lstrip()
                            in_existing_card_data = any(split_card_name in d for d in existing_card_data)

                            if (not card_name_in_list and not in_existing_card_data and (
                                    not is_this_a_basic(card_name))):
                                # print('// card not in  data')
                                print("// in name {} - not in  existing data".format(split_card_name))

                                dict_to_add = get_single_card_data_from_scryfall(split_card_name)
                                dict_to_add[split_card_name]['type'] = card_type
                                dict_to_add[split_card_name]['decklist_id'] = card_deck_list_id

                                existing_card_data.append(dict_to_add)
                                card_name_in_list.append(card_name)
                                new_card_name_list.append(split_card_name)

                            else:
                                print('// card in existing data')
                                print("// in name {} - in  existing data".format(split_card_name))
                                card_name_in_list.append(card_name)
                                new_card_name_list.append(split_card_name)

                                for card in existing_card_data:
                                    if split_card_name in card.keys():
                                        # existing_card_data[card[split_card_name]['decklist_id']] = card_deck_list_id
                                        index = existing_card_data.index(card)

                                        existing_card_data[index][split_card_name]['decklist_id'] = card_deck_list_id

                                        # card[split_card_name]['decklist_id'] = card_deck_list_id
                                        break

                        # else:
                        #
                        #     new_card_name_list.append(card_name)
                        #     # existing_card_data[card_name]['decklist_id'] = card_deck_list_id
                        #     for card in existing_card_data:
                        #         if card_name in card.keys():
                        #             card[card_name]['decklist_id'] = card_deck_list_id
                        #             break
                    else:
                        print('regular name')

                        in_existing_card_data = any(card_name in d for d in existing_card_data)

                        if (not card_name_in_list and not in_existing_card_data and (
                                not is_this_a_basic(card_name))):

                            # pprint('')
                            print("regular name {} - not in existing card data".format(card_name))

                            # if (card_name_div.string not in card_list) and (not is_this_a_basic(card_name_div.string)):

                            dict_to_add = get_single_card_data_from_scryfall(card_name)
                            # dict_to_add['name'] = card_name_div.string
                            dict_to_add[card_name]['type'] = card_type
                            dict_to_add[card_name]['decklist_id'] = card_deck_list_id

                            existing_card_data.append(dict_to_add)
                            card_name_in_list.append(card_name)
                            new_card_name_list.append(card_name)

                        else:
                            print("regular name {} In data file".format(card_name))
                            card_name_in_list.append(card_name)
                            new_card_name_list.append(card_name)
                            # existing_card_data[card_name]['decklist_id'] = card_deck_list_id
                            for card in existing_card_data:
                                if card_name in card.keys():
                                    # card[card_name]['decklist_id'] = card_deck_list_idndex
                                    index = existing_card_data.index(card)
                                    existing_card_data[index][card_name]['decklist_id'] = card_deck_list_id
                                    break

                        # card_list.append(dict_to_add)

            # https://stackoverflow.com/questions/11092511/python-list-of-unique-dictionaries
            unique_cards = existing_card_data
            # unique_cards = [dict(s) for s in set(frozenset(d.items()) for d in card_list)]

            dict_to_file = {
                # 'url': '',
                'url': modern_league_url,
                "card_set": unique_cards,
            }
            latest_card_names_dict = {
                "card_names": new_card_name_list
            }
            with open('static/card_data_url.json', 'w') as fp:
                json.dump(dict_to_file, fp, sort_keys=True, indent=4)
            with open('static/latest_card_names.json', 'w') as fp:
                json.dump(latest_card_names_dict, fp, sort_keys=True, indent=4)

        else:
            modern_league_url = card_data['url']
            cards_from = 'cards from file'
            unique_cards = card_data['card_set']
            print(cards_from)

    return {
        "modern_league_url": 'https://magic.wizards.com' + modern_league_url,
        "unique_cards": unique_cards,
        "cards_from": cards_from
    }


def replace_card_name_in_oracle(name: str, oracle_text: str) -> str:
    """
    Replaces the name of the card in the oracle text with "This card" and returns it
    :param name: The name of the card
    :param oracle_text: The Oracle text of the card
    :return: oracle_text (str):
    """
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


def is_this_a_basic(potential_basic: str) -> bool:
    """
    Returns True if potential_basic is a name of a basic land
    :param potential_basic:str()
    :return:
    """
    if potential_basic == 'Swamp' or \
            potential_basic == 'Mountain' or \
            potential_basic == 'Island' or \
            potential_basic == 'Plains' or \
            potential_basic == 'Forest' or \
            potential_basic == 'Wastes' or \
            'Snow-Covered' in potential_basic:
        return True
    return False


def replace_symbols_in_text(oracle_text: str) -> str:
    """
    Replaces mana and other special symbols in oracle text with a
    HTML <span> with the corresponding class
    :param oracle_text: str()
    :return: oracle_text
    """
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
        "{X}": "sx",
    }
    for key, value in symbols.items():
        # pprint(key)
        if str(key) in oracle_text:
            oracle_text = oracle_text.replace(str(key), '<span class="mana small align-middle ' + value + '"></span>')

        # oracle_text = oracle_text.replace(key, )

    return oracle_text


def read_from_file(filename: str) -> dict:
    """
    Return JSON data from file as a dict object
    :param filename: str() Path to file
    :return: JSON data
    """
    with open(filename, 'r') as fp:
        data = json.load(fp)
    return data


def get_single_card_data_from_scryfall(card: str) -> dict:
    """
    Fetches Oracle text, Image URL, Flavor text from Scryfall's API
    :param card: str() name of the card we want to return data for
    :return: dict()
    """
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


def get_card_data_from_local_file(card: str) -> dict:
    # random_card_data = {}

    data_api = read_from_file('static/card_data_url.json')
    card_data_scryfall = data_api['card_set']
    # card_data_mtgjson = read_from_file('static/ModernAtomic.json')
    # card_data = json.loads(open("static/ModernAtomic.json", encoding="utf8").read())

    # for card in card:
    # pprint(card)

    card_info = next((item for item in card_data_scryfall if card in item), None)

    # card_name = next((key for key in card_data['data'].keys() if card in key), None)
    # card_name = next(
    #     (key for key in card_data_mtgjson['data'].keys() if
    #      card in [key.rstrip().lstrip() for key in key.split("//") if string_found(card, key)]), None)

    # pprint(card_info)

    # card_data_json = card_data_mtgjson['data'][card_name][0]

    random_card_data = {
        'name': card,
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
    pprint(card_name)
    list_similar_cards = []
    cards = read_from_file('static/ModernAtomic.json')

    local_card_data = read_from_file('static/card_data_url.json')
    existing_card_data = local_card_data['card_set']

    card_info = next(
        (item[card_name]['similar_cards'] for item in existing_card_data if
         card_name in item and 'similar_cards' in item[card_name].keys()),
        None)
    # pprint(card_info)

    if card_info:
        print('card in info')
        return card_info

    all_card_names = cards['data'].keys()

    # card_name = next(
    #     (key for key in cards['data'].keys() if
    #      card_name in [key.rstrip().lstrip() for key in key.split("//") if string_found(card_name, key)]), None)

    card_name_full = ""
    for name in all_card_names:
        if '//' in name:
            if name.split("//")[0].rstrip().lstrip() == card_name:
                card_name_full = name
                break
        elif name == card_name:
            card_name_full = name
            break
    card_name = card_name_full

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
    card_cmc = card_info['convertedManaCost'] if 'convertedManaCost' in card_info else ""

    # card_subtypes.sort()
    # pprint(card_info)

    for current_card_name, current_card_data in cards['data'].items():
        # result = all(elem in card_subtypes for elem in v[0]['subtypes'])
        # if len(list_similar_cards) > 15:
        #     break

        if current_card_name != card_name:
            current_type = current_card_data[0]['types']
            current_subtypes = current_card_data[0]['subtypes']
            current_colors = current_card_data[0]['colors']
            current_identity = current_card_data[0]['colorIdentity']
            current_name = current_card_data[0]['name']
            if '//' in current_name:
                current_name = current_name[:current_name.index("/")]

            # if this_type != 'Land':
            cmc = current_card_data[0]['convertedManaCost'] if 'convertedManaCost' in current_card_data[
                0].keys() else ""
            if current_type != card_type:
                continue
            if is_this_a_basic(current_card_name):
                # pprint(k)
                continue

            if 'Planeswalker' in card_type:
                # if card_type == 'Planeswalker':
                # if not_enough:
                # if len(list_similar_cards)
                if current_subtypes == card_subtypes:
                    # pprint(k)
                    list_similar_cards.append(current_name)

            if 'Land' in card_type and current_card_name not in list_similar_cards:
                if not_enough:
                    if current_identity == card_identity:
                        list_similar_cards.append(current_name)
                else:
                    if (card_subtypes and current_subtypes == card_subtypes) or current_identity == card_identity:
                        list_similar_cards.append(current_name)
            # if 'Land' in card_type:
            #     if not_enough:
            #         if identity == card_identity:
            #             list_similar_cards.append(k)
            #     else:
            #         if identity == card_identity:
            #             list_similar_cards.append(k)

            if 'Creature' in card_type and current_card_name not in list_similar_cards:
                if not_enough:
                    if current_colors == card_colors and cmc == card_cmc:
                        list_similar_cards.append(current_name)
                    elif card_subtypes[0] in current_subtypes and cmc == card_cmc:
                        list_similar_cards.append(current_name)
                    elif card_subtypes[0] in current_subtypes and current_colors == card_colors:
                        list_similar_cards.append(current_name)


                else:
                    if card_subtypes[0] in current_subtypes and current_colors == card_colors and cmc == card_cmc:
                        # if subtypes == card_subtypes and colors == card_colors and cmc == card_cmc:
                        list_similar_cards.append(current_name)

            if 'Sorcery' in card_type or 'Instant' in card_type and current_card_name not in list_similar_cards:
                if not_enough:
                    if current_colors == card_colors and not_enough:
                        list_similar_cards.append(current_name)
                else:
                    if current_colors == card_colors and cmc == card_cmc:
                        list_similar_cards.append(current_name)
                # if colors == card_colors and cmc == card_cmc:
                #     # print(cmc, card_cmc)
                #     list_similar_cards.append(k)
                #     continue
                # elif colors == card_colors and not_enough:
                #     list_similar_cards.append(k)
                # else:
                #     continue

            if 'Artifact' in card_type and current_card_name not in list_similar_cards:
                if current_colors == card_colors and \
                        cmc == card_cmc and \
                        (card_subtypes and current_subtypes == card_subtypes) and not not_enough:
                    list_similar_cards.append(current_name)

                elif cmc == card_cmc and current_colors == card_colors:
                    list_similar_cards.append(current_name)

            if 'Enchantment' in card_type and current_card_name not in list_similar_cards:
                if current_colors == card_colors and current_subtypes == card_subtypes and cmc == card_cmc:
                    list_similar_cards.append(current_name)

            if 'Tribal' in card_type and current_card_name not in list_similar_cards:
                if current_colors == card_colors:
                    list_similar_cards.append(current_name)

    # pprint(list_similar_cards)
    # if len(list_similar_cards) < 5:
    #     similar_cards(card_name, True)
    for card in existing_card_data:
        if card_name in card.keys():
            card[card_name]['similar_cards'] = list_similar_cards
            break

    local_card_data['card_set'] = existing_card_data
    with open('static/card_data_url.json', 'w') as fp:
        json.dump(local_card_data, fp, sort_keys=True, indent=4)

    return list_similar_cards

    # elif colors == card_colors:
    #     # print(subtypes)
    #     list_similar_subtype.add(k)

    # if result:
    #     list_similar_subtype.append(k)
    # print(k, v)


def gen_new_cards(*args):
    data = read_from_file('static/card_data_url.json')
    # data = read_from_file('static/card_data_url.json')
    latest_card_names = read_from_file('static/latest_card_names.json')

    unique_cards = data['card_set']

    list_card_names = latest_card_names['card_names']
    # list_card_names = [list(d.keys())[0] for d in unique_cards]

    # random.shuffle(list_card_names)
    random_card_name = sample(list_card_names, 1)[0]

    # random_card_name = 'Ugin, the Ineffable'
    # random_card_name = 'Klothys, God of Destiny'
    # random_card_name = 'Shefet Dunes'
    # random_card_name = 'Wear'
    random_card_name = 'Sling-Gang Lieutenant'
    # TODO Darksteel Citadel - Artifact land
    # random_card_name = 'Batterskull'
    # random_card_name = 'Merfolk Secretkeeper'
    # random_card_name = 'Grafdigger\'s Cage'

    correct_answer_data = get_card_data_from_local_file(random_card_name)

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

    correct_answer_oracle_text = correct_answer_data['flavor_text'] if not correct_answer_data['oracle_text'] else \
        correct_answer_data['oracle_text']
    correct_answer_decklist_id = correct_answer_data['decklist_id']
    # pprint(correct_answer_oracle_text)
    correct_answer_name = correct_answer_data['name']
    correct_answer_image = correct_answer_data['image']
    # pprint(correct_answer_oracle_text)

    if correct_answer_data['flavor_text']:
        correct_answer_flavor_text = correct_answer_data['flavor_text']
    else:
        correct_answer_flavor_text = correct_answer_data

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


# pprint(get_single_card_data_from_scryfall('Wear'))
# scrape_card_data()

# local_card_data = read_from_file('static/card_data_url.json')
# existing_card_data = local_card_data['card_set']
# for card in existing_card_data:
#     pprint(list(card.keys())[0])
#     pprint(similar_cards(list(card.keys())[0], not_enough=True))
