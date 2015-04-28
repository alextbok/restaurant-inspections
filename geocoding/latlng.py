'''
Alex Bok

Various functions that geocode (retrieve (lat, long) pairs) for our addresses
Part of the manual ETL process, and is not used in the web application
'''
import csv
import requests
import time

BASE_URL = "http://geocoding.geo.census.gov/geocoder/locations/address"

def get_curr_addresses():
	'''
	Returns a set of already geocoded addresses so we don't ask
	the service to geocode them again
	'''
	a = {}
	with open('./latlng.csv', 'rb') as f:
		reader = csv.reader(f)
		for r in reader:
			a[r[0] + "," + r[1]] = 1
	return a

def write_to_file():
	'''
	Queries service to geocode addresses and writes
	tuples (address,lat,lng) to standard output
	Pauses every iteration so we don't overload the server
	and/or get banned from using the free service
	'''
	finished = get_curr_addresses()
	with open('./inspections.csv', 'rb') as f:
		reader = csv.reader(f)
		reader.next() #skip header
		unique = {}
		for r in reader:
			address = "%s %s,%s" % (r[3], r[4], r[5])
			if address not in finished:
				unique[address] = 1
		for address in unique:
			a = address.split(",")
			payload = {'street': a[0], 
					'city': 'New York',
					'state': 'NY',
					'zip': a[1],
					'benchmark': 9,
					'format': 'json'}
			r = requests.get(BASE_URL, params=payload)
			try:
				lat = r.json()["result"]["addressMatches"][0]["coordinates"]["y"]
				lng = r.json()["result"]["addressMatches"][0]["coordinates"]["x"]
				print "%s,%s,%s" % (address,lat,lng)
			except IndexError:
				print "%s,%s,%s" % (address,"NULL","NULL")
			except KeyError:
				continue
			time.sleep(1.2) # pause to not overwhelm the server

def split():
	'''
	Find all of the null valued coordinates (i.e. the addresses that the
	geocoding service failed on) and splits them into files with 100 addresses
	each. (The other service we use allows 100-line csv fils for free)
	'''
	finished = []
	null = []
	with open('./latlng.csv', 'rb') as f:
		reader = csv.reader(f)
		for r in reader:
			if r[2] == "NULL":
				null.append((r[0],r[1]))
			else:
				finished.append(r)
	file_no = 0
	writer = None
	for i in range(len(null)):
		if i % 100 == 0:
			writer = csv.writer(open('./unfinished/latlng_null_' + str(i/100) + '.csv', 'w'))
			writer.writerow(["Address","Zip","City","State"])
			i += 1
		writer.writerow([null[i][0], null[i][1], "New York", "NY"])

def write_all():
	'''
	Combines results of all geocoding requests
	'''
	addresses = {}
	with open('./latlng.csv', 'rb') as f:
		reader = csv.reader(f)
		for r in reader:
			addresses[r[0] + "," + r[1]] = (r[2], r[3])
	for i in range(19):
		f = open('./finished/latlng' + str(i) + '.csv', 'rb')
		reader = csv.reader(f)
		reader.next() # skip header
		for r in reader:
			addresses[r[4] + "," + r[5]] = (r[0], r[1])
	with open('../data/inspections.csv', 'rb') as f:
		reader = csv.reader(f)
		writer = csv.writer(open('../data/final_latlng.csv','w'))
		reader.next() # skip header
		for r in reader:
				r.append(addresses[r[3] + " " + r[4] + "," + r[5]][0])
				r.append(addresses[r[3] + " " + r[4] + "," + r[5]][1])
				writer.writerow(r)

if __name__=="__main__":
	#write_to_file()
	#split()
	write_all()








