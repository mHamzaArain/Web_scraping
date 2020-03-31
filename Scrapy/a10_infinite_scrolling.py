# -*- coding: utf-8 -*-
import scrapy
import json

class A10InfiniteScrollingSpider(scrapy.Spider):
    name = 'a10_infinite_scrolling'
    api = 'http://quotes.toscrape.com/api/quotes?page={}'
    start_urls = [api.format(1)]
    
    def parse(self, respones):
        str_data = respones.text
        json_data = json.loads(str_data)
        quotes_lst = json_data["quotes"]
        for quote in quotes_lst:
            item = {
                'name' : quote['author']['name'],
                'quote' : quote['text'],
                'tags' : ', '.join(quote['tags']) 
            }
            
            yield item
        
        if json_data['has_next']:
            next_page = json_data['page'] = 1  
            yield scrapy.Request(url=self.api.format(next_page), callback=self.parse)    