# -*- coding: utf-8 -*-
import scrapy


class A052ndExcerciseSpider(scrapy.Spider):
    name = '05_2nd_excercise'
    start_urls = ['http://scrapeit.home.blog/']

    def parse(self, response):
        self.log(f'Got response from {response.url}')
        blogs = response.css('article') 
        for blog in blogs:
            item = {
                'title': blog.css('.entry-title a::text').get(),
                'paragraph': blog.css('p:nth-child(1)::text').get(),
                'author': blog.css('.url.fn.n::text').get(),
                'published_date': blog.css('.entry-date.published::text').get(),
                'topic': blog.css('.cat-links a::text').getall(),  # Logical err: Not separate for single title  
                'tags': blog.css('.tags-links a::text').getall()   # Logical err: Not separate for single title
                }
    
            yield item
