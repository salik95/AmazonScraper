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

book_url = []

data = []

column_names = ['BSR']

class BsrextractorSpider(scrapy.Spider):

	name = 'bsrextractor'
	start_urls = book_url

	def __init__(self):
		dispatcher.connect(self.spider_closed, signals.spider_closed)
		with open('amazonurl.tsv') as tsvfile:
			for item in tsvfile:
				# Extracting URLs
				book_url.append(str(item.strip()))

	def parse(self, response):

		print('=================================================================')
		bsr = re.sub('[^0-9,]', "", "".join(response.css('li[id="SalesRank"]::text').extract()).strip())
		print('bsr: ' + bsr)
		data.append([bsr])
		print('=================================================================')

	def spider_closed(self, spider):
		print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
		outfile = open('bsr_data.csv', 'w')
		outcsv = csv.writer(outfile)
		outcsv.writerow([column for column in column_names])
		[outcsv.writerow([value for value in item]) for item in data]
		outfile.close()
		print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')