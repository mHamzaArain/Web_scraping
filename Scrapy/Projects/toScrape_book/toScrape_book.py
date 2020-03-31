# -*- coding: utf-8 -*-
import scrapy
import regex

class ToscrapeBookSpider(scrapy.Spider):
    name = 'toScrape_book'
    start_urls = ['http://books.toscrape.com/catalogue/page-{}.html'.format(i) for i in range(1, 150+1)]

    def parse(self, response):
        titles =  response.css('.product_pod a::attr(title)').getall() 
        prices =  response.css('.price_color::text').getall()  
        # To remove extra chars from stock 
        stocks_availibility = [self.cleanup_string(i) for i in response.css('.availability::text').getall() ]
        
        # 'star-rating Five'
        ratings = [i.replace('star-rating ', '') for i in response.css(' .product_pod > p::attr(class)').getall() ]
        imageLinks = [response.urljoin(i) for i in response.css('img::attr(src)').getall()] 
        
        for each in range(len(titles)):
            yield {
                'title': titles[each],
                'price':prices[each],
                'stocks_availibility':stocks_availibility[each],
                'rating': ratings[each],
                'imageLinks': imageLinks[each]
            }   
        
    def cleanup_string(self,string):
        '''/n,/r,/t, @ replace with no character'''
        if string:
            string = regex.sub(r'[\n\t\r@]', '', string).strip()
            if string == '':
                return "In stack"
            return string