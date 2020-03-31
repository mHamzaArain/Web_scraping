import json 
import csv
import os

# To change path to store csv files in it 
os.chdir('/home/hamza/Desktop/Scrapy/Projects/nba/player_profile/Profiles')

# To open json file
filename = '/home/hamza/Desktop/Scrapy/Projects/nba/player_profile/nba_regular_stats.json'
f = open(filename, 'r')
js_data = json.load(f)

def player_data(name):
    '''Extract all data related to a relavent player in list'''
    player = []
    for dic in js_data:
        if name == dic["name"]:
            player.append(dic)
    return player

 
def csv_file(name, dic):
    '''Make csv file of a relavent player''' 
    File = f'{name}.csv'
    # if os.path.exists(File):
    with open(File, 'w', newline = '') as wf:
        csvWrite = csv.DictWriter(wf, fieldnames = ['name', 'year', 'team', 'games_played', 'ftm', 'fta', 'tpa']) #write
        csvWrite.writeheader()
        for row in dic: 
            print(row)
            csvWrite.writerow(
                {
                    'name' :  row['name'],
                    'year' : row['year'],
                    'team' : row['teamId'],
                    'games_played' : row['games_played'],
                    'ftm' : row['ftm'],
                    'fta' : row['fta'],
                    'tpa' : row['tpa'],
                    
                }
            )
    # else:
    #     None
                    
def main_proc():  
    '''This eliminate player after extraction of its data & whole relavent produres'''         
    elimination = []
    for dic1 in js_data:
        name = dic1["name"]
        if name not in elimination:
            elimination.append(name)
            lst2 = player_data(name)
            csv_file(name, lst2)
                    
        
        
main_proc()