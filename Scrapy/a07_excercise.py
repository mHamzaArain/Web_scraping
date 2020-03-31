# -*- coding: utf-8 -*-
import scrapy


class A07ExcerciseSpider(scrapy.Spider):
    name = '07_excercise'
    start_urls = ['https://scrapeit.home.blog/']

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
            
        next_page_url = response.css('.next.page-numbers ::attr(href)').get()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            request = scrapy.Request(url=next_page_url, callback=self.parse) 
            yield request           
            
