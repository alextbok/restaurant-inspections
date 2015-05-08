'''
Prints the percentage of violations that are repeated. For example, if 
restaurant A commits violation 10F in 2013 and does so again in 2014,
then those two violations are counted as a single repeat.
'''
import csv

def get_data(fp):
	with open(fp, 'rb') as f:
		rows = [r for r in csv.reader(f)]
		return rows[0], rows[1:]

def do_query(inspections):
	restaurants = {}
	count = 0
	total = 0
	for i in inspections:
		total += 1
		_id = i[0]
		name = i[1]
		address = i[4]
		code = i[11]
		try:
			restaurants[name + address].append(code)
		except KeyError:
			restaurants[name + address] = [code]
	for r in restaurants:
		count += len(restaurants[r]) - len(set(restaurants[r]))

	return (count + 0.0) / total

if __name__=="__main__":
	print do_query(get_data('../../app/data/final_latlng.csv')[1])






