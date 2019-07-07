import requests
import urllib.request
import time
import json
from pprint import pprint
from bs4 import BeautifulSoup
from random import choice, sample
import random
import scrython

import asyncio
# from flask_bs4 import Bootstrap

import os
from flask import Flask, render_template, request, jsonify, Markup

app = Flask(__name__)

# app.config.from_object(os.environ['APP_SETTINGS'])
# await asyncio.sleep(0.1)
card = scrython.cards.Named(fuzzy="Tear")

card_info = vars(card)

pprint(card_info)


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


def get_card_info():
    with open('old_url.json', 'r') as fp:
        data = json.load(fp)
        unique_cards = data['card_set']

    random_cards = sample(unique_cards, 5)
    oracle_text = []

    for card in random_cards:
        print(card)
        card_info = scrython.cards.Named(fuzzy=card)
        card_info = vars(card_info)

        if 'card_faces' in card_info['scryfallJson'] and 'image_uris' not in card_info['scryfallJson']:
            oracle_txt = card_info['scryfallJson']['card_faces'][0]['oracle_text']
            card_img = card_info['scryfallJson']['card_faces'][0]['image_uris']['art_crop']

        else:
            oracle_txt = card_info['scryfallJson']['oracle_text']
            card_img = card_info['scryfallJson']['image_uris']['art_crop']

        oracle_text.append({
            'name': card,
            'oracle_text': oracle_txt,
            'image': card_img
        })

    correct_answer = random.choice(oracle_text)
    correct_answer_index = oracle_text.index(correct_answer) + 1
    new_oracle_text = correct_answer['oracle_text']

    # new_oracle_text = replace_symbols_in_text(new_oracle_text)
    # new_oracle_text = new_oracle_text.replace()

    list_of_new_text = new_oracle_text.split('\n')
    to_html = ""
    for p in list_of_new_text:
        # to_html =   '<p class="card-text">' + p + '</p>'

        to_html += str('<p class="card-text mb-1">' + replace_symbols_in_text(p) + '</p>')

    card_name = correct_answer['name']
    return {"card_info": oracle_text, "correct_answer": correct_answer_index, "new_oracle_text": to_html,
            "name": card_name}


@app.route('/get_new_cards', methods=['POST'])
def get_new_cards():
    asd = 'asd'
    # return jsonify({'error': 'Nope, try again.'})
    card_info = get_card_info()
    correct_answ = card_info['correct_answer']
    new_oracle_text = card_info['new_oracle_text']
    card_name = card_info['name']
    new_oracle_text = new_oracle_text.replace(card_name,
                                              '<span class="badge badge-secondary align-text-top">This card</span>')

    card_info = card_info['card_info']
    return jsonify(
        {"html": render_template('cards.html', card_info=card_info), "correct_answ": correct_answ,
         'new_oracle_text': new_oracle_text})
    # return jsonify({'card_set': get_random_cards()})


@app.route('/process', methods=['POST'])
def process():
    choice = request.form['choice']

    correct_answer = request.form['correct_answer']
    print(choice)
    print(correct_answer)
    if choice == correct_answer:
        return jsonify({'choice': 'Well done!'})

    return jsonify({'error': 'Nope, try again.'})


@app.route("/", methods=['GET', 'POST'])
def index():
    url = 'https://magic.wizards.com/en/content/deck-lists-magic-online-products-game-info'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    latest_modern_league = soup.find("h3", text="Modern League").parent.parent.parent
    latest_modern_league_url = latest_modern_league['href']

    url_to_file = {}
    pprint(latest_modern_league_url)

    with open('old_url.json', 'r') as fp:
        data = json.load(fp)
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
                            for card_name in split_str:
                                card_set.add(card_name)

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
                # modern_league_url_from_file = data['url']
                cards_from = 'cards from file'
                unique_cards = data['card_set']

    # n_cards = int(input())
    # random_cards = sample(unique_cards, n_cards)
    random_cards = sample(unique_cards, 5)

    oracle_text = []
    # oracle_text = {}
    dict_to_append = {}

    card_index = 0
    for card in random_cards:
        print(card)
        card_info = scrython.cards.Named(fuzzy=card)
        card_info = vars(card_info)
        if 'card_faces' in card_info['scryfallJson']:
            oracle_txt = card_info['scryfallJson']['card_faces'][0]['oracle_text']
            card_img = card_info['scryfallJson']['card_faces'][0]['image_uris']['art_crop']

        else:
            oracle_txt = card_info['scryfallJson']['oracle_text']
            card_img = card_info['scryfallJson']['image_uris']['art_crop']

        oracle_text.append({
            'name': card,
            'oracle_text': oracle_txt,
            'image': card_img

        })

        # oracle_text.append({str(index): {
        #     'name': card,
        #     'oracle_text': card_info['scryfallJson']['oracle_text']
        # }})

        card_index = card_index + 1

    correct_answer = random.choice(oracle_text)
    correct_answer_index = oracle_text.index(correct_answer) + 1
    # TODO: Get only oracle text of correct_answer
    card_name = correct_answer['name']
    oracle_text_answer = correct_answer['oracle_text']
    oracle_text_answer = replace_symbols_in_text(oracle_text_answer)

    oracle_text_answer = oracle_text_answer.replace(card_name,
                                                    '<span class="badge badge-secondary align-text-top">This card</span>')
    # oracle_text_answer = oracle_text_answer.replace('\n', ' <br/> ')

    return render_template("index.html", correct_answer_index=correct_answer_index, correct_answer=correct_answer,
                           card_info=oracle_text,
                           oracle_text_answer=Markup(oracle_text_answer),
                           random_cards=random_cards, cards_from=cards_from,
                           message="Hello Flask!")


if __name__ == '__main__':
    app.run(debug=True)
