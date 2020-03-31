# -*- coding: utf-8 -*-
import scrapy
import regex


class NflProjSpider(scrapy.Spider):
    name = 'nfl_proj'
    start_urls = ['http://www.nfl.com/players/search?category=lastName&filter=A&playerType=historical']

    def parse(self, response):
        # # for 1 player to check bugs
        # player = response.css('#result a::attr(href)').get()
        # link = response.urljoin(player)
        # yield scrapy.Request(url=link, callback=self.parse_profiles) 
        
        all_players = response.css('#result a::attr(href)').getall()         
        for player in all_players:
            link = response.urljoin(player)
            yield scrapy.Request(url=link, callback=self.parse_profiles)
        
        # Pagination here 
        next_page = response.css('a:contains("next")::attr(href)').get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)
        
    def parse_profiles(self, response):
        link = response.urljoin('gamelogs')
        yield scrapy.Request(url=link, callback=self.parse_game_log)
        
    def parse_game_log(self, response):
        player_name = response.css('.player-name::text').get() 
        current_year_game_log = response.css('select option[selected="selected"]::text').get()
        for season in response.css('table'):
            # process each table 1 by 1
            season_name =  response.css('thead > tr > td ::text').get()
            
            # Process row 1 by 1 
            for week in response.css('tbody > tr'):
                second_td = week.css('td:nth-child(2)::text').get()
                
                if (second_td is None) or ('TOTAL' in second_td):
                    continue
                
                else:    
                    wk = week.css('td:nth-child(1)::text').get()
                    game_date = week.css('td:nth-child(2)::text').get()
                    opp = week.css('td:nth-child(3) a:last-child::text').get()
                    g = week.css('td:nth-child(5)::text').get()
                    gs = week.css('td:nth-child(6)::text').get()
        
                    items = {
                        'plyer_name' : self.cleanup_string(player_name),
                        'year' : current_year_game_log, 
                        'season_name' : season_name,
                        'wk' : wk,
                        'game_date' : game_date,
                        'opp' : self.cleanup_string(opp),
                        'g' : g,
                        'gs' : gs,
                        'urk': response.url
                    }
                    
                    yield items
                
    def cleanup_string(self,string):
        '''/n,/r,/t, @ replace with no character'''
        if string:
            return regex.sub(r'[\\n\\t\\r@]', '', string).strip()