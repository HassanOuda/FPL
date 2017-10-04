import requests
import json
import pandas as pd
import plotly.offline as py
import plotly.figure_factory as ff

#GET GENERAL FPL DATA
fpl_data = requests.get('https://fantasy.premierleague.com/drf/bootstrap-static').json()
#for i, phase in enumerate(fpl_data['phases']):
#	print (fpl_data['phases'][i])

#GET SPECIFIC LEAGUE DATA
fpl_league = requests.get('https://fantasy.premierleague.com/drf/leagues-classic-standings/16873').json()

#print(fpl_league["league"]["name"])

#EXTRACT MEMBERS OF LEAGUE
members = []
for i in (fpl_league['standings']['results']):
	members.append(i)


memberDetails = [] #GET MORE DETAILS OF THOSE MEMBERS
gameweek = []
transfers = [] #NEW TRANSFER INFO
transferHist = [] #TRANSFER HISTORY
chips = [] # CHIPS INFORMATION
wildcard = [] #PLAYED WILDCARDS
for member in (members):
	memberDetails.append(requests.get('https://fantasy.premierleague.com/drf/entry/'+str(member['entry'])).json()['entry'])
	gameweek.append(requests.get('https://fantasy.premierleague.com/drf/entry/'+str(member['entry'])+'/event/'+str(fpl_data['current-event'])+'/picks').json()['entry_history'])
	transfers.append(requests.get('https://fantasy.premierleague.com/drf/entry/'+str(member['entry'])+'/transfers').json()['entry'])
	transferHist.append(requests.get('https://fantasy.premierleague.com/drf/entry/'+str(member['entry'])+'/transfers').json()['history'])
	chips.append(requests.get('https://fantasy.premierleague.com/drf/entry/'+str(member['entry'])+'/history').json()['chips'])
	wildcard.append(requests.get('https://fantasy.premierleague.com/drf/entry/'+str(member['entry'])+'/transfers').json()['wildcards'])



#GENERATE TABLE
columns = ['rank','entry_name', 'player_name', 'player_region_name','total','summary_overall_rank','total_transfers','bank','value','chips','public_transfers']
good_columns = ['Rank','Team Name', 'Player Name', 'Region','Total','Overall Rank','Total Transfers','Old Bank','New Bank','Old Value','New Value','Chips Played','Public Transfers']
data = []
for i,row in enumerate(members):
	selected_row = []
	gw = gameweek[i]
	details = memberDetails[i]
	wc = wildcard[i]
	chip_length = len(chips[i])
	transfer_count = 0
	for j, r in enumerate(transferHist[i]):
		if wc and wc[0].get('event') == r.get('event'):
			transfer_count += 0
		else:
			transfer_count += 1
	for item in columns:
		if item in row:
			selected_row.append(row[item])	
		elif item in details:
			if item == 'bank':
				selected_row.append(gw[item]/10.0)
				selected_row.append(details[item]/10.0)
			elif item == 'value':
				selected_row.append(gw[item]/10.0)
				selected_row.append(details[item]/10.0)				
			else:
				selected_row.append(details[item])
		elif item == 'chips':
			selected_row.append(chip_length)
		else:
			selected_row.append(transfer_count)
	data.append(selected_row)

#print(data)

league_results = pd.DataFrame(data, columns=good_columns)
	
table = ff.create_table(league_results)
#py.init_notebook_mode(connected=True)
py.plot(table, filename='simple_table.html')

#with open('results.txt', 'w') as outfile:  
#    json.dump(members, outfile)

#for i, player in enumerate(fpl_data['elements']):
#	fpl_data['elements'][i]['history'] = requests.get('https://fantasy.premierleague.com/drf/element-summary/' + str(player['id'])).json()
