import base64
import json
from pprint import pprint
from random import choice, sample
import random
import re
from PIL import Image
from io import BytesIO

import scrython
from bs4 import BeautifulSoup
import requests
import datetime as DT
from rq import Queue
from worker import conn
# from test import count_words_at_url
from rq import get_current_job
import time
import os
from pymongo import UpdateOne
# from flask import current_app as app
from app import mongo


# from db import mongo


# DB_URI = os.environ['DB_URI']
# print(DB_URI)

def is_there_new_data() -> dict:
    """
    Checks if new modern tournament decklist data has been published from MTGO
    :return:is_new_data :bool,latest_modern_tournament_url:str
    """
    url_data = read_from_file('static/card_data_url.json')

    urls_doc_from_db = mongo.db.urls.find_one({"_id": "decklists_urls"})
    # pprint(urls_doc_from_db)
    urls_from_db = urls_doc_from_db['urls']

    today = DT.date.today()
    week_ago = today - DT.timedelta(days=7)
    # d = DT.datetime.strptime(today, '%Y-%m-%d')
    today = DT.date.strftime(today, "%m/%d/%Y")
    week_ago = DT.date.strftime(week_ago, "%m/%d/%Y")
    # print(today, week_ago)
    is_new_data = False
    url = 'https://magic.wizards.com/en/section-articles-see-more-ajax?dateoff=&l=en&f=9041&search-result-theme=&limit=30&fromDate=' + week_ago + '&toDate=' + today + '&sort=ASC&word=modern&offset=0'
    # url = 'https://magic.wizards.com/en/content/deck-lists-magic-online-products-game-info'
    # pprint(url)
    response = requests.get(url)
    json_data = response.json()
    # for url in  response['data']
    response_html = json_data['data']
    response_html.reverse()
    # pprint(response_html)
    soup = BeautifulSoup('"""' + ''.join(response_html) + '"""', 'html.parser')
    # soup = BeautifulSoup(response_html, 'html.parser')
    # print(soup)
    tournament_urls = []
    latest_modern_tournament = soup.findAll("a")
    # pprint(latest_modern_tournament)
    for a in latest_modern_tournament:
        # pprint(a['href'])

        if "League" not in a.text:
            tournament_urls.append('https://magic.wizards.com' + a['href'])
    # text=re.compile('\bModern\s*(League|Challenge|Preliminary)', flags=re.IGNORECASE))
    # print(latest_modern_tournament)

    if latest_modern_tournament is None:

        latest_modern_tournament_urls = urls_from_db
    elif tournament_urls:
        # latest_modern_tournament_parent = latest_modern_tournament.parent.parent.parent
        latest_modern_tournament_urls = tournament_urls
        #
        # latest_modern_tournament_url = 'https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-league-2020-07-21'
        # latest_modern_tournament_url = 'https://magic.wizards.com' + latest_modern_tournament_parent['href']
        #
        # data = read_from_file('static/card_data_url.json')
        set_data_url = set(urls_from_db)
        set_latest_modern_tournament_urls = set(latest_modern_tournament_urls)
        # pprint(set_data_url)
        # pprint(set_latest_modern_tournament_urls)
        if set_data_url != set_latest_modern_tournament_urls:
            # if data['url'] != latest_modern_tournament_urls:
            is_new_data = True
        # return tournament_urls
    else:
        latest_modern_tournament_urls = urls_from_db

    # return {"is_new_data": True, "latest_modern_tournament_urls": latest_modern_tournament_urls}
    return {"is_new_data": is_new_data, "latest_modern_tournament_urls": latest_modern_tournament_urls}


def scrape_card_data() -> dict:
    """
    Using Beautiful soup scrapes card names,types and decklist_ids and saves that information
    in dict format to a local JSON file

    :return:unique_cards:Dict format card data,modern_league_url:str,cards_from:str
    """
    card_data = read_from_file('static/card_data_url.json')
    # card_names_data = read_from_file('static/latest_card_names.json')
    # latest_card_names = read_from_file('static/latest_card_names.json')
    # existing_card_data = card_data['card_set']
    existing_card_data = []
    urls_to_add = []
    card_names_to_add = []

    cards = mongo.db.cards
    urls = mongo.db.urls
    list_card_names_db = mongo.db.list_card_names
    card_ids = cards.find().distinct('_id')

    # existing_urls = card_data['url']

    is_there_new_data_data = is_there_new_data()
    # is_new_data = True
    is_new_data = is_there_new_data_data['is_new_data']
    # latest_modern_tournament_urls = [
    #     'https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-preliminary-2020-08-08']
    latest_modern_tournament_urls = is_there_new_data_data['latest_modern_tournament_urls']
    if is_new_data:
        print('update urls')
        cards_from = 'cards from URL'
        print(cards_from)

        # get_new_url = True
        # card_data_json = open('static/card_data_url.json', 'w')
        #
        # card_names_list = open('static/latest_card_names.json', 'w')
        card_list = []  # list of dict items

        for url in latest_modern_tournament_urls[::-1]:
            # if url not in existing_urls:
            modern_league_url_from_file = url

            modern_league_url = modern_league_url_from_file
            # modern_league_url = 'https://magic.wizards.com' + modern_league_url_from_file
            # pprint(modern_league_url)
            response_league = requests.get(modern_league_url)
            modern_deck_lists = BeautifulSoup(response_league.text, 'html.parser')

            sorted_by_type = modern_deck_lists.findAll('div',
                                                       attrs={'class': re.compile(
                                                           '^sorted-by-(Tribal|Planeswalker|Creature|Sorcery|Land|Enchantment|Artifact|Instant|Sideboard)',
                                                           flags=re.IGNORECASE)})
            # pprint(sorted_by_type)

            new_card_name_list = set()  # list of dict items
            # card_name_in_list = bool

            for sorted_by_type in sorted_by_type:
                # print(sorted_by_type.find('h5').string)
                cards_in_decks = sorted_by_type.findAll('a', attrs={'class': 'deck-list-link'})
                for card_name_div in cards_in_decks:

                    dict_to_add = {}

                    card_deck_list_id = card_name_div.parent.parent.parent.parent.parent.parent.parent.get('id')
                    if not card_deck_list_id:
                        card_deck_list_id = card_name_div.parent.parent.parent.parent.parent.parent.get('id')
                    # print(card_deck_list_id)

                    card_type = card_name_div.parent.parent.parent.find('h5').string
                    # card_type = card_type[:card_type.index(" (")]
                    card_name = card_name_div.string
                    # if "Snapcaster Mage" in card_name:
                    # print(card_name_div.string + ': ' + card_type)
                    # print(div.string + ': ' + str(is_this_a_basic(div.string)))
                    # if ((any(d['name'] == card_name_div.string for d in card_list)) and (
                    #         not is_this_a_basic(card_name_div.string)) or not card_list):
                    card_name_in_list = any(card_name in d for d in card_list)
                    card_list.append(card_name)
                    # pprint(card_list)
                    print(card_name, card_name_in_list)

                    # card_name_in_list = any(d.get('name', 'icara') == card_name for d in card_list)
                    if '//' in card_name:

                        # print("// in name {} ".format(card_name))

                        split_str = card_name.split('//', 1)

                        for split_card_name in split_str:
                            split_card_name = split_card_name.rstrip().lstrip()

                            # in_existing_card_data = mongo.db.cards.count_documents({'_id': split_card_name}, limit=1)
                            if "Tear" in split_card_name:
                                in_existing_card_data = True if cards.count_documents({'_id': "Tear"},
                                                                                      limit=1) else False

                                try:
                                    pprint(cards.find_one({'_id': "Tear"})['_id'])
                                except TypeError:
                                    print("nema takoa jivotno")
                            else:
                                in_existing_card_data = True if cards.count_documents({'_id': split_card_name},
                                                                                      limit=1) else False
                                # in_existing_card_data = False

                            # in_existing_card_data = any(split_card_name in d for d in card_ids)

                            if (not card_name_in_list and not in_existing_card_data and (
                                    not is_this_a_basic(card_name))):
                                # print('// card not in  data')
                                print("// in name {} - not in  existing data".format(split_card_name))

                                dict_to_add = get_single_card_data_from_scryfall(split_card_name)
                                # dict_to_add[split_card_name]['type'] = card_type
                                dict_to_add['decklist_id'] = url + "#" + card_deck_list_id
                                # dict_to_add[split_card_name]['decklist_id'] = url + "#" + card_deck_list_id
                                existing_card_data.append(dict_to_add)

                                # existing_card_data.append(dict_to_add)
                                new_card_name_list.add(split_card_name)

                            else:
                                # print('// card in existing data')
                                print("// in name {} - in  existing data".format(split_card_name))
                                # card_name_in_list.append(card_name)
                                new_card_name_list.add(split_card_name)

                                # update_existing_decklist_url_in_db = cards.update_one({"_id": split_card_name},
                                #                                                       {"$set": {
                                #                                                           "decklist_id": url + "#" + card_deck_list_id}},
                                #                                                       upsert=True)

                                # for card in existing_card_data:
                                #     # pprint(card)
                                #     if split_card_name in card.keys():
                                #         # existing_card_data[card[split_card_name]['decklist_id']] = card_deck_list_id
                                #         index = existing_card_data.index(card)
                                #         existing_card_data[index][split_card_name][
                                #             'decklist_id'] = url + "#" + card_deck_list_id
                                #         # card[split_card_name]['decklist_id'] = card_deck_list_id
                                #         break

                        # else:
                        #
                        #     new_card_name_list.append(card_name)
                        #     # existing_card_data[card_name]['decklist_id'] = card_deck_list_id
                        #     for card in existing_card_data:
                        #         if card_name in card.keys():
                        #             card[card_name]['decklist_id'] = card_deck_list_id
                        #             break
                    else:
                        # print('regular name')

                        # in_existing_card_data = mongo.db.cards.count_documents({'_id': card_name}, limit=1)
                        # in_existing_card_data = any(card_name in d for d in card_ids)

                        in_existing_card_data = True if cards.count_documents({'_id': card_name},
                                                                              limit=1) else False
                        # in_existing_card_data = False
                        if not is_this_a_basic(card_name):
                            if not card_name_in_list and not in_existing_card_data:

                                # pprint('')
                                print("regular name {} - not in existing card data".format(card_name))

                                # if (card_name_div.string not in card_list) and (not is_this_a_basic(card_name_div.string)):

                                dict_to_add = get_single_card_data_from_scryfall(card_name)
                                # pprint(dict_to_add)

                                # dict_to_add['name'] = card_name_div.string

                                dict_to_add['decklist_id'] = url + "#" + card_deck_list_id
                                # dict_to_add[card_name]['decklist_id'] = url + "#" + card_deck_list_id
                                existing_card_data.append(dict_to_add)

                                # existing_card_data.append(dict_to_add)
                                card_list.append(card_name)
                                new_card_name_list.add(card_name)

                            else:
                                print("regular name {} In data file".format(card_name))
                                # card_name_in_list.append(card_name)
                                new_card_name_list.add(card_name)
                                # existing_card_data[card_name]['decklist_id'] = card_deck_list_id

                                update_existing_decklist_url_in_db = cards.update_one({"_id": card_name},
                                                                                      {"$set": {
                                                                                          "decklist_id": url + "#" + card_deck_list_id}},
                                                                                      upsert=True)

                                # for card in existing_card_data:
                                #     if card_name in card.keys():
                                #         # card[card_name]['decklist_id'] = card_deck_list_idndex
                                #         index = existing_card_data.index(card)
                                #         existing_card_data[index][card_name][
                                #             'decklist_id'] = url + "#" + card_deck_list_id
                                #         break
                        # if dict_to_add:

                # card_list.append(dict_to_add)
            # unique_cards = existing_card_data
            # https://stackoverflow.com/questions/11092511/python-list-of-unique-dictionaries
            # unique_cards = [dict(s) for s in set(frozenset(d.items()) for d in card_list)]
            # existing_card_data.append(list_dicts_to_add)

            # urls_to_add.insert(0, url)
            urls_to_add.append(url)

            # card_names_to_add.insert(0, list(new_card_name_list))
            card_names_to_add.append(list(new_card_name_list))

            # urls_to_add.append(temp_urls)
            # existing_card_names.append(card_names_to_add)

        # existing_urls.pop(0)
        # card_names_to_add.pop(0)
        # pprint(existing_card_data)
        # pprint(card_names_to_add)
        # pprint(urls_to_add)

        # dict_to_file = {
        #     'url': urls_to_add,
        #     "card_set": existing_card_data,
        # }

        insert_urls_in_db = urls.update_one({"_id": "decklists_urls"},
                                            {"$set": {"urls": urls_to_add}},
                                            upsert=True)

        set_card_names = set()
        for list_card_names in card_names_to_add:
            for card in list_card_names:
                set_card_names.add(card)

        # latest_card_names_dict = {
        #     "card_names": card_names_to_add,
        #     "set_card_names": list(set_card_names)
        # }

        insert_list_card_names_in_db = list_card_names_db.update_one({"_id": "card_names"},
                                                                     {"$set": {"set_card_names": list(set_card_names),
                                                                               "card_names": card_names_to_add}},
                                                                     upsert=True)

        if existing_card_data:
            upserts = [UpdateOne({'_id': x['_id']}, {'$set': x}, upsert=True) for x in existing_card_data]
            # upserts = [UpdateOne({'_id': x['_id']}, {'$setOnInsert': x}, upsert=True) for x in existing_card_data]

            insert_new_cards = cards.bulk_write(upserts)

        # with open('static/card_data_url.json', 'w') as fp:
        #     json.dump(dict_to_file, fp, sort_keys=True, indent=4)
        #
        # with open('static/latest_card_names.json', 'w') as fp:
        #     json.dump(latest_card_names_dict, fp, sort_keys=True, indent=4)

        # card_data_json.close()
        # card_names_list.close()
    else:
        modern_league_url = card_data['url']
        cards_from = 'cards from file'
        unique_cards = card_data['card_set']
        print(cards_from)

    return {
        "modern_league_url": 'https://magic.wizards.com',
        # "modern_league_url": 'https://magic.wizards.com' + modern_league_url,
        # "unique_cards": unique_cards,
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
    # with open(file_name) as f:
    #     return json.load(f)

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
    # pprint(card_info['scryfallJson'])
    # pprint(card_info['scryfallJson']['mana_cost'])
    # pprint(replace_symbols_in_text(card_info['scryfallJson']['mana_cost']))
    card_data, card_oracle_txt, card_mana_cost, card_img, card_flavor_txt = {}, '', '', '', card

    if 'card_faces' in card_info['scryfallJson']:
        for card_faces in card_info['scryfallJson']['card_faces']:
            if card in card_faces['name']:
                card_oracle_txt = card_faces['oracle_text']
                if "flavor_text" in card_faces:
                    card_flavor_txt = card_faces['flavor_text']
                if "mana_cost" in card_faces:
                    card_mana_cost = card_faces['mana_cost']
                    # card_mana_cost = replace_symbols_in_text(card_faces['mana_cost'])
                if "image_uris" not in card_info['scryfallJson']:
                    card_img = card_faces['image_uris']['art_crop']
                else:
                    card_img = card_info['scryfallJson']['image_uris']['art_crop']

    else:
        card_oracle_txt = card_info['scryfallJson']['oracle_text']
        card_mana_cost = card_info['scryfallJson']['mana_cost']
        # card_mana_cost = replace_symbols_in_text(card_info['scryfallJson']['mana_cost'])
        card_img = card_info['scryfallJson']['image_uris']['art_crop']
        if "flavor_text" in card_info['scryfallJson']:
            card_flavor_txt = card_info['scryfallJson']['flavor_text']

    card_data = {
        '_id': card,
        'name': card,
        'oracle_text': card_oracle_txt,
        'mana_cost': card_mana_cost,
        'flavor_text': card_flavor_txt,
        'image': card_img,
        # 'image_url': pil2datauri(get_mtg_img_from_url(card_img))
        # 'image_uri': pil2datauri(get_mtg_img_from_url(card_img))
    }
    # card_data = {
    # card: {
    #     'name': card,
    #     'oracle_text': card_oracle_txt,
    #     'flavor_text': card_flavor_txt,
    #     'image': card_img
    # }}

    # pprint(card_data.keys())
    return card_data


def get_card_data_from_local_file(card: str) -> dict:
    # random_card_data = {}
    cards = mongo.db.cards
    # TODO: Check if all keys are persent in card_info before getting oracle text etc from it, not only for URIs
    pprint("get_card_data_from_local_file broken card - {}".format(card))
    # data_api = read_from_file('static/card_data_url.json')
    # card_data_scryfall = data_api['card_set']
    # card_data_mtgjson = read_from_file('static/ModernAtomic.json')
    # card_data = json.loads(open("static/ModernAtomic.json", encoding="utf8").read())

    # for card in card:
    # pprint(card)

    # card_info = list(filter(lambda x: x if card in x.keys() else None, card_data_scryfall))[0]
    card_info = cards.find_one({"_id": card})

    if 'oracle_text' not in card_info.keys():
        new_card_info = get_single_card_data_from_scryfall(card)
        card_info['oracle_text'] = new_card_info['oracle_text']
        card_info['flavor_text'] = new_card_info['flavor_text']
        card_info['image'] = new_card_info['image']
        # card_info['image_uri'] = new_card_info['image_uri']

        update_existing_decklist_url_in_db = cards.update_one({"_id": card},
                                                              {"$set":
                                                                  {
                                                                      "oracle_text": card_info['oracle_text'],
                                                                      "flavor_text": card_info['flavor_text'],
                                                                      "decklist_id": card_info['decklist_id'],
                                                                      "image": card_info['image'],
                                                                      # "image_uri": card_info['image_uri'],
                                                                  },
                                                              },
                                                              upsert=True)
    # elif card_info is not None and 'image_url' in card_info.keys():
    #     card_info['image_uri'] = pil2datauri(get_mtg_img_from_url(card_info['image_url']))
    # card_info['image_uri'] = card_info['image_uri']
    # else:
    #     card_info['image_uri'] = pil2datauri(get_mtg_img_from_url(card))

    # card_info_count = card_info.count()
    # pprint(card_info)
    # card_info = [x for x in card_data_scryfall if card in x.keys()][0]
    # card_info = [x for x in card_data_scryfall if card in x.keys()][0]

    # pprint(card_info)
    # card_info = next((item for item in card_data_scryfall if card in item), None)

    # card_name = next((key for key in card_data['data'].keys() if card in key), None)
    # card_name = next(
    #     (key for key in card_data_mtgjson['data'].keys() if
    #      card in [key.rstrip().lstrip() for key in key.split("//") if string_found(card, key)]), None)
    # TODO FIX ME PLEASE check for each field if it is in card then create vars
    # if card_info is not None and 'image_uri' in card_info.keys():
    #     card_info['image_uri'] = card_info['image_uri']
    # else:
    #     print("update card with no image_uri from scryfall api ")
    #     new_card_info = get_single_card_data_from_scryfall(card)
    #     card_info['oracle_text'] = new_card_info['oracle_text']
    #     card_info['flavor_text'] = new_card_info['flavor_text']
    #     # card_info['decklist_id'] = new_card_info['decklist_id']
    #     card_info['image'] = new_card_info['image']
    #     card_info['image_uri'] = new_card_info['image_uri']
    #     # oracle_text = new_card_info['oracle_text']
    #     # image_uri = get_single_card_data_from_scryfall(card)['image_uri']
    #
    #     update_existing_decklist_url_in_db = cards.update_one({"_id": card},
    #                                                           {"$set":
    #                                                               {
    #                                                                   "oracle_text": card_info['oracle_text'],
    #                                                                   "flavor_text": card_info['flavor_text'],
    #                                                                   "decklist_id": card_info['decklist_id'],
    #                                                                   "image": card_info['image'],
    #                                                                   "image_uri": card_info['image_uri'],
    #                                                               },
    #                                                           },
    #                                                           upsert=True)
    # pprint(card_info)

    # card_data_json = card_data_mtgjson['data'][card_name][0]

    random_card_data = {
        'name': card,
        'oracle_text': card_info['oracle_text'],
        'flavor_text': card_info['flavor_text'],
        'decklist_id': card_info['decklist_id'],
        'mana_cost': card_info['mana_cost'],
        'image': card_info['image'],
        # 'image_uri': card_info['image_uri']
    }

    # pprint(random_card_data)
    return random_card_data


def string_found(string1, string2):
    if re.search(r"\b" + re.escape(string1) + r"\b", string2):
        return True
    return False


def find_all(card_type, card_colors, card_subtypes, card_identity, card_cmc, not_enough, card_name, card_supertypes,
             last_chance, card_names_atomic):
    modern_atomic = mongo.db.modern_atomic
    # count = modern_atomic.count()

    # pprint()
    # find_all = modern_atomic.aggregate([{"$sample": {"size": 14000}}], batchSize=14000)
    # find_all = modern_atomic.aggregate([{"$sample": {"size": count}}])
    find_all = modern_atomic.find({})
    print(type(find_all))
    # pprint(find_all.count())

    list_similar_cards = []
    # counter = 0
    for card in find_all:

        # if len(list_similar_cards) > 20:
        #     break
        # if card['_id'] == "Nylea, God of the Hunt":
        if card_name != card['_id'] and card['_id'] not in card_names_atomic and "//" not in card['_id']:
            # counter += 1
            # print(counter, ' ', card['_id'])
            try:
                current_type = card['type']
            except KeyError:
                print("No card type for - {0}".format(card['_id']))
            current_subtypes = card['subtypes']
            current_supertypes = card['supertypes']
            current_colors = card['colors']
            current_identity = card['colorIdentity']
            current_id = card['_id']
            # print(current_id,card_name)
            current_name = card['name']

            # pprint(current_name)

            current_cmc = card['convertedManaCost'] if 'convertedManaCost' in card.keys() else ""
            # if current_type != card_type:
            #     continue
            if is_this_a_basic(current_id):
                # pprint(k)
                continue
            # if 'Creature' in card_type and \
            #         'Creature' in current_type and \
            #         'Artifact' in card_type and \
            #         'Artifact' in current_type:
            #     print("wurm here")
            if 'Creature' in card_type and 'Creature' in current_type and 'Artifact' in card_type and 'Artifact' in current_type:
                # print('creature artifact')
                if not_enough:
                    # print("not enough wurms")
                    if card_subtypes[0] in current_subtypes:
                        if current_cmc == card_cmc:
                            list_similar_cards.append(current_id)
                        elif current_colors == card_colors:
                            list_similar_cards.append(current_id)
                    elif card_supertypes == current_supertypes and current_cmc == card_cmc and (
                            card_colors and current_colors == card_colors or current_identity == card_identity):
                        list_similar_cards.append(current_id)
                elif last_chance:
                    if card_supertypes == current_supertypes and (
                            card_colors and current_colors == card_colors or current_identity == card_identity):
                        list_similar_cards.append(current_id)

                else:
                    if card_subtypes[
                        0] in current_subtypes and current_colors == card_colors and current_cmc == card_cmc:
                        # if subtypes == card_subtypes and colors == card_colors and cmc == card_cmc:
                        list_similar_cards.append(current_id)
            elif 'Creature' in card_type and 'Creature' in current_type and current_id not in list_similar_cards and 'Artifact' not in card_type and 'Artifact' not in current_type:
                if not_enough:
                    if card_subtypes[0] in current_subtypes and card_colors:
                        if card_supertypes and card_supertypes == current_supertypes and current_colors == card_colors and current_cmc == card_cmc:
                            list_similar_cards.append(current_id)
                            # continue
                        elif card_supertypes and card_supertypes == current_supertypes and current_colors[
                            0] in card_colors:
                            list_similar_cards.append(current_id)
                            # continue
                        elif card_supertypes and card_supertypes == current_supertypes and current_cmc == card_cmc:
                            list_similar_cards.append(current_id)
                        elif current_colors:
                            if card_supertypes and card_supertypes == current_supertypes and current_cmc == card_cmc and \
                                    current_colors[0] in card_colors:
                                list_similar_cards.append(current_id)
                            elif card_subtypes[0] in current_subtypes and current_colors[
                                0] in card_colors and current_cmc == card_cmc:
                                list_similar_cards.append(current_id)
                    elif card_subtypes[0] in current_subtypes:
                        if card_supertypes and card_supertypes == current_supertypes and current_colors == card_colors and current_cmc == card_cmc:
                            list_similar_cards.append(current_id)
                            # continue
                        elif card_supertypes and card_supertypes == current_supertypes and current_cmc == card_cmc:
                            list_similar_cards.append(current_id)
                        elif current_cmc == card_cmc:
                            list_similar_cards.append(current_id)



                elif last_chance:

                    if card_supertypes and card_supertypes == current_supertypes and current_cmc == card_cmc and \
                            card_subtypes[0] in current_subtypes:
                        list_similar_cards.append(current_id)
                    elif card_supertypes and card_supertypes == current_supertypes and current_cmc == card_cmc:
                        list_similar_cards.append(current_id)
                    elif card_supertypes and card_supertypes == current_supertypes:
                        if current_cmc == card_cmc and current_colors == card_colors:
                            list_similar_cards.append(current_id)
                    elif card_subtypes[0] in current_subtypes:
                        if current_cmc == card_cmc:
                            list_similar_cards.append(current_id)
                            # continue
                        elif current_colors == card_colors:
                            list_similar_cards.append(current_id)

                        # continue
                    # elif current_colors == card_colors:
                    #     list_similar_cards.append(current_id)
                #
                else:
                    if card_subtypes == current_subtypes and current_colors == card_colors and current_cmc == card_cmc and card_supertypes == current_supertypes:
                        # if subtypes == card_subtypes and colors == card_colors and cmc == card_cmc:
                        list_similar_cards.append(current_id)

            elif 'Artifact' in card_type and 'Artifact' in current_type and current_id not in list_similar_cards and 'Creature' not in current_type and 'Creature' not in card_type:
                if not_enough:
                    if current_cmc == card_cmc and current_identity == card_identity:
                        list_similar_cards.append(current_id)
                    elif current_colors == card_colors:
                        list_similar_cards.append(current_id)

                else:
                    if current_identity == card_identity and \
                            current_cmc == card_cmc and \
                            (card_subtypes and current_subtypes == card_subtypes):
                        list_similar_cards.append(current_id)
                    elif current_identity == card_identity and \
                            current_cmc == card_cmc and \
                            current_subtypes == card_subtypes:
                        list_similar_cards.append(current_id)

    return list_similar_cards


def similar_cards(card_name, not_enough=False, last_chance=False, force=False):
    # TODO: fix similar cards for split cards cause converted CMC is combined and not per card
    modern_atomic = mongo.db.modern_atomic
    cards = mongo.db.cards
    pprint("working in similar_cards_2")
    # pprint(card_name)

    card_modern_atomic = modern_atomic.find_one({'_id': card_name})
    # if not force:

    try:
        card_from_cards = cards.find_one({'_id': card_name, "similar_cards": {"$exists": True, "$ne": None}})
        similar_cards = card_from_cards['similar_cards']

        len_sim_cards = len(similar_cards)
        if len_sim_cards >= 3:
            print("similar_cards from db")
            return similar_cards
    except TypeError:
        print("Card does not have similar_cards")

    list_similar_cards = []
    card_id_atomic = card_modern_atomic['_id']
    card_name_atomic = card_modern_atomic['name']
    card_names_atomic = []

    if '//' in card_name_atomic:
        # card_names_atomic = []
        split_card_name_atomic = card_name_atomic.split('//', 1)
        for name in split_card_name_atomic:
            card_names_atomic.append(name.lstrip().rstrip())
    else:
        card_names_atomic = ['icara e super', ' lud']

    # card_info = cards.find_one({'_id': card_name})
    # card_name = card_info['name']

    card_colors = card_modern_atomic['colors']
    card_type = card_modern_atomic['type']
    card_type_s = card_modern_atomic['types']
    card_supertypes = card_modern_atomic['supertypes']

    # if 'Planeswalker' not in card_type:
    #     pprint("not a Planeswalker")
    #     return "1"

    pprint(card_type)

    card_subtypes = card_modern_atomic['subtypes']
    card_identity = card_modern_atomic['colorIdentity']
    card_cmc = card_modern_atomic['convertedManaCost'] if 'convertedManaCost' in card_modern_atomic.keys() else ""

    if 'Planeswalker' in card_type:
        if not_enough:
            # similar_cards = modern_atomic.find(
            #     {"types": card_type_s, "colorIdentity": card_identity, "subtypes": card_subtypes}, limit=10)

            similar_cards = modern_atomic.aggregate([
                {"$match": {"_id": {"$ne": card_id_atomic}, "types": card_type_s,
                            "subtypes": card_subtypes}},
                {"$sample": {"size": 10}}])

        elif last_chance:
            similar_cards = modern_atomic.aggregate([
                {"$match": {"_id": {"$ne": card_id_atomic}, "types": card_type_s,
                            "colorIdentity": card_identity,
                            # "convertedManaCost": card_cmc,
                            }},
                {"$sample": {"size": 10}}])
        else:
            # similar_cards = modern_atomic.find(
            #     {"types": card_type_s, "subtypes": card_subtypes}, limit=10)
            similar_cards = modern_atomic.aggregate([
                {"$match": {"$and": [{"_id": {"$ne": card_id_atomic}},
                                     {"_id": {"$nin": card_names_atomic}}], "types": card_type_s,
                            "subtypes": card_subtypes,
                            "colorIdentity": card_identity}},
                {"$sample": {"size": 10}}])

        list_similar_cards = set([card['_id'] for card in similar_cards])

    # if current_identity == card_identity:
    # list_similar_cards.append(current_name)
    elif 'Tribal' in card_type:
        similar_cards = modern_atomic.find({"_id": {"$ne": card_id_atomic}, "types": {"$in": ["Tribal"]},
                                            'subtypes': card_subtypes})
        list_similar_cards = set([card['_id'] for card in similar_cards])
    elif 'Land' in card_type:

        lands = ['Swamp', 'Mountain', 'Island', 'Plains', 'Forest', 'Wastes',
                 'Snow-Covered Swamp', 'Snow-Covered Mountain', 'Snow-Covered Island', 'Snow-Covered Plains',
                 'Snow-Covered Forest', card_id_atomic]
        if not_enough or last_chance:
            similar_cards = modern_atomic.aggregate([
                {"$match": {
                    "$and": [
                        {"$and": [{"_id": {"$nin": lands}},
                                  {"_id": {"$ne": card_id_atomic}},
                                  {"_id": {"$nin": card_names_atomic}}]},
                        {"types": card_type_s,
                         "colorIdentity": card_identity}
                    ]
                }},
                {"$sample": {"size": 15}}])

            # similar_cards = modern_atomic.find(
            #     {"type": card_type, "colorIdentity": card_identity}, limit=15)
        else:

            similar_cards = modern_atomic.aggregate([
                {"$match": {"$and": [
                    {"_id": {"$ne": card_id_atomic}},
                    {"_id": {"$nin": card_names_atomic}}],
                    "$or": [{"type": card_type, "colorIdentity": card_identity},
                            {"$and": [{"type": card_type, 'subtypes': card_subtypes},
                                      {"type": card_type, 'subtypes': {"$ne": []}}]}]}},
                {"$sample": {"size": 15}}])

        list_similar_cards = set([card['_id'] for card in similar_cards])

    elif 'Creature' in card_type or 'Artifact' in card_type:
        list_similar_cards = find_all(card_type, card_colors, card_subtypes, card_identity, card_cmc,
                                      not_enough, card_name, card_supertypes, last_chance, card_names_atomic)
    #
    elif 'Sorcery' in card_type or 'Instant' in card_type:
        pprint("instant is here")
        if not_enough or last_chance:
            similar_cards = modern_atomic.aggregate([
                # {"$match": {"_id": {"$nin": [card_id_atomic, card_name_atomic]}, "type": card_type,
                #             "colors": card_colors}},
                {"$match": {"$and": [{"_id": {"$ne": card_id_atomic}},
                                     {"_id": {"$nin": card_names_atomic}}],

                            "type": card_type, "colors": card_colors}},
                {"$sample": {"size": 100}}])
        # if current_colors == card_colors:
        #     list_similar_cards.append(current_name)
        else:
            # print(card_type)
            similar_cards = modern_atomic.aggregate(
                [
                    {"$match":

                         {"$and": [{"_id": {"$ne": card_id_atomic}},
                                   {"_id": {"$nin": card_names_atomic}}],
                          "type": card_type, "convertedManaCost": card_cmc, "colors": card_colors
                          }
                     },
                    # {"$match": {"_id": {"$ne": card_id_atomic}, "type": card_type, "convertedManaCost": card_cmc,
                    # "colors": card_colors}},
                    # {"$match": {"_id": { "$ne": card_name_atomic},"$and": [{"types": card_type, "colors": card_colors},
                    #                      {"types": card_type, "convertedManaCost": card_cmc}]}},
                    {"$sample": {"size": 100}}
                    # {"$sample": {"size": 20}}
                ]
            )
        list_similar_cards = set([card['_id'] for card in similar_cards])

    # elif 'Artifact' in card_type:
    # list_similar_cards = find_all(card_type, card_colors, card_subtypes, card_identity, card_cmc,
    #                               not_enough, card_name, card_supertypes)
    # similar_cards = modern_atomic.find(
    #     {"$and": [{"types": card_type, "colors": card_colors},
    #               {"types": card_type, "convertedManaCost": card_cmc}]},
    #     limit=15)

    elif 'Enchantment' in card_type:
        if not_enough or last_chance:
            similar_cards = modern_atomic.aggregate([
                {"$match": {"$and": [
                    {"_id": {"$ne": card_id_atomic}},
                    {"_id": {"$nin": card_names_atomic}}], "type": card_type, "colors": card_colors}},
                {"$sample": {"size": 20}}])
        # if current_colors == card_colors:
        #     list_similar_cards.append(current_name)
        else:
            similar_cards = modern_atomic.aggregate(
                [
                    {
                        "$match":
                            {
                                # "_id": {"$ne": card_id_atomic},
                                # {"$and": [{"_id": {"$ne": card_id_atomic}},
                                #           {"_id": {"$nin": card_names_atomic}}],
                                "$and": [
                                    {"$and": [
                                        {"_id": {"$ne": card_id_atomic}},
                                        {"_id": {"$nin": card_names_atomic}}]
                                    }
                                    ,
                                    {"type": card_type, "colors": card_colors},
                                    {"type": card_type, "convertedManaCost": card_cmc}, ]
                            }
                    },
                    {"$sample": {"size": 10}}
                ]
            )
            # if current_colors == card_colors and current_subtypes == card_subtypes and cmc == card_cmc:
            #     list_similar_cards.append(current_name)
        list_similar_cards = set([card['_id'] for card in similar_cards])
    # list_similar_cards.discard(card_name)
    # if card_name in list_similar_cards:
    list_similar_cards = list(list_similar_cards)
    # print("stuck here")

    # pprint(list_similar_cards)
    cards.update_one({"_id": card_id_atomic},
                     {"$set": {"similar_cards": list_similar_cards}},
                     upsert=True)

    # print("and here stuck here")
    return list_similar_cards


def gen_new_cards(get_all_uris, get_oracle_texts=0):
    pprint("get_all_uris {}".format(get_all_uris, get_oracle_texts))
    cards = mongo.db.cards
    # data = read_from_file('static/card_data_url.json')
    # data = read_from_file('static/card_data_url.json')
    # latest_card_names = read_from_file('static/latest_card_names.json')
    # latest_card_names = read_from_file('static/latest_card_names.json')
    list_card_names = mongo.db.list_card_names
    latest_card_names = list_card_names.find_one({"_id": "card_names"})

    # unique_cards = data['card_set']

    list_card_names = latest_card_names['set_card_names']
    # list_card_names = [list(d.keys())[0] for d in unique_cards]

    # random.shuffle(list_card_names)
    random_card_name = sample(list_card_names, 1)[0]

    # random_card_name = 'Ugin, the Ineffable'
    # random_card_name = 'Klothys, God of Destiny'
    # random_card_name = 'Shefet Dunes'
    # random_card_name = 'Wear'
    # random_card_name = 'Sling-Gang Lieutenant'
    # TODO Darksteel Citadel - Artifact land
    # random_card_name = 'Batterskull'
    # random_card_name = 'Merfolk Secretkeeper'
    # random_card_name = 'Thopter Foundry'
    # random_card_name = 'Ramunap Ruins'
    # random_card_name = 'Breeding Pool'
    # random_card_name = 'Sakura-Tribe Scout'
    # random_card_name = "Narset, Parter of Veils"
    # random_card_name = "Wurmcoil Engine"
    # random_card_name = "Yorion, Sky Nomad"
    # random_card_name = "Renegade Rallier"
    # random_card_name = "Cranial Plating"
    # random_card_name = "Golos, Tireless Pilgrim"
    # random_card_name = "Aria of Flame"
    random_card_name = "Plague Engineer"
    #
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
    if sample_size < 3:
        list_card_names_with_same_type = similar_cards(random_card_name, not_enough=True)
        print(list_card_names_with_same_type)
        # print(len(list_card_names_with_same_type))
        sample_size = len(list_card_names_with_same_type)
        if sample_size < 3:
            # sample_size = len(list_card_names_with_same_type)
            print("for real not enough")
            list_card_names_with_same_type = similar_cards(random_card_name, last_chance=True)
            # pprint(list_card_names_with_same_type)
            if sample_size < 3:
                sample_size = len(list_card_names_with_same_type)
            else:
                sample_size = 3
        else:
            sample_size = 3
    else:
        sample_size = 3
    # TODO: fix for less than 4 of card type?

    random_cards_name_same_type = sample(list_card_names_with_same_type, sample_size)

    random_cards_name_same_type.append(random_card_name)

    # pprint(random_cards_name_same_type)

    random.shuffle(random_cards_name_same_type)
    dict_random_cards_name_same_typ = {}
    dict_random_cards_name_same_type_oracle_texts = {}

    if get_all_uris == '1':
        for card in random_cards_name_same_type:
            card_info = cards.find_one({"_id": card})
            if card_info is not None and 'image' in card_info.keys():
                print("uri_form_db url -", card)
                image_url = card_info['image']
                image_uri = pil2datauri(get_mtg_img_from_url(image_url))
                dict_random_cards_name_same_typ[card] = image_uri
            else:
                print("uri_scryfall_api -", card)
                image_url = get_single_card_data_from_scryfall(card)['image']
                image_uri = pil2datauri(get_mtg_img_from_url(image_url))
                dict_random_cards_name_same_typ[card] = image_uri
                update_existing_decklist_url_in_db = cards.update_one({"_id": card}, {"$set": {"image": image_url}},
                                                                      upsert=True)

    # pprint(dict_random_cards_name_same_typ)
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
    correct_answer_mana_cost = "" if not correct_answer_data['mana_cost'] else replace_symbols_in_text(
        correct_answer_data['mana_cost'])
    correct_answer_decklist_id = correct_answer_data['decklist_id']
    # pprint(correct_answer_oracle_text)
    correct_answer_name = correct_answer_data['name']
    correct_answer_image = correct_answer_data['image']

    correct_answer_image_uri = pil2datauri(get_mtg_img_from_url(correct_answer_image))
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
            "card_info_uris": dict_random_cards_name_same_typ,
            "card_info_oracle_texts": dict_random_cards_name_same_type_oracle_texts,
            "correct_answer_index": correct_answer_index,
            "correct_answer_oracle_text": to_html_list_correct_answer_oracle_text,
            "correct_answer_flavor_text": correct_answer_flavor_text,
            "correct_answer_decklist_id": correct_answer_decklist_id,
            "correct_answer_image": correct_answer_image,
            "correct_answer_mana_cost": correct_answer_mana_cost,
            "correct_answer_image_uri": correct_answer_image_uri,
            "correct_answer_name": correct_answer_name}


def increment_game_mode(game_mode_id, correct):
    # TODO: Update corresponding game mode document fields
    #       total_count, correct/wrong guesses
    game_modes = mongo.db.game_modes
    field_to_increment = "wrong"
    if correct:
        field_to_increment = "correct"
    update_game_modes = game_modes.update_one({"_id": game_mode_id},
                                              {"$inc": {"total_count": 1, field_to_increment: 1}},
                                              upsert=True)


def get_mtg_img_from_url(url):
    response = requests.get(url)
    # pprint(response)
    img = Image.open(BytesIO(response.content))

    return img


def pil2datauri(img):
    # converts PIL image to datauri
    # img = Image.open(BytesIO(response.content))

    data = BytesIO()
    img.save(data, "JPEG")
    data64 = base64.b64encode(data.getvalue())
    return u'data:img/jpeg;base64,' + data64.decode('utf-8')

# pprint(get_single_card_data_from_scryfall('Wear'))
# scrape_card_data()

# local_card_data = read_from_file('static/card_data_url.json')
# existing_card_data = local_card_data['card_set']
# for card in existing_card_data:
#     list_card_names_with_same_type = similar_cards(list(card.keys())[0])
#     sample_size = len(list_card_names_with_same_type)

#
# if sample_size < 4:
#     print('not enough cards')
#     list_card_names_with_same_type = similar_cards(list(card.keys())[0], True)
# pprint(similar_cards(existing_card_data['The Royal Scions']))
# pprint(similar_cards(list(card.keys())[0], not_enough=True))
