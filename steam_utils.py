import requests
import json
import time
from howlongtobeatpy import HowLongToBeat as hltb
from tqdm import tqdm
import string
from bs4 import BeautifulSoup as bs4


def get_games(id, key, write=False):
    r = requests.get(
        f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={id}&format=json'
    )
    if (r.status_code == requests.codes.ok):
        if write == True:
            with open('games.json', 'w') as f:
                json.dump(r.json(), f, indent=4)
        return r.json()
    else:
        return 404


def get_appids(games, write=False):
    appids = ''
    for game in games:
        appids = (f"{appids}{game['appid']}\n")
    if write == True:
        with open('id_list.csv', 'w') as f:
            f.write(appids)
    return appids


def remove_unicode(x):
    encode = str(x).encode("ascii", "ignore")
    return encode.decode()


def strip_tags(s):
    soup = bs4(s, features="html.parser")
    return soup.get_text()


def strip_req_tags(s, id, req='pc_requirements'):
    s_index = s[id]['data']
    if req in s_index:
        if 'minimum' in s_index[req]:
            s_index[req]['minimum'] = remove_unicode(
                strip_tags(s_index[req]['minimum'])).strip().replace(
                    '\n', ' ')
        if 'recommended' in s_index[req]:
            s_index[req]['recommended'] = remove_unicode(
                strip_tags(s_index[req]['recommended'])).strip().replace(
                    '\n', ' ')
    return s


def clean_json(j, id):
    parse = ("steam_appid", "required_age", "is_free", "detailed_description",
             "about_the_game", "short_description", "supported_languages",
             "website", "developers", "publishers", "price_overview",
             "packages", "package_groups", "metacritic", "genres",
             "screenshots", "recommendations", "achievements", "release_date",
             "support_info", "background", "background_raw",
             "content_descriptors", "movies", "demos", "categories",
             "legal_notice", "reviews", "drm_notice", "mac_requirements", "dlc")

    j[id].pop("success", None)
    j[id]['data']['platforms'].pop('mac', None)
    for k in parse:
        try:
            j[id]['data'].pop(k, None)
        except:
            print(f"Failed to pop {k}")

    j = strip_req_tags(j, id)
    j = strip_req_tags(j, id, 'linux_requirements')

    return j


def clean_name(name):
    parsed_name = remove_unicode(name)
    parsed_name = parsed_name.translate(
        str.maketrans(string.punctuation,
                      ' ' * len(string.punctuation))).lower().replace(
                          '  ', ' ')
    return parsed_name


def howlong(name, fail_file='failures.txt'):
    parsed_name = clean_name(name)
    print("Parsed:" + parsed_name)

    results = hltb().search(str(parsed_name))
    try:
        results[0]
    except IndexError:
        name_array = parsed_name.split()
        length = len(name_array)
        print('Gonna try to find it.')

        sep = ' '
        while length - 1 > 0:
            length -= 1
            print(name_array[:length])
            results = hltb().search(sep.join(name_array[:length]))
            if 0 <= 0 < len(results):
                break

    hltb_dict = {
        "gameplay_main": "-1",
        "gameplay_main_extra": "-1",
        "gameplay_completionist": "-1"
    }

    if 0 <= 0 < len(results):
        hltb_dict["gameplay_main"] = remove_unicode(results[0].gameplay_main)
        hltb_dict["gameplay_main_extra"] = remove_unicode(
            results[0].gameplay_main_extra)
        hltb_dict["gameplay_completionist"] = remove_unicode(
            results[0].gameplay_completionist)

        print('howlong: ' + results[0].game_name)
        return hltb_dict
    else:
        print(f"nothin from hltb")
        return hltb_dict


def get_app_json(appid):
    print(f"\nGetting json for {appid}")
    r = requests.get(
        f'https://store.steampowered.com/api/appdetails/?appids={appid}')
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
            return name

def get_all_game_details(id,
                         key,
                         file='gamedetails.json',
                         rate=3,
                         parsed=False,
                         fail_file='failures.txt'):

    r = get_games(id, key)
    games = r['response']['games']
    failed = []
    loop = 0
    game_dict = {}
    for game in tqdm(games):
        try:
            game_json = get_app_json(game['appid'])
            appid = str(game['appid'])
            game_name = game_json[appid]['data']['name']
            playtime = str(game['playtime_forever'])

            print(game_name)

            while game_json == 404:
                game_json = get_app_json(game['appid'])

            if parsed == True:
                clean_json(game_json, appid)

            hltb_result = howlong(game_name, fail_file)
            game_json[appid]['data']['playtime'] = playtime
            if hltb_result != None:
                game_json[appid]['data']['howlongtobeat'] = hltb_result

            game_dict[loop] = game_json
            print(loop)
            loop += 1
            time.sleep(rate)

        except Exception as e:
            failed.append(appid)
            print(f"FAIL: {appid} failed.\n{e}")
            continue

    with open(file, 'a') as f:
        json.dump(game_dict, f, indent=4)

    with open(fail_file, 'a') as f:
        for fail in failed:
            f.write(fail + ', ')

