import steamspypi as s
import requests
import json
import time
import datetime
import asyncio
from howlongtobeatpy import HowLongToBeat as hltb
from tqdm import tqdm

id = '76561198809936084'
key = '9437477ABC2F494C082FF6605AD880D2'

def get_games(id, key, write=False):
    r = requests.get(f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={id}&format=json')
    if (r.status_code == requests.codes.ok):
        if write == True:
            with open('games.json', 'w') as f:
                f.write(r.json())
        return r.json()
    else:
        return 404

def get_appids(games, write=False):
    for game in games:
        appids = f"{appids}{game['appid']}\n"
    if write == True:
        with open('id_list.csv', 'w') as f:
            f.write(appids)
    return appids

# todo: hltb
def howlong(name):
    try:
        encode = name.encode("ascii", "ignore")
        parsed_name = encode.decode()
        results = hltb(0.2).search(parsed_name)
        hltb_dict = {"gameplay_main": "", "gameplay_main_extra": "", "gameplay_completionist": ""}
        hltb_dict["gameplay_main"] = results[0].gameplay_main
        hltb_dict["gameplay_main_extra"] = results[0].gameplay_main_extra
        hltb_dict["gameplay_completionist"] = results[0].gameplay_completionist
        print(hltb_dict)
        print(results[0].game_name)
        return hltb_dict
    except:
        return None
    # self.game_name = None
    # self.gameplay_main = -1
    # self.gameplay_main_extra = -1
    # self.gameplay_completionist = -1

def get_all_game_details(id='', key='',file='gamedetails.json', rate=3, parsed=False):
    loop = 0
    r = get_games(id, key)
    total = r['response']['game_count']
    games = r['response']['games']
    failed = []
    parse = ("steam_appid", "required_age", "is_free","steam_appid","required_age","is_free","detailed_description","about_the_game","short_description","supported_languages","header_image","website","developers","publishers","price_overview","packages","package_groups","metacritic","categories","genres","screenshots","recommendations","achievements","release_date","support_info","background","background_raw","content_descriptors")
    
    for game in tqdm(games):
        loop += 1
        print(f"Loop {loop} of {total}.")
        try:
            game_json = get_app_json(game['appid'])
            appid = str(game['appid'])
            print(get_name(game['appid'], game_json))

            while game_json == 404:
                game_json = get_app_json(game['appid'])
            if parsed==True:
                for k in parse:
                    game_json[appid]['data'].pop(k, None)
                game_json.update(howlong(game_json[appid]['data']['name']))
            with open(file, 'a') as f:
                json.dump(game_json, f)
                f.write(',')

            time.sleep(rate)
        except:
            failed.append(appid)
            print(f"{appid} failed.")
            continue
    print(f"Failed to add: {failed}")

def get_app_json(appid):
    print(f"Getting json for {appid}")
    r = requests.get(f'https://store.steampowered.com/api/appdetails/?appids={appid}')
    if (r.status_code == requests.codes.ok):
        return r.json()
    else:
        print(f"Status: {r.status_code}")
        return 404

def get_name(appid, json=''):
    if json != '':
        return json[f'{appid}']['data']['name']
    else:
        game = get_app_json(appid)
        if game == 404:
            return 0
        else:
            name = game[f'{appid}']['data']['name']
            print(f"get_name: {name}")
            return name

get_all_game_details(id, key, file="parsed_games.json", rate=1, parsed=True)