from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import csv

data = []

isbn_list = []

column_names = ['Title', 'Author', 'Book Format', 'ASIN', 'ISBN-10', 'ISBN-13', 'BSR', 'Price in £ (starting from)', 'URL']

driver = webdriver.Chrome()

asin = []
isbn10 = []
isbn13 = []

driver.get('https://www.amazon.co.uk')
with open('isbn_list.json') as jsonfile:
	isbn_list_unclean = json.load(jsonfile)['isbn']
	
	for unclean_isbn in isbn_list_unclean:
		if unclean_isbn[:3] == '978':
			isbn_list.append(unclean_isbn)

	for isbn in isbn_list:
		search_bar = driver.find_element_by_id('twotabsearchtextbox')
		search_bar.clear()
		search_bar.send_keys(isbn)
		search_bar.send_keys(Keys.RETURN)

		try:
			driver.find_element_by_css_selector('li[id="result_0"] a').click()
		except:
			search_bar = driver.find_element_by_id('twotabsearchtextbox')
			search_bar.clear()
			search_bar.send_keys(isbn[3:])
			search_bar.send_keys(Keys.RETURN)
			try:
				driver.find_element_by_css_selector('li[id="result_0"] a').click()
			except:
				continue
		try:
			driver.find_element_by_css_selector('button[aria-label="No, thank you"]').click()
		except:
			pass

		try:
			title = driver.find_element_by_xpath('//span[contains(@id, "roductTitle")]').text
		except:
			continue

		try:
			author = driver.find_element_by_css_selector('div[id="booksTitle"] span.author a').text
			if author == '':
				author = driver.find_element_by_css_selector('div[id="booksTitle"] span.author a.contributorNameID').text
		except:
			try:
				author = driver.find_element_by_css_selector('div[id="booksTitle"] span.author a.contributorNameID').text
			except:
				author = None
		if author == None:
			author = ''

		url = driver.current_url

		try:
			bsr = driver.find_element_by_css_selector('li[id="SalesRank"]').text.split('Amazon Bestsellers Rank: ')[1].split(' in')[0]
		except:
			continue

		try:
			book_format = driver.find_element_by_css_selector('li.selected span.format a span').text
		except:
			book_format = ''
		
		try:
			used_offer = driver.find_element_by_css_selector('li.selected span.olp-used a').text.strip().split('£')[1]
		except:
			continue

		try:
			ASIN = driver.find_element_by_css_selector('input[id="ASIN"]').get_attribute('value')
		except:
			ASIN = ''
		asin.append(ASIN)
		
		try:
			ISBN_10 = driver.find_element_by_xpath('//li/b[contains(text(), "ISBN-10:")]/..').text.split('ISBN-10: ')[1]
		except:
			ISBN_10 = ''
		isbn10.append(ISBN_10)
		
		try:
			ISBN_13 = driver.find_element_by_xpath('//li/b[contains(text(), "ISBN-13:")]/..').text.split('ISBN-13: ')[1]
		except:
			ISBN_13 = ''
		isbn13.append(ISBN_13)

		data.append([title, author, book_format, ASIN, ISBN_10, ISBN_13, bsr, used_offer, url])
		if len(data) == 11:
			break

for asn in asin:
	print(asn)
print('===========================================')
print('===========================================')
for isn10 in isbn10:
	print(isn10)
print('===========================================')
print('===========================================')
for isn13 in isbn13:
	print(isn13)
print('===========================================')
print('===========================================')

outfile = open('ISBNToAmazonData.csv', 'w')
outcsv = csv.writer(outfile)
outcsv.writerow([column for column in column_names])
[outcsv.writerow([value for value in item]) for item in data]
outfile.close()

driver.close()