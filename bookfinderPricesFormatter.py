import csv

data = []

with open('Amazon and Bookfinder.tsv') as tsvfile:
	for item in tsvfile:	
		data.append(item.split('\t'))
print('=========================')
print(len(data))

for index, item in enumerate(data):
	if ',' in item[11]:
		if item[11][len(item[11])-3] == ',':
			print(item[11][len(item[11])-3])
			temp = list(data[index][11])
			temp[len(item[11])-3] = '.'
			data[index][11] = "".join(temp).replace('\xa0',',')
			print(data[index][11])

	if ',' in item[13]:
		if item[13][len(item[13])-3] == ',':
			print(item[13][len(item[13])-3])
			temp = list(data[index][13])
			temp[len(item[13])-3] = '.'
			data[index][13] = "".join(temp).replace('\xa0',',')
			print(data[index][13])

outfile = open('bookfinderPricesFixed.csv', 'w')
outcsv = csv.writer(outfile)
[outcsv.writerow([value for value in item]) for item in data]
outfile.close()
print('===================================')