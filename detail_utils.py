#  requirements 
import requests
import json
from bs4 import BeautifulSoup as bs4
import steam_utils
def write_to_file(result, file, append='w'):
    try:
        with open(file, append) as f:
            #for x in result:
               # f.write(str(x) + '\n')
            f.write(result)
    except:
        print('ruh roh')
def get_controller_support(j):
    return get_category(j, 'controller_support', val=True)

def get_image(j):
    return get_category(j, 'header_image', val=True)

def get_playtime(j):
    return get_category(j, 'playtime', val=True)
            
def get_platforms(j, platform='linux'):
    if platform == 'windows':
        return get_category(j, 'platforms', 'windows')
    else:
        return get_category(j, 'platforms', 'linux')
def hltb(j, gp='all'):
    if gp == 'all':
        return get_category(j, 'howlongtobeat', val=True)
    else:
        return get_category(j, 'howlongtobeat', cat2=f"gameplay_{gp}", val=True)
def get_category(j, cat1, cat2='', val=False):
    results = []
    for pos in j:
        for appid in j[pos]:
            name = j[pos][appid]['data'].get('name')
            if cat2 == '':
                x = j[pos][appid]['data'].get(cat1)
                if val:
                    results.append((name, x))
                    print(f"{name}\n{x}\n")
                else:
                    results.append(name)
                    print(f"{name}")
            else:
                x = j[pos][appid]['data'].get(cat1).get(cat2)
                #if x == True:
                if cat1 == 'platforms':
                    if x == True:
                        if val:
                            results.append((name, x))
                            print(f"{name}\n{x}\n")
                        else:
                            results.append(name)
                            print(f"{name}")
                else:
                    if val:
                        results.append((name, x))
                        print(f"{name}\n{x}\n")
                    else:
                        results.append(name)
                        print(f"{name}")
    return results
def build_pcgw_json(sr):
    keys = ['minCPU', 'minCPU2', 'minRAM', 'minGPU', 'minGPU2', 'minGPU3', 'recCPU', 'recCPU2', 'recRAM', 'recGPU', 'recGPU2', 'recGPU3']
    json = {}
    for x in sr:
        for key in keys:
            if key in x:
                val = x[x.index(',')+1:]
                json[key] = val
    print(json)
    return json

# https://www.pcgamingwiki.com/w/api.php?action=cargoquery&tables=Infobox_game&fields=Infobox_game._pageName=System_Requirements&where=Infobox_game.Steam_AppID%20HOLDS%20%22{appid}%22&format=jsonfm
def pcgw_test(appid, name):
    r = requests.get(f"https://www.pcgamingwiki.com/w/api.php?action=cargoquery&tables=Infobox_game&fields=Infobox_game._pageID%3DPageID%2CInfobox_game.Steam_AppID&where=Infobox_game.Steam_AppID%20HOLDS%20%22{appid}%22&format=json")
    if (r.status_code == requests.codes.ok):
        soup = bs4(r.text, 'html5lib')
        try:
            pid = json.loads(soup.body.contents[0])['cargoquery'][0]['title']['PageID']
            r = requests.get(f"https://www.pcgamingwiki.com/w/api.php?action=parse&format=json&pageid={pid}&prop=wikitext")
            s = '==System requirements=='
            j = r.text
            joshi = {}
            if s in j:
                pos = j.find(s)
                chunk = j[pos+23:]
                chunk = chunk.replace('\\n', '\n').replace('{', '').replace('}', '').replace('|', '').replace('=', ',')
                if 'System requirements' in chunk:
                    chunk = chunk.replace('System requirements', '')
                if '''References"''' in chunk:
                    chunk = chunk.replace('''References"''', '')
                if "References" in chunk:
                    chunk = chunk.replace('References','')
                if '''GOG.com Enhancement Project"''' in chunk:
                    chunk = chunk.replace('''GOG.com Enhancement Project"''', '')
                chunksplit = chunk.splitlines()
                while '' in chunksplit:
                    chunksplit.pop(chunksplit.index(''))

                joshi['appid'] = appid
                joshi['name'] = name
                joshi['specs'] = build_pcgw_json(chunksplit)
                return json.dumps(joshi, indent=4)#" ".join(chunksplit)
            else:
                return 404
        except:
            print(soup)