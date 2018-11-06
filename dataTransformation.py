# Removing duplicate entries based on ASIN
import csv

asin = []
books = []

with open('final.tsv') as tsvfile:
	for item in tsvfile:	
		asin.append(item.split('\t')[6])

new_asin = set(asin)
asin = list(new_asin)
del asin[0]
print(len(asin))

with open('final.tsv') as tsvfile:
	for item in tsvfile:
		for data in asin:
			if item.split('\t')[6] == data:
				books.append(item.split('\t'))
				asin.remove(data)

print(len(books))
print(len(asin))

# Fixing ASIN to 10 Characters
for index, item in enumerate(books):
	if len(item[6]) < 10:
		zeros_count = 10 - len(item[6])
		new_item = item[6]
		while (zeros_count > 0):
			new_item = '0' + new_item
			zeros_count = zeros_count - 1
		print(new_item)
		books[index][6] = new_item
		print('============================')

print(len(books))
print(len(asin))

column_names = ['Title', 'BSR', 'Price in £ (starting from)', 'Author', 'Book Type', 'Offers', 'ASIN', 'ISBN-10', 'ISBN-13', 'URL']

outfile = open('Unique.csv', 'w')
outcsv = csv.writer(outfile)
outcsv.writerow([column for column in column_names])
[outcsv.writerow([value for value in item]) for item in books]
outfile.close()