import requests
from bs4 import BeautifulSoup
import csv

amazon_books = []
counter = 0

with open('amazon.tsv') as amazon:
	for item in amazon:
		amazon_books.append(item.split('\t'))

print('===================================')
print(len(amazon_books))

for index, book in enumerate(amazon_books):
	if book[11] == '' or book[11] == '0':
		counter+=1
		url = book[10].strip()
		print('URL: ' + url)

		if 'not available' in url.lower().strip():
			amazon_books[index].append('0')
			amazon_books[index].append('None')
			amazon_books[index].append('0')
			amazon_books[index].append('None')
		else:

			print(book[7])

			lower_price = '0'
			lower_vendor = 'None'

			higher_price = '0'
			higher_vendor = 'None'

			req = requests.get(url)
			soup = BeautifulSoup(req.text)

			price = soup.find_all('span', {"class": "results-price"})
			title = soup.find_all('span', {"class": "results-explanatory-text-Logo"})

			# For low price
			for item in price:
				lower_price = item.text
				break

			for item in title:
				if item.a is not None:
					lower_vendor = item.a.img['title']
					break
			
			amazon_books[index].append(lower_price.replace('£', '').strip())
			amazon_books[index].append(lower_vendor.strip())

			# For high price
			for item in price:
				higher_price = item.text

			for item in title:
				if item.a is not None:
					higher_vendor = item.a.img['title']

			end_page = 0
			end_page_url = ''

			for ana in soup.find_all('a'):
				if ana.parent.name == 'th':
					print('++++++++++++++')
					print(ana.text)
					if ana.text.strip() != '1' and ana.text.strip() != '2' and ana.text.strip() != '3' and ana.text.strip() != '4' and ana.text.strip() != '5':
						continue
					if int(ana.text) > end_page:
						end_page = int(ana.text)
						end_page_url = ana['href']
			
			if end_page != 0:
				req = requests.get(end_page_url)
				soup = BeautifulSoup(req.text)

				price = soup.find_all('span', {"class": "results-price"})
				title = soup.find_all('span', {"class": "results-explanatory-text-Logo"})

				# For high price
				for item in price:
					higher_price = item.text

				for item in title:
					if item.a is not None:
						higher_vendor = item.a.img['title']
				
			amazon_books[index].append(higher_price.replace('£', '').strip())
			amazon_books[index].append(higher_vendor.strip())
			print('----------------------')
			print(lower_price.replace('£', ''))
			print(lower_vendor)
			print(higher_price.replace('£', ''))
			print(higher_vendor)
			print('----------------------')
			print(counter)

outfile = open('bookfinder.csv', 'w')
outcsv = csv.writer(outfile)
[outcsv.writerow([value for value in item]) for item in amazon_books]
outfile.close()
print('===================================')
print(len(amazon_books))