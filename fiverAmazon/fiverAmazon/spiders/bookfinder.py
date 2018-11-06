# -*- coding: utf-8 -*-
import scrapy
import re
import locale
import csv
import json
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
import unicodedata

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 

data = {}
url = []

single_book = []

column_names = ['ISBN', 'High Price', 'High Price Provider', 'Low Price', 'Low Price Provider']


class BookfinderSpider(scrapy.Spider):

	name = 'bookfinder'
	start_urls = url

	def __init__(self):
		dispatcher.connect(self.spider_closed, signals.spider_closed)
		with open('bkurl1.tsv') as tsvfile:
			for item in tsvfile:
				if 'not available' in item.lower():
					url.append('https://www.google.com/')
				else:
					url.append(item.strip())
		print(len(url))
	
	def parse(self, response):
		if response.url == 'https://www.google.com/':
			data[str(len(data)) + 'None'] = ''
		else:

			print('-------------------- Start --------------------')
			
			price = response.css('tr.has-data td.results-table-center span.results-price a::text').extract()
			seller = response.css('tr.has-data td.results-table-center span.results-explanatory-text-Logo a img::attr(title)').extract()
			
			current_isbn = unicodedata.normalize('NFKD', response.css('span[itemprop = "isbn"]::text').extract_first()).encode('ascii','ignore')
			print('===============')
			print(current_isbn)
			print(price)
			print(seller)
			print('===============')
			
			if current_isbn not in data:
				data[current_isbn] = []
			
			for p, s in zip(price, seller):
				data[current_isbn].append([unicodedata.normalize('NFKD', p).encode('ascii','ignore'), unicodedata.normalize('NFKD', s).encode('ascii','ignore')])
			print('-------------------- End --------------------')
			
			next_page = response.css('tr.results-table-header-row th > a::attr(href)').extract_first()
			
			if next_page != None and len(next_page) > 1:
				yield response.follow(next_page, self.parse)

	def spider_closed(self, spider):
		print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
		final_data = []
		for item in data:
			maxprice = 0
			minprice = 0
			maxindex = 0
			minindex = 0
			print('--------------------------')
			print(item)
			print(data[item])
			print('--------------------------')
			try:
				if 'none' in item.lower():
					final_data.append(['Nill', '0', 'None',  '0', 'None'])
				else:	
					for index, entry in enumerate(data[item]):
						if locale.atof(entry[0]) > maxprice:
							maxprice = locale.atof(entry[0])
							maxindex = index
						if locale.atof(entry[0]) < minprice:
							minprice = locale.atof(entry[0])
							minindex = index
					print('===================================')
					print('ISBN: ' + item)
					print('Maximum: ' + ' - '.join(data[item][maxindex]))
					print('Minimum: ' + ' - '.join(data[item][minindex]))
					print('===================================')
					final_data.append([item, data[item][maxindex][0], data[item][maxindex][1],  data[item][minindex][0], data[item][minindex][1]])
			except:
				print('*********************************')
				print('EXCEPTION MET!!!!!!')
				print('*********************************')
				final_data.append(['Nill', '0', 'None',  '0', 'None'])
				pass
		outfile = open('bookfinder.csv', 'w')
		outcsv = csv.writer(outfile)
		outcsv.writerow([column for column in column_names])
		[outcsv.writerow([value for value in item]) for item in final_data]
		outfile.close()
		print(len(final_data))
		print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')