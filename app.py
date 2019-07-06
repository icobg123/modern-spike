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
from flask import Flask, render_template

app = Flask(__name__)

# app.config.from_object(os.environ['APP_SETTINGS'])
# await asyncio.sleep(0.1)
card = scrython.cards.Named(fuzzy="Black Lotus")
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


@app.route("/")
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
        # cards = vars(card_info)
        # for key in cards['scryfallJson']['data']:
        #     card_vars = key

        # pprint(card_info['scryfallJson']['oracle_text'])
        # oracle_text[card] = card_info
        # dict_to_append[index] = {
        #     'name': card,
        #     'oracle_text': card_info['scryfallJson']['oracle_text']
        # }

        oracle_text.append({
            'name': card,
            'oracle_text': card_info['scryfallJson']['oracle_text'],
            'image': card_info['scryfallJson']['image_uris']['art_crop']
        })

        # oracle_text.append({str(index): {
        #     'name': card,
        #     'oracle_text': card_info['scryfallJson']['oracle_text']
        # }})

        card_index = card_index + 1

    correct_answer = random.choice(oracle_text)
    correct_answer_index = oracle_text.index(correct_answer)
    # TODO: Get only oracle text of correct_answer
    card_name = correct_answer['name']
    oracle_text_answer = correct_answer['oracle_text']
    oracle_text_answer = oracle_text_answer.replace(card_name, '~')

    return render_template("index.html", correct_answer_index=correct_answer_index, correct_answer=correct_answer,
                           card_info=oracle_text,
                           oracle_text_answer=oracle_text_answer,
                           random_cards=random_cards, cards_from=cards_from,
                           message="Hello Flask!")


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run(debug=True)
