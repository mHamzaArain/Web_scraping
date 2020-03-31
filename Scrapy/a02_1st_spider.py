# -*- coding: utf-8 -*-
import scrapy


class A021stSpiderSpider(scrapy.Spider):
    name = '02_1st_spider'
    start_urls = ['http://quotes.toscrape.com/random']

    def parse(self, response):
        self.log(f'Got response from {response.url}')

        item = {
            'author': response.css('.author::text').get(),
            'quote' : response.css('.text::text').get(),
            'tags'  : response.css('.tag::text').getall()
        }
        
        yield item