import os
import steam_utils
import config
from bs4 import BeautifulSoup as bs4
import json

key = config.key
id = config.my_id
file = 'cody'

def test():
    with open("data/full_entry.json") as f:
        j = json.load(f)

    clean = steam_utils.clean_json(j, '240')
    print(clean)

    with open("data/clean_entry.json", 'w') as f:
        f.write(json.dumps(j, indent=4))

#steam_utils.get_games(id, key, write=True)
steam_utils.get_all_game_details(id, key, rate=1, file=file+'_details.json', fail_file=file+'_fail.txt',parsed=True)