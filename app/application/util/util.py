import config
import csv

def get_cuisine_types():
	'''
	Returns list of cuisine types to pass to client
	'''
	with open(config.DB_DIR + "/client_cuisine_type.csv", 'rb') as f:
		return [r[0].decode('utf-8') for r in csv.reader(f)]

def get_client_violations():
	'''
	Returns list of (code, description) tuples of violations to pass to client
	'''	
	truncate = lambda x: (x[:100] + " ...") if len(x) > 99 else x
	with open(config.DB_DIR + "/client_violations.csv", 'rb') as f:
		return [(r[0],r[1],truncate(r[2]), r[2]) for r in csv.reader(f)]

def get_client_names():
	'''
	Returns list of restaurant names to pass to client
	'''
	with open(config.DB_DIR + "/client_restaurant_names.csv", 'rb') as f:
			return [r[0].decode('utf-8') for r in csv.reader(f)]

def is_args_empty(args):
	'''
	Returns true if the client has not passed any args in GET request
	'''
	for a in args:
		if args[a] != '':
			return False
	return True

def process_query_results(results):
	'''
	Creates dictionary on query results to pass to client
	'''
	d = {}
	for r in results:
		generic = { "lat" : r["lat"],
				"lng" : r["lng"],
				"borough" : r["borough"],
				"cuisine_type" : r["cuisine_type"],
				"address" : r["address"].title() + ", " + r["zip"],
				"name" : r["name"].title() }

		specific = { "description" : r["description"], 
				"date" : r["inspection_date"] }
		try:
			d[r["name"]]["specific"].append(specific)
		except KeyError:
			d[r["name"]] = { "generic" : generic, "specific": [specific] }
	return d.values()





