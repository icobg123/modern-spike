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


# app.config.from_object(os.environ['APP_SETTINGS'])
# await asyncio.sleep(0.1)
# card = scrython.cards.Named(fuzzy="Tear")
#
# card_info = vars(card)


# pprint(card_info)


def is_this_a_basic(potential_basic):
    if potential_basic == 'Swamp' or \
            potential_basic == 'Mountain' or \
            potential_basic == 'Island' or \
            potential_basic == 'Plains' or \
            potential_basic == 'Forest' or \
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
        "{B/R}": "sub",
        "{B/G}": "sur",
        "{U/B}": "sbr",
        "{U/R}": "sbg",
        "{R/G}": "srw",
        "{R/W}": "srg",
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


def get_card_data(random_cards):
    random_card_data = []
    # random_cards = ['Wear', 'Merchant of the Vale', 'Thing in the Ice']

    for card in random_cards:
        print(card)
        card_info = scrython.cards.Named(fuzzy=card)
        card_info = vars(card_info)
        oracle_txt, card_img, flavor_txt = '', '', card

        if 'card_faces' in card_info['scryfallJson']:
            for card_faces in card_info['scryfallJson']['card_faces']:
                oracle_txt = card_faces['oracle_text']
                if "flavor_text" in card_faces:
                    flavor_txt = card_faces['flavor_text']
                if "image_uris" not in card_info['scryfallJson']:
                    card_img = card_faces['image_uris']['art_crop']
                else:
                    card_img = card_info['scryfallJson']['image_uris']['art_crop']

        else:
            oracle_txt = card_info['scryfallJson']['oracle_text']
            card_img = card_info['scryfallJson']['image_uris']['art_crop']
            if "flavor_text" in card_info['scryfallJson']:
                flavor_txt = card_info['scryfallJson']['flavor_text']

        random_card_data.append({
            'name': card,
            'oracle_text': oracle_txt,
            'flavor_text': flavor_txt,
            'image': card_img
        })

    return random_card_data


def gen_new_cards():
    data = read_from_file('old_url.json')

    unique_cards = data['card_set']

    random_cards = sample(unique_cards, 5)
    random_card_data = get_card_data(random_cards)

    correct_answer = random.choice(random_card_data)
    correct_answer_index = random_card_data.index(correct_answer) + 1

    correct_answer_oracle_text = correct_answer['oracle_text']

    if correct_answer['flavor_text']:
        correct_answer_flavor_text = correct_answer['flavor_text']
    else:
        correct_answer_flavor_text = correct_answer

    correct_answer_image = correct_answer['image']

    pprint(correct_answer_oracle_text)

    # new_oracle_text = replace_symbols_in_text(new_oracle_text)
    # new_oracle_text = new_oracle_text.replace()

    list_correct_answer_oracle_text = correct_answer_oracle_text.split('\n')
    to_html_list_correct_answer_oracle_text = ""

    for line in list_correct_answer_oracle_text:
        to_html_list_correct_answer_oracle_text += str(
            '<p class="card-text mb-1">' + replace_symbols_in_text(line) + '</p>')

    card_name = correct_answer['name']
    return {"card_info": random_card_data,
            "correct_answer": correct_answer_index,
            "correct_answer_oracle_text": to_html_list_correct_answer_oracle_text,
            "correct_answer_flavor_text": correct_answer_flavor_text,
            "correct_answer_image": correct_answer_image,
            "name": card_name}


@app.route('/get_new_cards', methods=['POST'])
def get_new_cards():
    asd = 'asd'
    # return jsonify({'error': 'Nope, try again.'})
    new_cards = gen_new_cards()

    correct_answer_index = new_cards['correct_answer']
    correct_answer_oracle_text = new_cards['correct_answer_oracle_text']
    correct_answer_name = new_cards['name']
    correct_answer_image = new_cards['correct_answer_image']

    if new_cards['correct_answer_flavor_text']:
        correct_answer_flavor_text = new_cards['correct_answer_flavor_text']
    else:
        correct_answer_flavor_text = correct_answer_name
    # correct_answer_flavor_text = new_cards['correct_answer_flavor_text']
    correct_answer_oracle_text = correct_answer_oracle_text.replace(correct_answer_name,
                                                                    '<span class="badge badge-secondary align-text-top">This card</span>')

    new_cards = new_cards['card_info']
    return jsonify({
        "html": render_template('cards.html', card_info=new_cards),
        "correct_answer_index": correct_answer_index,
        "correct_answer_name": correct_answer_name,
        "correct_answer_image": correct_answer_image,
        'new_oracle_text': correct_answer_oracle_text,
        'new_flavor_text': correct_answer_flavor_text,
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
        data = read_from_file('old_url.json')
        latest_modern_league_url = data['url']
    else:
        latest_modern_league_parent = latest_modern_league.parent.parent.parent

        latest_modern_league_url = latest_modern_league_parent['href']

    pprint(latest_modern_league_url)

    data = read_from_file('old_url.json')
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

            cards_in_decks = modern_deck_lists.findAll('a', attrs={'class': 'deck-list-link'})

            # print(
            #     ''.join(text for text in cards_in_decks if not is_this_a_basic(text.string)))

            card_set = set()

            for div in cards_in_decks:
                # print(div.string + ': ' + str(is_this_a_basic(div.string)))
                if (div.string not in card_set) and (not is_this_a_basic(div.string)):
                    if '//' in div.string:
                        split_str = div.string.split('//', 1)
                        for correct_answer_name in split_str:
                            card_set.add(correct_answer_name.rstrip().lstrip())

                    else:
                        card_set.add(div.string)

            # new_set = {x.replace('.good', '').replace('.bad', '') for x in card_set}

            unique_cards = list(sorted(card_set))

            dict_to_file = {
                'url': latest_modern_league_url,
                "card_set": unique_cards,
            }
            with open('old_url.json', 'w') as fp:
                json.dump(dict_to_file, fp, sort_keys=True, indent=4)

        else:
            modern_league_url = data['url']
            cards_from = 'cards from file'
            unique_cards = data['card_set']

    # n_cards = int(input())
    # random_cards = sample(unique_cards, n_cards)

    # random_cards = ['Wear', 'Merchant of the Vale']
    random_cards = sample(unique_cards, 5)
    # pprint(random_cards)
    random_card_data = get_card_data(random_cards)

    # pprint(random_card_data)

    correct_answer = random.choice(random_card_data)
    correct_answer_index = random_card_data.index(correct_answer) + 1

    # TODO: Get only oracle text of correct_answer
    correct_answer_name = correct_answer['name']
    correct_answer_image = correct_answer['image']
    correct_oracle_text_answer = correct_answer['oracle_text']
    if correct_answer['flavor_text']:
        correct_answer_flavor_text = correct_answer['flavor_text']
    else:
        correct_answer_flavor_text = correct_answer

    # correct_answer_flavor_text = correct_answer['flavor_text']
    correct_oracle_text_answer = replace_symbols_in_text(correct_oracle_text_answer)

    correct_oracle_text_answer = correct_oracle_text_answer.replace(correct_answer_name,
                                                                    '<span class="badge badge-secondary align-text-top">This card</span>')
    # oracle_text_answer = oracle_text_answer.replace('\n', ' <br/> ')

    # test_new_cards = get_new_cards()

    # pprint('icara')
    # pprint(test_new_cards)

    return render_template("index.html", correct_answer_index=correct_answer_index, correct_answer=correct_answer,
                           card_info=random_card_data,
                           correct_answer_name=correct_answer_name,
                           correct_answer_flavor_text=correct_answer_flavor_text,
                           correct_oracle_text_answer=Markup(correct_oracle_text_answer),
                           correct_answer_image=correct_answer_image,
                           random_cards=random_cards, cards_from=cards_from,
                           modern_league_url='https://magic.wizards.com' + modern_league_url,
                           message="Hello Flask!")


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
