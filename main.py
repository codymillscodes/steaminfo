import os
import steam_utils
import detail_utils as d
import json
import time
import config

id2 = config.levi
id = config.my_id
key = config.key

key = key
id = id
file = 'out/id_'
infile = 'data/id_details.json'
gpu = 'RX 580 4GB'
cpu = 'Ryzen 5 3600'
def test():
    with open("data/full_entry.json") as f:
        j = json.load(f)

    clean = steam_utils.clean_json(j, '240')
    print(clean)

    with open("data/clean_entry.json", 'w') as f:
        f.write(json.dumps(j, indent=4))

# with open(infile) as f:
#     j = json.load(f)
# for x in j:
#     for appid in j[x]:
#         d.write_to_file(f"{d.pcgw_test(appid, j[x][appid]['data']['name'])},", 'id_newspecs.txt', append='a')
#         time.sleep(1)

#print(d.pcgw_test(240))
#d.write_to_file(d.get_controller_support(j), 'id_controller.txt')
#d.get_image(j)
#d.write_to_file(d.get_playtime(j, 'main'), 'out/id2_playtime.txt')
#d.write_to_file(d.get_platforms(j), file=file+'linux.txt')
#steam_utils.get_games(id, key, write=True)
#steam_utils.get_all_game_details(id, key, rate=1, file=file+'details.json', fail_file=file+'_fail.txt',parsed=True)