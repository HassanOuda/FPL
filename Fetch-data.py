import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
fpl_data = requests.get('https://fantasy.premierleague.com/drf/bootstrap-static').json()
fpl_details = []
for i, player in enumerate(fpl_data['elements']):
    a_dict = {'player_id': str(player['id'])}
    fpl_details.append(requests.get('https://fantasy.premierleague.com/drf/element-summary/' + str(player['id'])).json())
    fpl_details[i].update(a_dict)

with open('players.json','w') as outfile:
    json.dump(fpl_data['elements'],outfile)
with open('positions.json','w') as outfile:
    json.dump(fpl_data['element_types'],outfile)
with open('player_details.json','w') as outfile:
    json.dump(fpl_details,outfile)
	
