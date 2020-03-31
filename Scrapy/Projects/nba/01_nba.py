# -*- coding: utf-8 -*-
import scrapy
import json 


class NbaSpider(scrapy.Spider):
    name = 'nba'
    # player_stats_link = "https://data.nba.net/prod/v1/2019/players/{}_profile.json"
    start_urls = ['http://data.nba.net/prod/v1/2019/players.json']

    def parse(self, response):
        str_data = response.text
        json_data = json.loads(str_data)
        for region in json_data['league'].keys(): # dictionary
            players = json_data['league'][region]
            for player in players: # list
                yield {
                    'player_id' : player["personId"],
                    'name' : player["firstName"] + ' ' +  player["lastName"],
                    'team' : self.teamID_code(player["teamId"]),
                    'active' : player["isActive"],
                    'country' : player["country"],
                    'debut' : player["nbaDebutYear"],
                    'experience' :  player["yearsPro"],
                    'hight' : f'{player["heightFeet"]}ft {player["heightInches"]}in',
                    'weight' : f'{player["weightKilograms"]} kg',
                    'birth_date' : player["dateOfBirthUTC"],
                }
                
    def teamID_code(self, code):
        filename = 'teamId.json'
        with open(filename, 'r') as data:    
            teams = json.load(data)
            for team in teams:
                if str(team["teamId"]).strip() != str(code).strip():
                    continue
                return  f'{team["teamName"]} ({team["abbreviation"]})'
