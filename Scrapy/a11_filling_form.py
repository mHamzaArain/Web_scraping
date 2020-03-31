# -*- coding: utf-8 -*-
import scrapy


class A11FillingFormSpider(scrapy.Spider):
    name = 'a11_filling_form'
    login_url = 'http://quotes.toscrape.com/login'
    start_urls = [login_url]
    
    def parse(self, response):
        
        # Extraact csrf token(This code changes every time after refreashing page)
        token = response.css('input[name="csrf_token"]::attr(value)').get()
        
        # Python dict to filling form essentials in name field
        credentials = {
            'csrf_token' : token,
            'username': 'abc',
            'password': 'abc', 
        }
        
        # Submit a form
        yield scrapy.FormRequest(url=self.login_url, callback=self.parse_quotes_url)

    def parse_quotes_url(self, response):
        yield scrapy.Request(url="http://quotes.toscrape.com/", callback=self.parse_quotes)
        
    def parse_quotes(self, response):
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
            request = scrapy.Request(url=next_page_url, callback=self.parse_quotes) 
            yield request           
            
