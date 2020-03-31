# -*- coding: utf-8 -*-
import scrapy


class VetSpider(scrapy.Spider):
    name = 'vet'
    start_urls = ['http://www.findalocalvet.com/Find-a-Veterinarian.aspx']

    def parse(self, response):
        
        major_cities = response.css('#SideByCity .itemresult a::attr(href)').getall()  
        for major_city in major_cities:
            major_city = response.urljoin(major_city)
            yield scrapy.Request(url=major_city, callback=self.parse_major_city)
            
    def parse_major_city(self, response):
        hospitals = response.css('.org::attr(href)').getall()    
        for hospital in hospitals:
            hospital = response.urljoin(hospital)
            yield scrapy.Request(url=hospital, callback=self.parse_hospital_info)
        
        # Pagination here
        next_page = response.css('a.dataheader:contains("Next")::attr(href)').getall() 
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse_major_city)
        
    def parse_hospital_info(self, response):
        hospital_name = response.css('h1 ::text').get()
        phone = response.css('.Phone::text').get()     
        address = ", ".join(response.css('.adr span::text').getall()) ; address += '.' 
        
        info = {
            'hospital_name': hospital_name,
            'phone' : phone, 
            'address' : address,
            'url' : response.url
        }
        
        yield info
        
