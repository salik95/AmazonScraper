# Removing duplicate entries based on ASIN
import csv

isbn = []
url = []

with open('isbn-10.tsv') as tsvfile:
	for item in tsvfile:	
		isbn.append(item.replace('\n', ''))

# Fixing ISBN to 10 Characters
for index, item in enumerate(isbn):
	if len(item) < 10:
		zeros_count = 10 - len(item)
		new_item = item
		while (zeros_count > 0):
			new_item = '0' + new_item
			zeros_count = zeros_count - 1
		print(new_item)
		isbn[index] = new_item
		print('============================')

for item in isbn:
	if 'not available' in item.lower():
		url.append('ISBN Not Available')
	else:
		url.append('https://www.bookfinder.com/search/?author=&title=&lang=en&isbn=' + str(item) + '&new_used=U&destination=gb&currency=GBP&mode=basic&st=sr&ac=qr')

print(url)
print(isbn)
print(len(isbn))
print(len(url))

column_names = ['Book Finder URL']

outfile = open('bkurl.csv', 'w')
outcsv = csv.writer(outfile, delimiter=',')
outcsv.writerow([column for column in column_names])
for value in url:
	outcsv.writerow([value])
outfile.close()