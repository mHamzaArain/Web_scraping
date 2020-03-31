# -*- coding: utf-8 -*-
import scrapy


class A04ScrapeitemListSpider(scrapy.Spider):
    name = '04_scrapeItem_list'
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        self.log(f'Got response from {response.url}')
        quotes = response.css('.quote')
        for quote in quotes:    
            item = {
                'author': quote.css('.author::text').get(),
                'quote' : quote.css('.text::text').get(),
                'tags'  : quote.css('.tag::text').getall()  
            }
    
            yield item
