# -*- coding: utf-8 -*-
import scrapy


class A08PgDetailListSpider(scrapy.Spider):
    name = '08_pg_detail_list'
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):        
        links = response.css('.quote span a::attr(href)').getall()
        for link in links:
            complete_link = response.urljoin(link)             
            yield scrapy.Request(url=complete_link, callback=self.parse_author)
        
        next_page_url = response.css('.next.page-numbers ::attr(href)').get()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            request = scrapy.Request(url=next_page_url, callback=self.parse) 
            yield request      
            
            
    def parse_author(self, response):
        yield {
            'author': response.css('.author-title::text').get(),
            'birth_data': response.css('.author-born-date::text').get(),
            'born_location': response.css('.author-born-location::text').get()
        }
