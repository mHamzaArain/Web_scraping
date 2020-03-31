# -*- coding: utf-8 -*-
import scrapy


class A031stExcerciseSpider(scrapy.Spider):
    name = '03_1st_excercise'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Python_(programming_language)']

    def parse(self, response):
        self.log(f'Got response from {response.url}')

        item = {
        'content':  response.css('.toclevel-1 > a .toctext::text').getall()      
        }
    
        yield item