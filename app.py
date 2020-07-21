import requests
import urllib.request
import time
import json
from pprint import pprint
from bs4 import BeautifulSoup
from random import choice, sample
import random
import re
import scrython
from flask_sslify import SSLify

import asyncio
# from flask_bs4 import Bootstrap

import os
from flask import Flask, render_template, request, jsonify, Markup, request, make_response

app = Flask(__name__)
sslify = SSLify(app)


# TODO implement same card type / similar effect


# app.config.from_object(os.environ['APP_SETTINGS'])
# await asyncio.sleep(0.1)
# card = scrython.cards.Named(fuzzy="Tear")
#
# card_info = vars(card)


# pprint(card_info)

def replace_card_name_in_oracle(name, oracle_text):
    html = '<span class="badge badge-secondary align-text-top">This card</span>'
    names = name.split("//")

    for name in names:
        name = name.rstrip().lstrip()
        if name in oracle_text:
            pprint('name after comma oracle')

            oracle_text = oracle_text.replace(name, html)

        if ',' in name:
            name_before_comma = name[:name.index(",")]
            if name_before_comma in oracle_text:
                pprint('name_before_comma in oracle')
                oracle_text = oracle_text.replace(name_before_comma, html)

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


def is_card_type(potential_card_type):
    if 'Planeswalker' in potential_card_type or \
            'Creature' in potential_card_type or \
            'Sorcery' in potential_card_type or \
            'Land' in potential_card_type or \
            'Enchantment' in potential_card_type or \
            'Artifact' in potential_card_type or \
            'Tribal' in potential_card_type:
        return True
    return False

    # if potential_card_type == 'Planeswalker' or \
    #         potential_card_type == 'Creature' or \
    #         potential_card_type == 'Sorcery' or \
    #         potential_card_type == 'Plains' or \
    #         potential_card_type == 'Instant' or \
    #         potential_card_type == 'Land' or \
    #         'Snow-Covered' in potential_card_type:
    #     return True
    #
    # return False


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


# print('icara' + replace_symbols_in_text('{T}'))


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

    pprint(card_data.keys())
    return card_data


def get_card_data_from_file_modern_json(card):
    # random_card_data = {}

    image_data = read_from_file('static/card_data_url.json')
    card_images = image_data['card_set']
    card_data = read_from_file('static/ModernAtomic.json')
    # card_data = json.loads(open("static/ModernAtomic.json", encoding="utf8").read())

    # for card in card:
    pprint(card)

    card_info = next((item for item in card_images if card in item), None)
    # card_name = next((key for key in card_data['data'].keys() if card in key), None)
    card_name = next(
        (key for key in card_data['data'].keys() if
         card in [key.rstrip().lstrip() for key in key.split("//") if string_found(card, key)]), None)

    pprint(card_info)

    card_data_json = card_data['data'][card_name][0]

    random_card_data = {
        'name': card_name,
        'oracle_text': card_data_json['text'],
        'flavor_text': card_name,
        'image': card_info[card]['image']
    }

    # pprint(random_card_data)
    return random_card_data


def get_card_data_from_file(random_cards):
    random_card_data = []
    # random_cards = ['Wear', 'Merchant of the Vale', 'Thing in the Ice']
    data = read_from_file('static/card_data_url.json')
    unique_cards = data['card_set']
    for card in random_cards:
        pprint(card)

        card_info = next((item for item in unique_cards if card in item), None)

        pprint(card_info)

        random_card_data.append({
            'name': card,
            'oracle_text': card_info[card]['oracle_text'],
            'flavor_text': card_info[card]['flavor_text'],
            'image': card_info[card]['image']
        })

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
    pprint(card_name)
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
                pprint(k)
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

    pprint(list_similar_cards)
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
        print(len(list_card_names_with_same_type))
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

    pprint(random_cards_name_same_type)

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
    pprint(correct_answer_oracle_text)
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
            "correct_answer_image": correct_answer_image,
            "correct_answer_name": correct_answer_name}


@app.route('/get_new_cards', methods=['POST'])
def get_new_cards():
    asd = 'asd'

    new_cards = gen_new_cards()

    return jsonify({
        "html": render_template('cards.html', card_info=new_cards['card_info']),
        "correct_answer_index": new_cards['correct_answer_index'],
        "correct_answer_name": new_cards['correct_answer_name'],
        "correct_answer_image": new_cards['correct_answer_image'],
        'new_oracle_text': new_cards['correct_answer_oracle_text'],
        'new_flavor_text': new_cards['correct_answer_flavor_text'],
    })
    # return jsonify({'card_set': get_random_cards()})


@app.route('/cookie', methods=['POST'])
def cookie():
    res = ''

    current_score = int(request.form['current_score'])
    total_score = int(request.form['total_score'])

    user_choice = request.form['choice']
    correct_answer = request.form['correct_answer']

    if user_choice == correct_answer:
        if not request.cookies.get('current_score') and not request.cookies.get('total_score'):
            current_score = 1
            total_score = 1
            res = make_response(jsonify({'current_score': current_score,
                                         'total_score': total_score, }))
            res.set_cookie('current_score', str(current_score), max_age=60 * 60 * 24 * 365 * 2)
            res.set_cookie('total_score', str(total_score), max_age=60 * 60 * 24 * 365 * 2)
        else:

            current_score = current_score + 1
            total_score = total_score + 1
            # pprint(current_score)

            res = make_response(jsonify({'current_score': current_score,
                                         'total_score': total_score, }))
            res.set_cookie('current_score', str(current_score), max_age=60 * 60 * 24 * 365 * 2)
            res.set_cookie('total_score', str(total_score), max_age=60 * 60 * 24 * 365 * 2)
    else:
        total_score = total_score + 1
        res = make_response(jsonify({'total_score': total_score, }))
        res.set_cookie('total_score', str(total_score), max_age=60 * 60 * 24 * 365 * 2)

    # res = make_response("Value of cookie score is {}".format(request.cookies.get('score')))

    return res


@app.route('/process', methods=['POST'])
def process():
    user_choice = request.form['choice']

    correct_answer = request.form['correct_answer']
    # print(user_choice)
    # print(correct_answer)
    if user_choice == correct_answer:
        return jsonify({'choice': 'Well done!'})

    return jsonify({'error': 'Nope, try again.'})


@app.route('/sw.js')
def sw():
    return app.send_static_file('sw.js')


@app.route('/offline.html')
def offline():
    return app.send_static_file('offline.html')


@app.route("/", methods=['GET', 'POST'])
def index():
    url = 'https://magic.wizards.com/en/content/deck-lists-magic-online-products-game-info'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    latest_modern_league = soup.find("h3",
                                     text=re.compile('Modern', flags=re.IGNORECASE))
    # text=re.compile('\bModern\s*(League|Challenge|Preliminary)', flags=re.IGNORECASE))
    print(latest_modern_league)
    if latest_modern_league is None:
        data = read_from_file('static/card_data_url.json')
        latest_modern_league_url = data['url']
    else:
        latest_modern_league_parent = latest_modern_league.parent.parent.parent

        latest_modern_league_url = latest_modern_league_parent['href']

    pprint(latest_modern_league_url)

    data = read_from_file('static/card_data_url.json')
    if 'card_set' not in data or 'url' not in data:
        raise ValueError("No target in given data")
    else:
        if data['url'] != latest_modern_league_url:
            print('update url')
            cards_from = 'cards from URL'

            # get_new_url = True
            modern_league_url_from_file = latest_modern_league_url

            modern_league_url = 'https://magic.wizards.com' + modern_league_url_from_file

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
                        pprint('not in the list of cards')
                        # if (card_name_div.string not in card_list) and (not is_this_a_basic(card_name_div.string)):
                        if '//' in card_name:
                            split_str = card_name.split('//', 1)
                            for correct_answer_name in split_str:
                                correct_answer_name = correct_answer_name.rstrip().lstrip()
                                dict_to_add = get_single_card_data_from_scryfall(correct_answer_name)
                                dict_to_add[correct_answer_name]['type'] = card_type
                                # card_list.append(correct_answer_name.rstrip().lstrip())
                                # dict_to_add['name'] = correct_answer_name

                                card_list.append(dict_to_add)

                        else:
                            dict_to_add = get_single_card_data_from_scryfall(card_name)
                            # dict_to_add['name'] = card_name_div.string
                            dict_to_add[card_name]['type'] = card_type

                            card_list.append(dict_to_add)

            # https://stackoverflow.com/questions/11092511/python-list-of-unique-dictionaries
            unique_cards = card_list
            # unique_cards = [dict(s) for s in set(frozenset(d.items()) for d in card_list)]

            dict_to_file = {
                # 'url': '',
                'url': latest_modern_league_url,
                "card_set": unique_cards,
            }
            with open('static/card_data_url.json', 'w') as fp:
                json.dump(dict_to_file, fp, sort_keys=True, indent=4)

        else:
            modern_league_url = data['url']
            cards_from = 'cards from file'
            unique_cards = data['card_set']

    new_cards = gen_new_cards(unique_cards)

    return render_template("index.html", correct_answer_index=new_cards['correct_answer_index'],
                           card_info=new_cards['card_info'],
                           correct_answer_name=new_cards['correct_answer_name'],
                           correct_answer_flavor_text=new_cards['correct_answer_flavor_text'],
                           correct_oracle_text_answer=Markup(new_cards['correct_answer_oracle_text']),
                           correct_answer_image=new_cards['correct_answer_image'],
                           cards_from=cards_from,
                           modern_league_url='https://magic.wizards.com' + modern_league_url,
                           message="Hello Flask!")


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
