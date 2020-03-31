# -*- coding: utf-8 -*-
import scrapy
from ..items import AmazonItem
import regex

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    start_urls = [r'https://www.amazon.com/s?bbn=9&rh=n%3A283155%2Cn%3A%211000%2Cn%3A9%2Cp_n_publication_date%3A1250226011&dc&fst=as%3Aoff&qid=1585192509&rnid=1250225011&ref=lp_9_nr_p_n_publication_date_0']
    next_page = 2
    
    def parse(self, response):
        items = AmazonItem()
        
        product_names = response.css('.a-color-base.a-text-normal::text').extract()
        # Need to remove unwanted chars in author name
        product_authors = response.css('.a-color-secondary .a-size-base+ .a-size-base::text').extract()
        product_authors = [self.cleanup_string(author) for author in product_authors]  
        product_prices = response.css('.a-color-secondary .a-color-base::text').extract()
        product_imageLinks = response.css('.s-image::attr(src)').extract()
        
        items['product_names'] = product_names
        items['product_authors'] = product_authors
        items['product_prices'] = product_prices
        items['product_imageLinks'] = product_imageLinks
        
        for each in range(len(product_names)):
            try:
                yield {
                    'product' :items['product_names'][each],
                    'author': items['product_authors'][each],
                    'price' : items['product_prices'][each],
                    'image_urk' : items['product_imageLinks'][each]
                }
            
                next_page_url = f'https://www.amazon.com/s?i=stripbooks&bbn=9&rh=n%3A283155%2Cn%3A1000%2Cn%3A9%2Cp_n_publication_date%3A1250226011&dc&page={self.next_page}&fst=as%3Aoff&qid=1585306004&rnid=1250225011&ref=sr_pg_{self.next_page}'
            
                if next_page_url <= 75:
                    request = scrapy.Request(url=next_page_url, callback=self.parse) 
                    yield request 
                     
            except:
                continue
            
            
    def cleanup_string(self,string):
        '''/n,/r,/t, @ replace with no character'''
        if string:
            return regex.sub(r'[\\n\\t\\r@]', '', string).strip()