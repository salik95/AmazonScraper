# -*- coding: utf-8 -*-
import scrapy
import re
import locale
import csv
import json
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 

scrape_next_page = True

data = []

column_names = ['Title', 'BSR', 'Price in £ (starting from)', 'Author', 'Book Type', 'ASIN', 'ISBN-10', 'ISBN-13', 'URL']

class Amazon2Spider(scrapy.Spider):

	name = 'amazon2'
	start_urls = ['https://www.amazon.co.uk/s/ref=sr_nr_p_36_5?rnid=389022011&rh=n%3A266239%2Cp_n_binding_browse-bin%3A492563011&qid=1540501469&bbn=266239&low-price=1000&high-price=2000']

	def __init__(self):
		dispatcher.connect(self.spider_closed, signals.spider_closed)

	def parse(self, response):
		
		global scrape_next_page

		for href in response.css('li div.a-fixed-left-grid-col a.s-access-detail-page::attr(href)').extract():
			yield response.follow(href, self.parse_author)
		if scrape_next_page:
			next_page = str(int(response.css('div[id="bottomBar"] span.pagnCur::text').extract_first()) + 1)
			if next_page == '75':
				scrape_next_page = False
			next_page_urls = response.css('div[id="bottomBar"] span.pagnLink a::attr(href)').extract()
			next_url = ''
			for item in next_page_urls:
				if 'page='+next_page in item:
					next_url = 'https://www.amazon.co.uk' + item
					print(next_url)
			yield scrapy.Request(next_url, callback = self.parse)

	def parse_author(self, response):

		print('=================================================================')
		print('Total Entries: ' + str(len(data)))
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
		if locale.atoi(bsr) <= 1500000:
			used_offer = response.css('li.selected span.olp-used a::text').extract()
			if used_offer is None:
				price = '0'
			else:
				used_offer = "".join(used_offer).strip().split('£')
				price = used_offer[len(used_offer)-1]
			print('Offer: ' + price)
			print('=================================================================')
			if len(used_offer) > 1:
				if locale.atof(price) >= 1000.00 and locale.atof(price) <= 2000.00:
					image = response.css('div[id="main-image-container"] img::attr(src)').extract_first()
					print('Image: ' + image)
					print('=================================================================')
					if 'no-img-lg' not in image:
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
						book_type = 'Hardcover'
						data.append([title, bsr, price, author, book_type, ASIN, ISBN_10, ISBN_13, url])
						with open('test2.txt', 'w') as f:
							for item in data:
								f.write("%s\n" % item)

	def spider_closed(self, spider):
		print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
		outfile = open('1000_2000_under_1.5_million.csv', 'w')
		outcsv = csv.writer(outfile)
		outcsv.writerow([column for column in column_names])
		[outcsv.writerow([value for value in item]) for item in data]
		outfile.close()
		print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')