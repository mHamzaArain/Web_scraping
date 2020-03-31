# -*- coding: utf-8 -*-
import scrapy
import json

api = 'https://www.monster.com/jobs/search/pagination/?q=Data-Scientist&where=Pakistan&stpage=1&isDynamicPage=true&isMKPagination=true&page={}&total=225'

class MonsterSpider(scrapy.Spider):
    name = 'Monster'
    start_urls = [api.format(pg_no) for pg_no in range(50)]

    def parse(self, response):
        str_data = response.text
        json_data = json.loads(str_data)
        
        for data in json_data:
            yield {
                'title' : data['Title'],
                'posted_date' : data["DatePosted"],
                'location' : data["LocationText"],
                'company_name' : data["Company"]["Name"],
                'detail_job_urk' : data["TitleLink"],
            }