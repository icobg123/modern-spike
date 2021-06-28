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
from helpers import *
import datetime as DT
# from db import mongo


from rq import Queue
from worker import conn
from pymongo import MongoClient


# client = MongoClient()


# from helpers import count_words_at_url

#####
# name = 'Fiery Islet'
# name = '"Hanweir Battlements // Hanweir, the Writhing Township"'
# name = 'Keranos, God of Storms'
# name = 'Neglected Heirloom // Ashmouth Blade'
# name = 'Sling-Gang Lieutenant'
# name = 'Uro, Titan of Nature\'s Wrath'
# name = 'Wrath of God'
# name = 'Spectral Procession'
# name = 'Nicol Bolas, Planeswalker'

# cards = json.loads(open("static/ModernAtomic.json", encoding="utf8").read())


# cards = json.loads(open("static/ModernAtomic.json", encoding="utf8").read())

# pprint(type(cards['data'].values()))
# pprint(cards['data'].keys())
# if 'Hanweir Battlements' in "Hanweir Battlements // Hanweir, the Writhing Township":
#     print(True)
# card_name = [key for key, value in cards.items() if name in key]
# card_name = next((key for key in cards['data'].keys() if name in key), None)


# card_name = name

# if card_name is not None:
#     do_something(key)
# card_name = next((item for item in cards if name in item), None)
# pprint(card_name)

# card_info = cards['data'][name][0]

# card_colors = cards['data'][name][0]['colors']
# card_type = cards['data'][name][0]['types'][0]
# card_subtypes = cards['data'][name][0]['subtypes']


# card_cmc = cards['data'][name][0]['convertedManaCost']
# card_subtypes.sort()
# pprint(card_info)


# pprint(card_cmc)


# pprint(card_type)
# pprint(card_subtypes)


# def from_modern_json(card_name, not_enough=False):
#     list_similar_cards = []
#
#     cards = json.loads(open("static/ModernAtomic.json", encoding="utf8").read())
#
#     card_name = next(
#         (key for key in cards['data'].keys() if card_name in [key.rstrip().lstrip() for key in key.split("//")]), None)
#
#     # print(card_name)
#     card_info = cards['data'][card_name][0]
#     card_colors = card_info['colors']
#     card_type = card_info['types']
#     # card_name = card_info['name']
#     # card_type = card_info['types'][0]
#     card_subtypes = card_info['subtypes']
#     if 'convertedManaCost' in card_info:
#         card_cmc = card_info['convertedManaCost']
#         pprint(card_cmc)
#     card_identity = card_info['colorIdentity']
#     card_subtypes.sort()
#     # pprint(card_info)
#
#     for k, v in cards['data'].items():
#         # result = all(elem in card_subtypes for elem in v[0]['subtypes'])
#         this_type = v[0]['types']
#         # this_type = v[0]['types'][0]
#         subtypes = v[0]['subtypes']
#         colors = v[0]['colors']
#         identity = v[0]['colorIdentity']
#         name = v[0]['name']
#         subtypes.sort()
#         colors.sort()
#
#         # pprint(v[0]['name'])
#         if 'convertedManaCost' in v[0].keys():
#             # if this_type != 'Land':
#             cmc = v[0]['convertedManaCost']
#         if this_type != card_type:
#             continue
#
#         if not is_this_a_basic(card_name):
#             # pprint(card_name)
#             continue
#
#         if 'Planeswalker' in card_type:
#             # if card_type == 'Planeswalker':
#             # if not_enough:
#             # if len(list_similar_cards)
#             if subtypes == card_subtypes:
#                 # pprint(k)
#                 list_similar_cards.append(k)
#
#         if 'Land' in card_type:
#             if not_enough:
#                 if identity == card_identity:
#                     list_similar_cards.append(k)
#             else:
#                 if (card_subtypes and subtypes == card_subtypes) or identity == card_identity:
#                     list_similar_cards.append(k)
#                 # elif identity == card_identity:
#                 #     list_similar_cards.append(k)
#
#         if 'Creature' in card_type:
#             if not_enough:
#                 if colors == card_colors and cmc == card_cmc:
#                     list_similar_cards.append(k)
#                 elif subtypes == card_subtypes and cmc == card_cmc:
#                     list_similar_cards.append(k)
#
#             else:
#                 if subtypes == card_subtypes and colors == card_colors and cmc == card_cmc:
#                     list_similar_cards.append(k)
#
#         if 'Sorcery' in card_type or 'Instant' in card_type:
#             if not_enough:
#                 if colors == card_colors and not_enough:
#                     list_similar_cards.append(k)
#             else:
#                 if colors == card_colors and cmc == card_cmc:
#                     list_similar_cards.append(k)
#             # if colors == card_colors and cmc == card_cmc:
#             #     # print(cmc, card_cmc)
#             #     list_similar_cards.append(k)
#             #     continue
#             # elif colors == card_colors and not_enough:
#             #     list_similar_cards.append(k)
#             # else:
#             #     continue
#
#         if 'Artifact' in card_type:
#             if colors == card_colors and cmc == card_cmc and not not_enough:
#                 list_similar_cards.append(k)
#
#             elif cmc == card_cmc:
#                 list_similar_cards.append(k)
#
#         if 'Enchantment' in card_type:
#             if colors == card_colors and subtypes == card_subtypes:
#                 list_similar_cards.append(k)
#
#         if 'Tribal' in card_type:
#             if colors == card_colors:
#                 list_similar_cards.append(k)
#
#     return list_similar_cards
#
#     # elif colors == card_colors:
#     #     # print(subtypes)
#     #     list_similar_subtype.add(k)
#
#     # if result:
#     #     list_similar_subtype.append(k)
#     # print(k, v)


# pprint(from_modern_json(name))
# pprint(len(from_modern_json(name)))


#
# pprint(from_modern_json(name, True))
# pprint(len(from_modern_json(name, True)))

#     pprint(value)
# print(find_key(card[0], 'Human'))
# for key, value in cards.items():
#     pprint("Key:")
#     pprint(key)


# def get_keys(dl, keys_list):
#     if isinstance(dl, dict):
#         keys_list += dl.keys()
#         map(lambda x: get_keys(x, keys_list), dl.values())
#     elif isinstance(dl, list):
#         map(lambda x: get_keys(x, keys_list), dl)
#
#
# keys = []
# get_keys(cards, keys)
# print(keys)

####################
# from mtgsdk import Card
#
# cards = Card.where(name='"Archangel Avacyn"').where(legalities='Modern').all()
# pprint(cards[0].subtypes[0])
# pprint(cards[0].legalities)
# cards1 = Card.where(subtypes=cards[0].subtypes[0]).where(legalities='Modern').all()
# pprint(cards1.name)
#
#
# for card in cards1:
#     pprint(card.name)

# db = CardDb.from_file('static/ModernAtomic.json')
# cards = json.loads(open("static/ModernAtomic.json", encoding="utf8").read())
# pprint(cards)


#
# # card = scrython.cards.Named(fuzzy="Merchant of the Vale")
# card = scrython.cards.Named(fuzzy="Wear")
# card_info = vars(card)
#
# # pprint(card_info['scryfallJson'])
#
# # for card in card_info['scryfallJson']['card_faces']:
# #
# #     if "Wear" in card['name']:
# #         oracle_txt = card['oracle_text']
# #         card_img = card_info['scryfallJson']['image_uris']['art_crop']
# #
# #         print(oracle_txt)
# #         print(card_img)
# # print("icara e mn lud")
# # print(card['oracle_text'])
# # pprint(card_info['scryfallJson']['card_faces'][0]['name'])
# # card = scrython.cards.Named(fuzzy="Merchant of the Vale")
# card = scrython.cards.Named(fuzzy="Bonecrusher Giant")
# # card = scrython.cards.Named(fuzzy="Thing in the Ice")
# card_info = vars(card)
#
# # pprint(card_info['scryfallJson'])
# # pprint(card_info['scryfallJson']['oracle_text'])
# # pprint(replace_card_name_in_oracle(card_info['scryfallJson']['name'], card_info['scryfallJson']['oracle_text']))
#
# if 'card_faces' in card_info['scryfallJson']:
#
#     for card_faces in card_info['scryfallJson']['card_faces']:
#         #
#         # if "image_uris" not in card_info['scryfallJson']:
#         # print("img_uris not in ")
#         pprint(card_faces)
#         # card_img = card_info['scryfallJson']['image_uris']['art_crop']
#     # else:
#     # oracle_txt = card_faces['oracle_text']
#     # pprint(card_faces)
#
#     # card_img = card_faces['image_uris']['art_crop']
#     # if "Thing in the Ice" in card['name']:
#     #     oracle_txt = card['oracle_text']
#     #     # card_img = card_info['scryfallJson']['image_uris']['art_crop']
#     #     card_img = card['image_uris']['art_crop']
#     #
#     #     # print(oracle_txt)
#     #     print(card_img)
#     # print("icara e mn lud")
#     # print(card['oracle_text'])
# # pprint(card_info['scryfallJson']['card_faces'][0]['name'])


# q = Queue(connection=conn)
#
# result = q.enqueue(count_words_at_url, 3)
# pprint(result)


# def is_there_new_data() -> dict:
#     """
#     Checks if new modern tournament decklist data has been published from MTGO
#     :return:is_new_data :bool,latest_modern_tournament_url:str
#     """
#     today = DT.date.today()
#     week_ago = today - DT.timedelta(days=7)
#     # d = DT.datetime.strptime(today, '%Y-%m-%d')
#     today = DT.date.strftime(today, "%m/%d/%Y")
#     week_ago = DT.date.strftime(week_ago, "%m/%d/%Y")
#     print(today, week_ago)
#     is_new_data = False
#     url = 'https://magic.wizards.com/en/section-articles-see-more-ajax?dateoff=&l=en&f=9041&search-result-theme=&limit=30&fromDate=' + week_ago + '&toDate=' + today + '&sort=ASC&word=modern&offset=0'
#     # url = 'https://magic.wizards.com/en/content/deck-lists-magic-online-products-game-info'
#     pprint(url)
#     response = requests.get(url)
#     json_data = response.json()
#     # for url in  response['data']
#     response_html = json_data['data']
#     response_html.reverse()
#     # pprint(response_html)
#     soup = BeautifulSoup('"""' + ''.join(response_html) + '"""', 'html.parser')
#     # soup = BeautifulSoup(response_html, 'html.parser')
#     # print(soup)
#     tournament_urls = []
#     latest_modern_tournament = soup.findAll("a")
#     # pprint(latest_modern_tournament)
#     for a in latest_modern_tournament:
#         if "League" not in a.text:
#             tournament_urls.append('https://magic.wizards.com' + a['href'])
#     # text=re.compile('\bModern\s*(League|Challenge|Preliminary)', flags=re.IGNORECASE))
#     # print(latest_modern_tournament)
#
#     if latest_modern_tournament is None:
#         data = read_from_file('static/card_data_url.json')
#         latest_modern_tournament_urls = data['url']
#     else:
#         # latest_modern_tournament_parent = latest_modern_tournament.parent.parent.parent
#         latest_modern_tournament_urls = tournament_urls
#     #
#     # latest_modern_tournament_url = 'https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-league-2020-07-21'
#     # latest_modern_tournament_url = 'https://magic.wizards.com' + latest_modern_tournament_parent['href']
#     #
#     data = read_from_file('static/card_data_url.json')
#     set_data_url = set(data['url'])
#     set_latest_modern_tournament_urls = set(latest_modern_tournament_urls)
#     pprint(set_data_url)
#     pprint(set_latest_modern_tournament_urls)
#     if set_data_url != set_latest_modern_tournament_urls:
#         is_new_data = True
#     # return tournament_urls
#     return {"is_new_data": is_new_data, "latest_modern_tournament_urls": latest_modern_tournament_urls}


# def old_is_new_data() -> dict:
#     """
#     Checks if new modern tournament decklist data has been published from MTGO
#     :return:is_new_data :bool,latest_modern_tournament_url:str
#     """
#     is_new_data = False
#     url = 'https://magic.wizards.com/en/content/deck-lists-magic-online-products-game-info'
#     response = requests.get(url)
#
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     latest_modern_tournament = soup.find("h3",
#                                          text=re.compile('Modern', flags=re.IGNORECASE))
#     # text=re.compile('\bModern\s*(League|Challenge|Preliminary)', flags=re.IGNORECASE))
#     # print(latest_modern_tournament)
#
#     if latest_modern_tournament is None:
#         data = read_from_file('static/card_data_url.json')
#         latest_modern_tournament_url = data['url']
#     else:
#         latest_modern_tournament_parent = latest_modern_tournament.parent.parent.parent
#
#         # latest_modern_tournament_url = 'https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-league-2020-07-21'
#         latest_modern_tournament_url = 'https://magic.wizards.com' + latest_modern_tournament_parent['href']
#
#     data = read_from_file('static/card_data_url.json')
#     if data['url'] != latest_modern_tournament_url:
#         is_new_data = True
#
#     return {"is_new_data": is_new_data, "latest_modern_tournament_url": latest_modern_tournament_url}


# online_users = mongo.db.card.find_one({'name': 'Crop Rotation'})
# cards = mongo.db.cards
# card = {
#     "_id": "Allosaurus Rider",
#     "decklist_id": "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-preliminary-2020-07-23#eggybenny_-",
#     "flavor_text": "Allosaurus Rider",
#     "image": "https://img.scryfall.com/cards/art_crop/front/8/f/8fdaedf0-c4d2-4c2c-a183-026f06f3c360.jpg?1562924036",
#     "name": "Allosaurus Rider",
#     "oracle_text": "You may exile two green cards from your hand rather than pay this spell's mana cost.\nAllosaurus Rider's power and toughness are each equal to 1 plus the number of lands you control.",
#     "similar_cards": [
#         "Advocate of the Beast",
#         "Aether Herder",
#         "Aetherwind Basker",
#         "Ajani's Comrade",
#         "Arashin War Beast",
#         "Arbor Elf",
#         "Architect of the Untamed",
#         "Archweaver",
#         "Armorcraft Judge",
#         "Avenger of Zendikar",
#         "Axebane Stag",
#         "Battering Wurm",
#         "Beanstalk Giant ",
#         "Beast Whisperer",
#         "Beastcaller Savant",
#         "Behemoth's Herald",
#         "Bloom Tender",
#         "Boreal Druid",
#         "Bounteous Kirin",
#         "Bramblewood Paragon",
#         "Brightwood Tracker",
#         "Carapace Forger",
#         "Carnage Wurm",
#         "Centaur's Herald",
#         "Chancellor of the Tangle",
#         "Civic Wayfinder",
#         "Copperhorn Scout",
#         "Craw Giant",
#         "Cultivator of Blades",
#         "Cylian Elf",
#         "Cylian Sunsinger",
#         "Cytospawn Shambler",
#         "Deep Forest Hermit",
#         "Devkarin Dissident",
#         "Devoted Druid",
#         "District Guide",
#         "Drove of Elves",
#         "Druid of the Anima",
#         "Druid of the Cowl",
#         "Duskdale Wurm",
#         "Dwynen's Elite",
#         "Dwynen, Gilt-Leaf Daen",
#         "Elderscale Wurm",
#         "Elegant Edgecrafters",
#         "Elfhame Druid",
#         "Elven Riders",
#         "Elves of Deep Shadow",
#         "Elvish Archdruid",
#         "Elvish Bard",
#         "Elvish Berserker",
#         "Elvish Branchbender",
#         "Elvish Champion",
#         "Elvish Clancaller",
#         "Elvish Eulogist",
#         "Elvish Handservant",
#         "Elvish Harbinger",
#         "Elvish Lyrist",
#         "Elvish Mystic",
#         "Elvish Pioneer",
#         "Elvish Piper",
#         "Elvish Reclaimer",
#         "Elvish Rejuvenator",
#         "Elvish Scrapper",
#         "Elvish Skysweeper",
#         "Elvish Visionary",
#         "Elvish Warrior",
#         "Emmara Tandris",
#         "Engulfing Slagwurm",
#         "Enormous Baloth",
#         "Essence Warden",
#         "Evolution Sage",
#         "Ezuri's Archers",
#         "Ezuri's Brigade",
#         "Ezuri, Renegade Leader",
#         "Farhaven Elf",
#         "Fauna Shaman",
#         "Fierce Empath",
#         "Foe-Razer Regent",
#         "Frontier Guide",
#         "Fyndhorn Elder",
#         "Gaea's Herald",
#         "Gaea's Revenge",
#         "Garruk's Horde",
#         "Ghastbark Twins",
#         "Ghirapur Guide",
#         "Giant Adephage",
#         "Gilt-Leaf Archdruid",
#         "Gilt-Leaf Seer",
#         "Gladecover Scout",
#         "Gladehart Cavalry",
#         "Glissa Sunseeker",
#         "Glistener Elf",
#         "Godtoucher",
#         "Golgari Decoy",
#         "Golgari Raiders",
#         "Greatbow Doyen",
#         "Greater Sandwurm",
#         "Greenhilt Trainee",
#         "Greenseeker",
#         "Greenside Watcher",
#         "Greenweaver Druid",
#         "Greenwheel Liberator",
#         "Greenwood Sentinel",
#         "Groundshaker Sliver",
#         "Growth-Chamber Guardian",
#         "Guardian of Cloverdell",
#         "Gyre Sage",
#         "Hatchery Spider",
#         "Havenwood Wurm",
#         "Heritage Druid",
#         "Highspire Artisan",
#         "Hornet Queen",
#         "Howling Giant",
#         "Immaculate Magistrate",
#         "Imperious Perfect",
#         "Incubation Druid",
#         "Ivy Lane Denizen",
#         "Jagged-Scar Archers",
#         "Joiner Adept",
#         "Joraga Bard",
#         "Joraga Treespeaker",
#         "Joraga Warcaller",
#         "Jungle Weaver",
#         "Kalonian Behemoth",
#         "Keeper of Progenitus",
#         "Krosan Tusker",
#         "Kujar Seedsculptor",
#         "Leaf Gilder",
#         "Lifecraft Cavalry",
#         "Lifespring Druid",
#         "Llanowar Augur",
#         "Llanowar Elves",
#         "Llanowar Empath",
#         "Llanowar Envoy",
#         "Llanowar Mentor",
#         "Llanowar Scout",
#         "Llanowar Sentinel",
#         "Llanowar Tribe",
#         "Llanowar Visionary",
#         "Lys Alana Bowmaster",
#         "Lys Alana Huntmaster",
#         "Maraleaf Rider",
#         "Marwyn, the Nurturer",
#         "Masked Admirers",
#         "Maul Splicer",
#         "Moldgraf Monstrosity",
#         "Molimo, Maro-Sorcerer",
#         "Mossbridge Troll",
#         "Mul Daya Channelers",
#         "Narnam Renegade",
#         "Nath's Elite",
#         "Nettle Sentinel",
#         "Nissa's Chosen",
#         "Nissa, Vastwood Seer ",
#         "Norwood Ranger",
#         "Nullmage Shepherd",
#         "Nurturer Initiate",
#         "Oak Street Innkeeper",
#         "Oakgnarl Warrior",
#         "Oakhame Adversary",
#         "Oracle of Mul Daya",
#         "Panglacial Wurm",
#         "Paradise Druid",
#         "Peema Aether-Seer",
#         "Peema Outrider",
#         "Pelakka Wurm",
#         "Pelt Collector",
#         "Pendelhaven Elder",
#         "Petrified Wood-Kin",
#         "Plated Crusher",
#         "Plated Slagwurm",
#         "Pollenbright Druid",
#         "Primal Forcemage",
#         "Protean Hulk",
#         "Quilled Slagwurm",
#         "Rampaging Brontodon",
#         "Reclamation Sage",
#         "Regal Force",
#         "Rhys the Exiled",
#         "Riftsweeper",
#         "Rishkar, Peema Renegade",
#         "Roaring Slagwurm",
#         "Rootbreaker Wurm",
#         "Rosethorn Acolyte ",
#         "Sacellum Archers",
#         "Sacellum Godspeaker",
#         "Sage of Shaila's Claim",
#         "Sandsteppe Mastodon",
#         "Saruli Gatekeepers",
#         "Scattershot Archer",
#         "Servant of the Conduit",
#         "Shaman of Spring",
#         "Siege Wurm",
#         "Sifter Wurm",
#         "Silhana Ledgewalker",
#         "Silhana Starfletcher",
#         "Silhana Wayfinder",
#         "Silkweaver Elite",
#         "Skyshroud Ranger",
#         "Skyway Sniper",
#         "Spearbreaker Behemoth",
#         "Spire Tracer",
#         "Springbloom Druid",
#         "Steel Leaf Champion",
#         "Sunblade Elf",
#         "Sylvan Advocate",
#         "Sylvan Messenger",
#         "Sylvan Primordial",
#         "Sylvan Ranger",
#         "Tajuru Archer",
#         "Tajuru Beastmaster",
#         "Tajuru Pathwarden",
#         "Tajuru Preserver",
#         "Tajuru Stalwart",
#         "Tajuru Warcaller",
#         "Talara's Battalion",
#         "Tel-Jilad Archers",
#         "Tel-Jilad Chosen",
#         "Tel-Jilad Fallen",
#         "Tel-Jilad Outrider",
#         "Thelon of Havenwood",
#         "Thelonite Hermit",
#         "Thorn Elemental",
#         "Thorn Lieutenant",
#         "Thorn Mammoth",
#         "Thornscape Battlemage",
#         "Thornweald Archer",
#         "Thundering Spineback",
#         "Tornado Elemental",
#         "Treeshaker Chimera",
#         "Treetop Ambusher",
#         "Trolls of Tel-Jilad",
#         "Trostani's Summoner",
#         "Turntimber Ranger",
#         "Twinblade Slasher",
#         "Vastwood Animist",
#         "Verdant Sun's Avatar",
#         "Vine Kami",
#         "Viridian Acolyte",
#         "Viridian Betrayers",
#         "Viridian Corrupter",
#         "Viridian Emissary",
#         "Viridian Joiner",
#         "Viridian Lorebearers",
#         "Viridian Scout",
#         "Viridian Shaman",
#         "Viridian Zealot",
#         "Warren-Scourge Elf",
#         "Wild Wanderer",
#         "Wildborn Preserver",
#         "Wildheart Invoker",
#         "Wildslayer Elves",
#         "Wildwood Tracker",
#         "Winnower Patrol",
#         "Wolf-Skull Shaman",
#         "Wood Elves",
#         "Woodland Champion",
#         "Woodland Mystic",
#         "Woolly Loxodon",
#         "Wrecking Beast",
#         "Wren's Run Packmaster",
#         "Wren's Run Vanquisher",
#         "Wurmskin Forger",
#         "Yeva's Forcemage",
#         "Yeva, Nature's Herald"
#     ],
#     "type": "Creature"
# }

def insert_cards_from_local():
    url_data = read_from_file('static/card_data_url.json')
    data = url_data['card_set']
    new_cards_dict = []
    cards = mongo.db.cards

    for old_card in data:
        # pprint(old_card.keys())
        # pprint(old_card.values())
        # for k, v in old_card:
        #     print(k,v)
        key = list(old_card.keys())[0]
        dict_to_add = {'_id': key,
                       'decklist_id': old_card[key]['decklist_id'],
                       'flavor_text': old_card[key]['flavor_text'],
                       'image': old_card[key]['image'],
                       'name': old_card[key]['name'],
                       'oracle_text': old_card[key]['oracle_text']}
        # if old_card[key]['decklist_id']:

        if 'similar_cards' in old_card.keys():
            dict_to_add['similar_cards'] = old_card[key]['similar_cards']
        new_cards_dict.append(dict_to_add)

    upserts = [UpdateOne({'_id': x['_id']}, {'$setOnInsert': x}, upsert=True) for x in new_cards_dict]
    pprint(upserts)
    insert_new_cards = cards.bulk_write(upserts)


# insert_cards_from_local()

def import_cards():
    card_data = read_from_file('urls.json')
    card_data = list(card_data)
    modern_atomic_upserts = [UpdateOne({'_id': x['_id']}, {'$setOnInsert': x}, upsert=True) for x in
                             card_data if x]

    pprint(modern_atomic_upserts)
    # cards = mongo.db.cards
    urls = mongo.db.urls

    insert_new_cards_modern_atomic = urls.bulk_write(modern_atomic_upserts)


# import_cards()


# urls = mongo.db.urls

# latest_card_names_f = read_from_file('static/latest_card_names.json')
#
#
# list_card_names_from_file_set = latest_card_names_f['set_card_names']
# list_card_names_from_file_list = latest_card_names_f['card_names']
#
# list_card_names = mongo.db.list_card_names
# insert_list_card_names_in_db = list_card_names.update_one({"_id": "card_names"},
#                                                           {"$set": {"set_card_names": list(list_card_names_from_file_set),
#                                                                     "card_names": list_card_names_from_file_list}},
#                                                           upsert=True)
# pprint(new_card)


# set_of_jsons = {json.dumps(d, sort_keys=True) for d in data}
# X = [json.loads(t) for t in set_of_jsons]
# pprint(X)
#
# dict_to_file = {
#     'url': [
#         "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-preliminary-2020-08-07",
#         "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-preliminary-2020-08-08",
#         "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-showcase-challenge-2020-08-09",
#         "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2020-08-10"
#     ],
#     "card_set": X,
# }
# with open('static/card_data_url.json', 'w') as fp:
#     json.dump(dict_to_file, fp, sort_keys=True, indent=4)


def from_atomic_to_db():
    modern_atomic = read_from_file('static/ModernAtomic.json')
    modern_atomic_data = modern_atomic['data']
    new_cards_dict_atomic = []
    modern_atomic = mongo.db.modern_atomic

    card_ids = modern_atomic.find().distinct('_id')
    pprint(card_ids)
    for current_card_name, current_card_data in modern_atomic_data.items():  # pprint(old_card.keys())
        atomic_dict_to_add = {}
        # TODO: FIX bug with flip planeswalker having creature as type not pw
        oracle_text = ''

        if current_card_name in card_ids:
            continue

        if len(current_card_data) > 1:
            # pprint(current_card_name)
            # pprint(type(current_card_data[0]))
            # current_card_data = current_card_data[0]
            split_str = current_card_name.split('//', 1)
            split_str.reverse()

            # check = any(item in split_str for item in card_ids)

            # if check:
            #     continue

            # pprint(split_str[1])
            # print(current_card_data)
            # pprint(len(split_str))
            for card in range(0, len(split_str)):
                # for split_card_name in split_str:
                # pprint(current_card_data[split_card_name]['faceName'])
                # current_card_data = current_card_data[split_card_name]
                # print(current_card_data)

                split_card_name = split_str[card].rstrip().lstrip()

                card = current_card_data[card]
                pprint(split_card_name)
                # pprint(current_card_data[card])

                #
                # pprint(split_card_name)
                try:
                    oracle_text = card['text']
                except KeyError:
                    print("No oracle text")
                atomic_dict_to_add = {'_id': split_card_name,
                                      'colorIdentity': card['colorIdentity'],
                                      'colors': card['colors'],
                                      'convertedManaCost': card['convertedManaCost'],
                                      'layout': card['layout'],
                                      'subtypes': card['subtypes'],
                                      'supertypes': card['supertypes'],
                                      'type': card['type'],
                                      'types': card['types'],
                                      'text': oracle_text,
                                      'name': card['name']}
                new_cards_dict_atomic.append(atomic_dict_to_add)
        else:
            # pprint()
            # break
            # pprint(current_card_name)
            card = current_card_data[0]
            try:
                oracle_text = card['text']
            except KeyError:
                print("No oracle text")
            atomic_dict_to_add = {'_id': current_card_name,
                                  'colorIdentity': card['colorIdentity'],
                                  'colors': card['colors'],
                                  'convertedManaCost': card['convertedManaCost'],
                                  'layout': card['layout'],
                                  'subtypes': card['subtypes'],
                                  'supertypes': card['supertypes'],
                                  'type': card['type'],
                                  'types': card['types'],
                                  'text': oracle_text,
                                  'name': card['name']}

            new_cards_dict_atomic.append(atomic_dict_to_add)
        # new_cards_dict_atomic.append(atomic_dict_to_add)
    # pprint(new_cards_dict_atomic)

    # Update all card properties
    modern_atomic_upserts = [UpdateOne({'_id': x['_id']}, {'$set': x}, upsert=True) for x in
                             new_cards_dict_atomic if x]

    # Update only oracle text
    # modern_atomic_upserts = [UpdateOne({'_id': x['_id']}, {"$set": {"oracle_text": x['text']}}, upsert=True) for x in
    #                          new_cards_dict_atomic if x]
    pprint(modern_atomic_upserts)
    insert_new_cards_modern_atomic = modern_atomic.bulk_write(modern_atomic_upserts)


# from_atomic_to_db()


# pprint(mongo.db.cards)
# pprint(len(card_ids))
# img_url = "https://img.scryfall.com/cards/art_crop/front/6/0/6072d9b0-d3c7-46f4-bd24-095bb13c4dea.jpg?1572489660"
# pprint(pil2datauri(get_mtg_img_from_url(img_url)))

# update card image link in card collection in db
def update_card_info_from_modern_atomic():
    modern_atomic = mongo.db.modern_atomic
    cards = mongo.db.cards
    cursor = cards.find({})
    # cursor = modern_atomic.find({})
    counter = 0
    for document in cursor:
        # pprint(document)
        try:
            if get_mtg_img_from_url(document['image']):
                pprint("{0}: there is img for - {1} ".format(counter, document['_id']))
                # print(counter)
                counter += 1
                continue
        except KeyError:
            print("no img found")

        if '//' in document['_id']:

            # print("// in name {} ".format(card_name))

            split_str = document['_id'].split('//', 1)
            for split_card_name in split_str:
                print(split_card_name)
                split_card_name = split_card_name.rstrip().lstrip()
                img_uri = get_single_card_data_from_scryfall(split_card_name)['image']
                result = cards.update_one({"_id": document['_id']},
                                          {"$set": {"image": img_uri}},
                                          upsert=True)
        else:
            # print(document)
            img_uri = get_single_card_data_from_scryfall(document['_id'])['image']
            pprint(img_uri)
            # img_uri = pil2datauri(get_mtg_img_from_url(document['image']))

            result = cards.update_one({"_id": document['_id']},
                                      {"$set": {"image": img_uri}},
                                      upsert=True)
        print(document['_id'])
        print(counter)
        counter += 1
        # if counter == 2:
        #     break
        # print()


# update_card_info_from_modern_atomic()
# Consign
# Expansion
# Flesh
# Gisela, the Broken Blade
# Wear

# pprint(get_mtg_img_from_url(
#     "https://c1.scryfall.com/file/scryfall-cards/art_crop/front/4/f/4f34efbb-70c3-44d2-a914-1d89dfd50ca7.jpg?1599769266"))
# pprint(pil2datauri(get_mtg_img_from_url("https://c1.scryfall.com/file/scryfall-cards/art_crop/front/4/f/4f34efbb-70c3-44d2-a914-1d89dfd50ca7.jpg?1599769266")))
# pprint(pil2datauri(get_mtg_img_from_url("https://c1.scryfall.com/file/scryfall-cards/art_crop/front/9/0/90694ded-b790-4b96-a72c-57795474711f.jpg")))
# pprint(get_mtg_img_from_url(
#     "https://c1.scryfall.com/file/scryfall-cards/art_crop/front/9/0/90694ded-b790-4b96-a72c-57795474711f.jpg"))
#
# pprint(similar_cards('Explosion', not_enough=False))

# def find_all(card_type, card_colors, card_subtypes, card_identity, card_cmc, not_enough, card_name, card_supertypes):
#     modern_atomic = mongo.db.modern_atomic
#     count = modern_atomic.count()
#
#     find_all = modern_atomic.aggregate([{"$sample": {"size": count}}])
#     # find_all = modern_atomic.find({})
#     print(type(find_all))
#
#     list_similar_cards = []
#     for card in find_all:
#         if card_name != card['_id']:
#
#             current_type = card['type']
#             current_subtypes = card['subtypes']
#             current_supertypes = card['supertypes']
#             current_colors = card['colors']
#             current_identity = card['colorIdentity']
#             current_id = card['_id']
#             current_name = card['name']
#
#             current_cmc = card['convertedManaCost'] if 'convertedManaCost' in card.keys() else ""
#             # if current_type != card_type:
#             #     continue
#             if is_this_a_basic(current_id):
#                 # pprint(k)
#                 continue
#             if 'Creature' in card_type and 'Creature' in current_type:
#                 if not_enough:
#                     if card_subtypes[
#                         0] in current_subtypes and current_colors == card_colors and current_cmc == card_cmc:
#                         list_similar_cards.append(current_id)
#                     elif card_subtypes[0] in current_subtypes and current_cmc == card_cmc:
#                         list_similar_cards.append(current_id)
#                     elif card_subtypes[0] in current_subtypes and current_colors == card_colors:
#                         list_similar_cards.append(current_id)
#                     elif card_supertypes == current_supertypes and current_cmc == card_cmc and current_colors == card_colors:
#                         list_similar_cards.append(current_id)
#                 #
#                 else:
#                     if card_subtypes[
#                         0] in current_subtypes and current_colors == card_colors and current_cmc == card_cmc:
#                         # if subtypes == card_subtypes and colors == card_colors and cmc == card_cmc:
#                         list_similar_cards.append(current_id)
#             if 'Artifact' in card_type and 'Artifact' in current_type:
#                 if not_enough:
#                     if current_cmc == card_cmc and current_colors == card_colors:
#                         list_similar_cards.append(current_name)
#                     elif current_colors == card_colors:
#                         list_similar_cards.append(current_name)
#
#                 else:
#                     if current_colors == card_colors and \
#                             current_cmc == card_cmc and \
#                             (card_subtypes and current_subtypes == card_subtypes) and not not_enough:
#                         list_similar_cards.append(current_name)
#
#     return list_similar_cards

# def similar_cards(card_name, not_enough=False):
#     # TODO: Fix lands same identity and creature identity
#     pprint(card_name)
#     list_similar_cards = []
#     cards = read_from_file('static/ModernAtomic.json')
#
#     local_card_data = read_from_file('static/card_data_url.json')
#     existing_card_data = local_card_data['card_set']
#
#     card_info = next(
#         (item[card_name]['similar_cards'] for item in existing_card_data if
#          card_name in item and 'similar_cards' in item[card_name].keys()),
#         None)
#     # pprint(card_info)
#
#     if card_info and len(card_info) > 3:
#         print('card in info')
#         return card_info
#
#     all_card_names = cards['data'].keys()
#
#     # card_name = next(
#     #     (key for key in cards['data'].keys() if
#     #      card_name in [key.rstrip().lstrip() for key in key.split("//") if string_found(card_name, key)]), None)
#
#     card_name_full = ""
#     for name in all_card_names:
#         if '//' in name:
#             if name.split("//")[0].rstrip().lstrip() == card_name or name.split("//")[1].rstrip().lstrip():
#                 card_name_full = name
#                 break
#         elif name == card_name:
#             card_name_full = name
#             break
#     card_name = card_name_full
#
#     # pprint(card_name)
#     #  card_name = next(
#     #     (key for key in cards['data'].keys() if card_name in [key.rstrip().lstrip() for key in key.split("//")]), None)
#     #
#     # # cards = json.loads(open("static/ModernAtomic.json", encoding="utf8").read())
#
#     card_info = cards['data'][card_name][0]
#     card_colors = card_info['colors']
#     card_type = card_info['types']
#     card_subtypes = card_info['subtypes']
#     card_identity = card_info['colorIdentity']
#     card_cmc = card_info['convertedManaCost'] if 'convertedManaCost' in card_info else ""
#
#     # card_subtypes.sort()
#     # pprint(card_info)
#
#     for current_card_name, current_card_data in cards['data'].items():
#         # result = all(elem in card_subtypes for elem in v[0]['subtypes'])
#         # if len(list_similar_cards) > 15:
#         #     break
#
#         if current_card_name != card_name:
#             current_type = current_card_data[0]['types']
#             current_subtypes = current_card_data[0]['subtypes']
#             current_colors = current_card_data[0]['colors']
#             current_identity = current_card_data[0]['colorIdentity']
#             current_name = current_card_data[0]['name']
#             if '//' in current_name:
#                 current_name = current_name[:current_name.index("/")]
#
#             # if this_type != 'Land':
#             cmc = current_card_data[0]['convertedManaCost'] if 'convertedManaCost' in current_card_data[
#                 0].keys() else ""
#             if current_type != card_type:
#                 continue
#             if is_this_a_basic(current_card_name):
#                 # pprint(k)
#                 continue
#
#             if 'Planeswalker' in card_type:
#                 # if card_type == 'Planeswalker':
#                 # if not_enough:
#                 # if len(list_similar_cards)
#                 if not_enough:
#                     if current_subtypes == card_subtypes:
#                         # pprint(k)
#                         list_similar_cards.append(current_name)
#                 else:
#                     if current_identity == card_identity:
#                         list_similar_cards.append(current_name)
#
#             if 'Land' in card_type and current_card_name not in list_similar_cards:
#                 if not_enough:
#                     if current_identity == card_identity:
#                         list_similar_cards.append(current_name)
#                 else:
#                     if (card_subtypes and current_subtypes == card_subtypes) or current_identity == card_identity:
#                         list_similar_cards.append(current_name)
#
#             # if 'Land' in card_type:
#             #     if not_enough:
#             #         if identity == card_identity:
#             #             list_similar_cards.append(k)
#             #     else:
#             #         if identity == card_identity:
#             #             list_similar_cards.append(k)
#
#             if 'Creature' in card_type and current_card_name not in list_similar_cards:
#                 if not_enough:
#                     if current_colors == card_colors and cmc == card_cmc:
#                         list_similar_cards.append(current_name)
#                     elif card_subtypes[0] in current_subtypes and cmc == card_cmc:
#                         list_similar_cards.append(current_name)
#                     elif card_subtypes[0] in current_subtypes and current_colors == card_colors:
#                         list_similar_cards.append(current_name)
#
#
#                 else:
#                     if card_subtypes[0] in current_subtypes and current_colors == card_colors and cmc == card_cmc:
#                         # if subtypes == card_subtypes and colors == card_colors and cmc == card_cmc:
#                         list_similar_cards.append(current_name)
#
#             if 'Sorcery' in card_type or 'Instant' in card_type and current_card_name not in list_similar_cards:
#                 if not_enough:
#                     if current_colors == card_colors:
#                         list_similar_cards.append(current_name)
#                 else:
#                     if current_colors == card_colors and cmc == card_cmc:
#                         list_similar_cards.append(current_name)
#                 # if colors == card_colors and cmc == card_cmc:
#                 #     # print(cmc, card_cmc)
#                 #     list_similar_cards.append(k)
#                 #     continue
#                 # elif colors == card_colors and not_enough:
#                 #     list_similar_cards.append(k)
#                 # else:
#                 #     continue
#
#             if 'Artifact' in card_type and current_card_name not in list_similar_cards:
#                 if current_colors == card_colors and \
#                         cmc == card_cmc and \
#                         (card_subtypes and current_subtypes == card_subtypes) and not not_enough:
#                     list_similar_cards.append(current_name)
#
#                 elif cmc == card_cmc and current_colors == card_colors:
#                     list_similar_cards.append(current_name)
#                 elif current_colors == card_colors:
#                     list_similar_cards.append(current_name)
#
#             if 'Enchantment' in card_type and current_card_name not in list_similar_cards:
#                 if not_enough:
#                     if current_colors == card_colors:
#                         list_similar_cards.append(current_name)
#                 else:
#                     if current_colors == card_colors and current_subtypes == card_subtypes and cmc == card_cmc:
#                         list_similar_cards.append(current_name)
#
#             if 'Tribal' in card_type and current_card_name not in list_similar_cards:
#                 if current_colors == card_colors:
#                     list_similar_cards.append(current_name)
#
#     # pprint(list_similar_cards)
#     # if len(list_similar_cards) < 5:
#     #     similar_cards(card_name, True)
#     for card in existing_card_data:
#         if card_name in card.keys():
#             card[card_name]['similar_cards'] = list_similar_cards
#             break
#
#     local_card_data['card_set'] = existing_card_data
#     with open('static/card_data_url.json', 'w') as fp:
#         json.dump(local_card_data, fp, sort_keys=True, indent=4)
#
#     return list_similar_cards
#
#     # elif colors == card_colors:
#     #     # print(subtypes)
#     #     list_similar_subtype.add(k)
#
#     # if result:
#     #     list_similar_subtype.append(k)
#     # print(k, v)


# def similar_cards_2(card_name, not_enough=False):
#     # TODO: fix similar cards for split cards cause converted CMC is combined and not per card
#     modern_atomic = mongo.db.modern_atomic
#     cards = mongo.db.cards
#     pprint("working in similar_cards_2")
#
#     pprint(card_name)
#
#     card_modern_atomic = modern_atomic.find_one({'_id': card_name})
#     if "similar_cards" in card_modern_atomic.keys():
#         len_sim_cards = len(card_modern_atomic['similar_cards'])
#         if len_sim_cards > 3:
#             return card_modern_atomic['similar_cards']
#
#     list_similar_cards = []
#     card_name_atomic = card_modern_atomic['_id']
#     # card_info = cards.find_one({'_id': card_name})
#     # card_name = card_info['name']
#
#     card_colors = card_modern_atomic['colors']
#     card_type = card_modern_atomic['type']
#     card_type_s = card_modern_atomic['types']
#     card_supertypes = card_modern_atomic['supertypes']
#     pprint(card_type)
#
#     card_subtypes = card_modern_atomic['subtypes']
#     card_identity = card_modern_atomic['colorIdentity']
#     card_cmc = card_modern_atomic['convertedManaCost'] if 'convertedManaCost' in card_info.keys() else ""
#
#     if 'Planeswalker' in card_type:
#         if not_enough:
#             # similar_cards = modern_atomic.find(
#             #     {"types": card_type_s, "colorIdentity": card_identity, "subtypes": card_subtypes}, limit=10)
#
#             similar_cards = modern_atomic.aggregate([
#                 {"$match": {"_id": {"$ne": card_name_atomic}, "types": card_type_s, "colorIdentity": card_identity}},
#                 {"$sample": {"size": 10}}])
#
#         else:
#             # similar_cards = modern_atomic.find(
#             #     {"types": card_type_s, "subtypes": card_subtypes}, limit=10)
#             similar_cards = modern_atomic.aggregate([
#                 {"$match": {"_id": {"$ne": card_name_atomic}, "types": card_type_s, "subtypes": card_subtypes}},
#                 {"$sample": {"size": 10}}])
#
#         list_similar_cards = set([card['_id'] for card in similar_cards])
#
#     # if current_identity == card_identity:
#     # list_similar_cards.append(current_name)
#     elif 'Tribal' in card_type:
#         similar_cards = modern_atomic.find({"types": {"$in": ["Tribal"]},
#                                             'subtypes': card_subtypes})
#         list_similar_cards = set([card['_id'] for card in similar_cards])
#     elif 'Land' in card_type:
#         if not_enough:
#             similar_cards = modern_atomic.aggregate([
#                 {"$match": {"_id": {"$ne": card_name_atomic},
#                             "types": card_type_s, "colorIdentity": card_identity}},
#                 {"$sample": {"size": 15}}])
#
#             # similar_cards = modern_atomic.find(
#             #     {"type": card_type, "colorIdentity": card_identity}, limit=15)
#         else:
#
#             similar_cards = modern_atomic.aggregate([
#                 {"$match": {"_id": {"$ne": card_name_atomic},
#                             "$or": [{"type": card_type, "colorIdentity": card_identity},
#                                     {"$and": [{"type": card_type, 'subtypes': card_subtypes},
#                                               {"type": card_type, 'subtypes': {"$ne": []}}]}]}},
#                 {"$sample": {"size": 15}}])
#
#         list_similar_cards = set([card['_id'] for card in similar_cards])
#
#     elif 'Creature' in card_type:
#         list_similar_cards = find_all(card_type, card_colors, card_subtypes, card_identity, card_cmc,
#                                       not_enough, card_name, card_supertypes)
#     #
#     elif 'Sorcery' in card_type or 'Instant' in card_type:
#         pprint("instant is here")
#         if not_enough:
#             similar_cards = modern_atomic.aggregate([
#                 {"$match": {"_id": {"$ne": card_name_atomic}, "type": card_type, "colors": card_colors}},
#                 {"$sample": {"size": 20}}])
#         # if current_colors == card_colors:
#         #     list_similar_cards.append(current_name)
#         else:
#             print(card_type)
#             similar_cards = modern_atomic.aggregate(
#                 [
#                     {"$match": {"_id": {"$ne": card_name_atomic}, "type": card_type, "convertedManaCost": card_cmc,
#                                 "colors": card_colors}},
#                     # {"$match": {"_id": { "$ne": card_name_atomic},"$and": [{"types": card_type, "colors": card_colors},
#                     #                      {"types": card_type, "convertedManaCost": card_cmc}]}},
#                     {"$sample": {"size": 20}}
#                 ]
#             )
#         list_similar_cards = set([card['_id'] for card in similar_cards])
#
#     elif 'Artifact' in card_type:
#         list_similar_cards = find_all(card_type, card_colors, card_subtypes, card_identity, card_cmc,
#                                       not_enough, card_name, card_supertypes)
#     # similar_cards = modern_atomic.find(
#     #     {"$and": [{"types": card_type, "colors": card_colors},
#     #               {"types": card_type, "convertedManaCost": card_cmc}]},
#     #     limit=15)
#
#     elif 'Enchantment' in card_type:
#         if not_enough:
#             similar_cards = modern_atomic.aggregate([
#                 {"$match": {"_id": {"$ne": card_name_atomic}, "type": card_type, "colors": card_colors}},
#                 {"$sample": {"size": 20}}])
#         # if current_colors == card_colors:
#         #     list_similar_cards.append(current_name)
#         else:
#             similar_cards = modern_atomic.aggregate(
#                 [
#                     {
#                         "$match":
#                             {
#                                 "_id": {"$ne": card_name_atomic},
#                                 "$and": [{"type": card_type, "colors": card_colors},
#                                          {"type": card_type, "convertedManaCost": card_cmc}, ]
#                             }
#                     },
#                     {"$sample": {"size": 10}}
#                 ]
#             )
#             # if current_colors == card_colors and current_subtypes == card_subtypes and cmc == card_cmc:
#             #     list_similar_cards.append(current_name)
#         list_similar_cards = set([card['_id'] for card in similar_cards])
#     # list_similar_cards.discard(card_name)
#     # if card_name in list_similar_cards:
#     list_similar_cards = list(list_similar_cards)
#     # cards.update_one({"_id": card_name_atomic},
#     #                  {"$set": {"similar_cards": list_similar_cards}},
#     #                  upsert=True)
#
#     return list_similar_cards


# pprint(similar_cards_2('Lightning Bolt', not_enough=False))
# pprint(similar_cards_2('Jace Beleren', not_enough=False))
# pprint(similar_cards_2('Sigil of the Empty Throne', not_enough=False))
# pprint(similar_cards_2('Thopter Foundry', not_enough=True))
# pprint(similar_cards_2('Ensnaring Bridge', not_enough=False))
# pprint(similar_cards_2('Breeding Pool', not_enough=True))
# pprint(similar_cards_2('Tarfire', not_enough=True))
# pprint(similar_cards_2('Klothys, God of Destiny', not_enough=True))
# pprint(similar_cards_2('Heliod, God of the Sun', not_enough=False))
# pprint(similar_cards_2('Heliod, God of the Sun', not_enough=True))
# pprint(similar_cards_2('Heliod, God of the Sun', last_chance=True))
# pprint(similar_cards_2('Thalia, Guardian of Thraben', not_enough=True))
# pprint(similar_cards('Nylea, Keen-Eyed', force=True))
# pprint(similar_cards('Nylea, Keen-Eyed', not_enough=True, force=True))
# pprint(similar_cards('Nylea, Keen-Eyed', last_chance=True, force=True))
# pprint(similar_cards('Nylea, Keen-Eyed', force=False))
#
# pprint(similar_cards_2("Wurmcoil Engine", not_enough=False))
#
# pprint(similar_cards_2("Renegade Rallier", not_enough=True))
# pprint(similar_cards("Bonecrusher Giant",last_chance=True))
# pprint(len(similar_cards("Bonecrusher Giant",last_chance=True)))
# pprint(similar_cards_2("Tear"))

# pprint(similar_cards_2("Ketria Triome", last_chance=True))

# pprint(similar_cards("Kroxa, Titan of Death's Hunger",not_enough=True))
# pprint(similar_cards("Ugin, the Spirit Dragon"))
# pprint(similar_cards("Ugin, the Spirit Dragon",not_enough=True))
# pprint(similar_cards("Ugin, the Spirit Dragon",last_chance=True))
# pprint(similar_cards("Ugin, the Spirit Dragon",last_chance=True))
# pprint(similar_cards("Ugin, the Spirit Dragon",last_chance=True))

# for num in range(15000):
#     print(num)
# DB_URI = os.environ['NEW_DB_URI']
# pprint(DB_URI)
# client = MongoClient(DB_URI)

import timeit


# print(pymongo.has_c())
def end_me():
    # mongo_client = client['modern-spike']
    # modern_atomic = mongo_client.modern_atomic

    modern_atomic = mongo.db.cards
    # modern_atomic = mongo.db.modern_atomic
    # count = modern_atomic.count()

    # pprint(count)
    # find_all = modern_atomic.aggregate([{"$sample": {"size": count}}])
    # find_all = modern_atomic.aggregate([{"$sample": {"size": count}}])
    # stats = mongo_client.stats()
    # find_all = modern_atomic.find({}, batch_size=99).sort("_id")
    # find_all2 = modern_atomic.find({}, batch_size=20).sort("_id").explain()
    # find_all = modern_atomic.aggregate([{"$sample": {"size": count}}], batchSize=count)
    find_all = modern_atomic.find({})
    print(find_all)
    # print(type(find_all))
    # pprint(find_all)
    # pprint(find_all2)
    # pprint(mongo_client.command("serverStatus"))
    list_similar_cards = []
    counter = 0
    for card in find_all:
        counter += 1
        print(counter)


# end_me()
def update_image_urls():
    return


def split_cards():
    cards = mongo.db.cards

    in_existing_card_data = True if cards.count_documents({'_id': "Tear"},
                                                          limit=1) else False

    return in_existing_card_data


# print(split_cards())


def update_all_sim_cards():
    cards = mongo.db.cards
    # card_names = mongo.db.list_card_names
    # list_card_names = card_names.find_one({"_id": "card_names"})
    #
    # set_card_names = list_card_names['set_card_names']
    # print(len(set_card_names))
    card_names = cards.find({"oracle_text": {"$exists": True, "$ne": None}})
    # results = card_names.count()
    counter = 0
    # pprint(results)
    for card in card_names:
        card_name = card['_id']
        sim_cards = similar_cards(card_name, not_enough=False, force=True)
        sample_size = len(sim_cards)
        counter += 1

        if sample_size < 3:
            sim_cards = similar_cards(card_name, not_enough=True, force=True)
            print(counter, ' not enough ', card_name)
            sample_size = len(sim_cards)
            if sample_size < 3:
                print("for real not enough")
                sim_cards = similar_cards(card_name, last_chance=True, force=True)
        else:
            print(counter, ' :', card_name)


#

# update_all_sim_cards()


def delete_img_uris():
    cards = mongo.db.cards
    # cards = mongo.db.modere
    # cards.update_many({}, {"$rename": {"image_url": "image"}})
    # update_icara = cards.update_one({"_id": "Snapcaster Mage"},
    #                                 {"$unset": {"image_uri": 1}})

    # update_icara = cards.update_many({},
    #                                  {"$unset": {"image_uri": 1}})

    # result = cards.delete_many({'_id': {'$regex': '//', '$options': 'i'}})
    # cards.update_many({}, {"$set": {"mana_cost": ""}}, upsert=True, array_filters=None)
    # update_icara = cards.update_many({}, {"$set": {"oracle_text": ""}})
    # update_icara = cards.update_one({"_id": "Snapcaster Mage"},{"$set": {"mana_cost": "{1}{U}"}})
    #                                 {"$unset": {"image_uri": 1}})
    icara = cards.find({"_id": {'$regex': 'Snapcaster', '$options': 'i'}})
    for card in icara:
        pprint(card)
    # icara = cards.find_one({"_id": "Expansion // Explosion"})
    # return icara


# pprint(delete_img_uris())


# pprint(get_single_card_data_from_scryfall(card="Snapcaster Mage"))
# get_single_card_data_from_scryfall(card="Snapcaster Mage")
# pprint(get_single_card_data_from_scryfall(card="Jace, Vryn's Prodigy"))

def update_mana_costs():
    cards = mongo.db.cards
    list_card_names = mongo.db.list_card_names
    card_names = list_card_names.find_one({"_id": "card_names"})
    # card_info = cards.find()
    return True if "Valakut Awakening" in card_names['set_card_names'] else False
    # for card in card_names['set_card_names']:
    #     pprint(card)
    #     # if not card['mana_cost']:
    #     new_card_info = get_single_card_data_from_scryfall(card)
    #     # card_info['oracle_text'] = new_card_info['oracle_text']
    #     # card_info['flavor_text'] = new_card_info['flavor_text']
    #     # card_info['image'] = new_card_info['image']
    #     mana_cost = new_card_info['mana_cost']
    #     # card_info['image_uri'] = new_card_info['image_uri']
    #
    #     update_existing_decklist_url_in_db = cards.update_one({"_id": card},
    #                                                           {"$set":
    #                                                               {
    #                                                                   # "oracle_text": card_info['oracle_text'],
    #                                                                   # "flavor_text": card_info['flavor_text'],
    #                                                                   # "decklist_id": card_info['decklist_id'],
    #                                                                   # "image": card_info['image'],
    #                                                                   "mana_cost": mana_cost,
    #                                                                   # "image_uri": card_info['image_uri'],
    #                                                               },
    #                                                           },
    #                                                           upsert=True)
    #
    #     # upserts = [UpdateOne({'_id': x['_id']}, {'$set': x}, upsert=True) for x in existing_card_data]
    #     # upserts = [UpdateOne({'_id': x['_id']}, {'$setOnInsert': x}, upsert=True) for x in existing_card_data]
    #
    #     # insert_new_cards = cards.bulk_write(upserts)


# print(update_mana_costs())

def add_types():
    card_types_sets = mongo.db.card_types_sets
    # insert_list_card_names_in_db = card_types_sets.insert_one({"_id": "planeswalker"})
    # insert_list_card_names_in_db = card_types_sets.insert_one({"_id": "creature"})
    # insert_list_card_names_in_db = card_types_sets.insert_one({"_id": "land"})
    # insert_list_card_names_in_db = card_types_sets.insert_one({"_id": "sorcery"})
    # insert_list_card_names_in_db = card_types_sets.insert_one({"_id": "enchantment"})
    # insert_list_card_names_in_db = card_types_sets.insert_one({"_id": "artifact"})
    # insert_list_card_names_in_db = card_types_sets.insert_one({"_id": "instant"})
    # insert_list_card_names_in_db = card_types_sets.insert_one({"_id": "sideboard"})
    # insert_list_card_names_in_db = card_types_sets.insert_one({"_id": "other"})


#
#
# add_types()
# pprint(get_card_data_from_local_file("Pact of Negation"))
# scrape_card_data()
# pprint(get_single_card_data_from_scryfall("Pact of Negation"))
# gen_new_cards(card_type_filters=['planeswalker', 'land',
#                                  # 'enchantment', 'instant',
#                                  # 'artifact', 'tribal',
#                                  'sorcery', 'creature', ])

# scrape_card_data()
# pprint(is_there_new_data())
