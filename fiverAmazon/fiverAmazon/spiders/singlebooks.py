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

prices = []
books_format = []
offers = []

data = []

iterator = -1

column_names = ['Title', 'BSR', 'Price in £ (starting from)', 'Author', 'Book Type', 'Offers', 'ASIN', 'ISBN-10', 'ISBN-13', 'URL']

class SinglebooksSpider(scrapy.Spider):

	name = 'singlebooks'
	start_urls = book_url

	def __init__(self):
		dispatcher.connect(self.spider_closed, signals.spider_closed)
		with open('singlebooks.tsv') as tsvfile:

			for index, item in enumerate(tsvfile):
				# Extracting URLs
				book_url.append(str(item.split('\t')[5].strip()))

				# Extracting Prices
				price_single = item.split('\t')[4].strip().split('£')
				if len(price_single) > 1:
					price_single = price_single[len(price_single)-1]
				else:
					price_single = '0'
				prices.append(price_single)

				# Extracting Books Formats
				books_format_single = item.split('\t')[2].strip()
				if len(books_format_single) < 2:
					books_format_single = 'Not available'
				books_format.append(books_format_single)

				# Extracting Available Offers
				offer_single = item.split('\t')[3].strip().lower()
				if 'unknown' in offer_single or len(offer_single) < 5:
					offer_single = 'None'
				offers.append(offer_single)

	def parse(self, response):

		global iterator

		iterator = iterator + 1
		print('=================================================================')
		print('Total Entries: ' + str(len(data)))
		print('=================================================================')
		print('Iterator: ' + str(iterator))
		print('=================================================================')
		title = response.xpath('//span[contains(@id, "roductTitle")]/text()').extract_first()
		if title is None:
			title = 'No Title Available!!'
		print('title: ' + title)
		print('=================================================================')
		url = response.url
		print('url: ' + url)
		print('=================================================================')
		bsr = re.sub('[^0-9,]', "", "".join(response.css('li[id="SalesRank"]::text').extract()).strip())
		print('bsr: ' + bsr)
		print('=================================================================')
		author = response.css('div[id="booksTitle"] span.author a.contributorNameID::text').extract_first()
		if author is None:
			author = response.css('div[id="booksTitle"] span.author a::text').extract_first()
			if author is None:
				author = 'No Author Specified!!'
		print('author: ' + author)
		print('=================================================================')
		ASIN = response.css('input[id="ASIN"]::attr(value)').extract_first()
		if ASIN is None:
			ASIN = 'Not available'
		print('ASIN: ' + ASIN)
		print('=================================================================')
		ISBN_10 = response.xpath('//li/b[contains(text(), "ISBN-10:")]/../text()').extract_first()
		if ISBN_10 is None:
			ISBN_10 = 'Not available'
		print('ISBN_10: ' + ISBN_10.strip())
		print('=================================================================')
		ISBN_13 = response.xpath('//li/b[contains(text(), "ISBN-13:")]/../text()').extract_first()
		if ISBN_13 is None:
			ISBN_13 = 'Not available'
		print('ISBN_13: ' + ISBN_13.strip())
		print('=================================================================')
		price = prices[iterator]
		book_type = books_format[iterator]
		sale_offers = offers[iterator]
		data.append([title, bsr, price, author, book_type, sale_offers, ASIN, ISBN_10, ISBN_13, url])

	def spider_closed(self, spider):
		print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
		outfile = open('singlebooks_data.csv', 'w')
		outcsv = csv.writer(outfile)
		outcsv.writerow([column for column in column_names])
		[outcsv.writerow([value.encode('ascii', 'replace') for value in item]) for item in data]
		outfile.close()
		print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')