# -*- coding: utf-8 -*-
import scrapy


class A06PaginationSpider(scrapy.Spider):
    name = '06_pagination'
    start_urls = ['http://quotes.toscrape.com/']

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
            
        next_page_url = response.css('li.next > a::attr(href)').get()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            request = scrapy.Request(url=next_page_url, callback=self.parse) 
            yield request           
            
