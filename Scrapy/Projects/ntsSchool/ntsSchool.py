# -*- coding: utf-8 -*-
import scrapy
import json

class NtsschoolSpider(scrapy.Spider):
    name = 'ntsSchool'
    start_urls = ['http://directory.ntschools.net/#/schools']
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'BIGipServerdirectory.ntschools.net_443.app~directory.ntschools.net_443_pool=747307530.20480.0000',
        'Host': 'directory.ntschools.net',
        'Pragma': 'no-cache',
        'Referer': 'https://directory.ntschools.net/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/80.0.3987.132 Chrome/80.0.3987.132 Safari/537.36',
        'X-Requested-With': 'Fetch',
    }
    
    def parse(self, response):
        yield scrapy.Request(
            url="https://directory.ntschools.net/api/System/GetAllSchools",
            callback=self.parse_api, headers=self.headers)
        
    def parse_api(self, response):
        # To yield json data
        str_data = response.body
        json_data = json.loads(str_data)
        for school in json_data:
            school_code = school['itSchoolCode']
            yield  scrapy.Request(
                url=f'https://directory.ntschools.net/api/System/GetSchool?itSchoolCode={school_code}',
                callback=self.parse_school, headers=self.headers)
        
    def parse_school(self, response):
        # Convert json to working url
        working_url = 'https://directory.ntschools.net/#/schools/details/'
        json_url = response.url  # https://directory.ntschools.net/api/System/GetSchool?itSchoolCode=aspdcsch
        schoolCode_mechanism = (len(json_url) - json_url.find('=')-1) # 8
        schoolCode = json_url[-schoolCode_mechanism:] # aspdcsch
        
        # To yield json data
        str_data = response.body
        json_data = json.loads(str_data)
        
        yield {
            'Name' : json_data['name'],
            'Physical_address' : json_data['physicalAddress']['displayAddress'],
            'Postal_address' : json_data['postalAddress']['displayAddress'],
            'Email' : json_data['mail'],
            'Phone' : json_data['telephoneNumber'],
            'url' : working_url + schoolCode,
        }
        