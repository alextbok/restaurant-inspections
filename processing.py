'''
Ignore this script. This was originally used to explore that dataset to 
see if it was of interest to me. It is in no way used in my project.
'''
import csv
import itertools

def get_data(fp):
	with open(fp, 'rb') as f:
		rows = [r for r in csv.reader(f)]
		return rows[0], rows[1:]

def get_inspections(inspections, vcodes):
	for i in inspections:
		if i[11] in vcodes:
			i.append(vcodes[i[11]])
	return inspections


def query(code, inspections):
	count = 0
	restaurants = []
	for i in inspections:
		if i[11] == code:
			count += 1
			restaurants.append(i)

	print str(count) + ' restaurants in nyc have violation: '
	print '\t' + vcodes[code]

	return restaurants

if __name__=="__main__":

	vcodes = {r[3]:r[4] for r in get_data('./violation_codes.csv')[1]}
	inspections = get_inspections(get_data('./inspections.csv')[1], vcodes)

	rs = query('05B', inspections)
	print 'restaurants:'
	for r in rs:
		print '\t' + r[1]




		
