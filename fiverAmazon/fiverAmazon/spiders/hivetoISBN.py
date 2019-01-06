# -*- coding: utf-8 -*-
import scrapy
import re
import locale
import csv
import json
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.http.request import Request

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 

hive_url = []

data = {}
data['isbn'] = []

iterator = -1

column_names = ['ISBN']

class HiveToISBNSpider(scrapy.Spider):

	name = 'hivetoISBN'
	start_urls = hive_url

	def __init__(self):
		dispatcher.connect(self.spider_closed, signals.spider_closed)
		with open('hive.json') as jsonfile:
			for item in json.load(jsonfile)['links']:
				hive_url.append(item)

	def parse(self, response):
		print(response.css('span[itemprop="isbn"]::text').extract_first())
		data['isbn'].append(response.css('span[itemprop="isbn"]::text').extract_first())

	def spider_closed(self, spider):
		print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
		with open('isbn_list.json', 'w') as fp:
			json.dump(data, fp)
		print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')