import json

with open('data/id_details.json', 'r') as f:
    games = json.loads(f.read())
#appid = list(games['0'].keys())[0]
#print(appid)
cat1 = 'platforms'
cat2 = 'linux'
#loc = ['data'][cat1][cat2]
for pos in games:
    print(pos)
    for appid in games[pos]:
        print('Linux?: '+ games.index('linux'))
        #print(appid['data'])