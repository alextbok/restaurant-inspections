import sqlite3 as sql
import config

valid_params = set(['name', 'borough', 'cuisine_type', 'violation_code'])

def select(kwargs):
	'''
	Executes a select query on inspections table
	'''

	clause = ' AND '.join(['%s = :%s' % (k, k) for k in kwargs.keys() if k in valid_params])
	with sql.connect(config.DB_PATH) as con:
		cursor = con.cursor()
		query = ('SELECT * FROM inspections AS i, ' 
			'violations AS v '
			'WHERE i.violation_code = v.code ')
		if len(clause) > 0:
			query += "AND %s" % (clause)
		columns = ', '.join(kwargs.keys())
		cursor.execute(query, kwargs)
		ret = []
		for row in cursor.fetchall():
			_, name, borough, address, _zip, cuisine_type, inspection_date, action, _, score, current_grade, lat, lng, _, _, description = row
			yield { 'name' : name, 
					'borough' : borough, 
					'address' : address, 
					'zip' : _zip, 
					'cuisine_type' : cuisine_type, 
					'inspection_date' : inspection_date, 
					'action' : action, 
					'score' : score, 
					'current_grade' : current_grade, 
					'lat' : lat, 
					'lng' : lng, 
					'description' : description }
