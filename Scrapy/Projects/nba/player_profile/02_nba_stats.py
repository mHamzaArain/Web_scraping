# -*- coding: utf-8 -*-
import scrapy
import json
import pandas as pd

class playerObject_List():
    def __init__(self):
        self.dataset = pd.read_csv('/home/hamza/Desktop/Scrapy/Projects/nba/nba.csv',
                                   squeeze=True, usecols=['player_id', 'name']) 
        self.ids   = self.dataset.iloc[:, [0]].values.reshape(1,-1).tolist()
        self.names = self.dataset.iloc[:, [1]].values.reshape(1,-1).tolist()
        
    def idsList(self):
        return self.ids[0]
    
    def namesList(self):
        return self.names[0]
         

class NbaStatsPySpider(scrapy.Spider):
    name = 'nba_stats'
    players = playerObject_List()
    names, ids = players.namesList(), players.idsList()
    
    start_urls = [f'https://data.nba.net/prod/v1/2019/players/{id}_profile.json' for id in ids]
    
    def parse(self, response):
        str_data = response.text
        json_data = json.loads(str_data)
        for region in json_data['league'].keys(): 
            for counter, data in enumerate(json_data['league'][region]["stats"]["regularSeason"]["season"]): 
                yield {
                    'name': self.names[counter],
                    'year' : data["seasonYear"],
                    'teamId' : self.teamID_code(json_data['league'][region]["teamId"]),
                    'games_played' : data["teams"][0]["gamesPlayed"], 
                    'ftm' : data["teams"][0]["ftm"], 
                    'fta' : data["teams"][0]["fta"], 
                    'tpa' : data["teams"][0]["tpa"],
                }
                
    def teamID_code(self, code):
        filename = '/home/hamza/Desktop/Scrapy/Projects/nba/teamId.json'
        with open(filename, 'r') as data:    
            teams = json.load(data)
            for team in teams:
                if str(team["teamId"]).strip() != str(code).strip():
                    continue
                return  f'{team["teamName"]} ({team["abbreviation"]})'
