# -*- coding: utf-8 -*-
import scrapy


class A09DealerProjSpider(scrapy.Spider):
    name = '09_dealer_proj'
    allowed_domains = ['www.machinerypete.com']
    start_urls = ['https://www.machinerypete.com/dealerships/search']

    def parse(self, response):
        links = response.css('div .col-xs-12.center-align > a::attr(href)').getall() 
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(url=link, callback=self.parse_1)
        
    def parse_1(self, response):
        links = response.css(
            'li[style="font-size: 0.8em;"] > a::attr(href)').getall()  
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(url=link, callback=self.parse_2)
            
    def parse_2(self, response):
        title = response.css('h1[style="margin-top: 5px;"]::text').get()
        
        contact_lst = response.css('div .store-header:contains("Contact") ~ div::text').getall() 
        contact_lst = [x for x in contact_lst if x!='\n']
        contact =', '.join(contact_lst)
        
        address_lst = response.css('div .store-header:contains("Address") ~ div::text').getall()
        address_lst = [x for x in contact_lst if x!='\n']
        address = ', '.join(address_lst)
        
        yield {
            'title': title,
            'contact': contact,
            'address': address
        }