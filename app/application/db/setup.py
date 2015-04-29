'''
Alex Bok

Contains functions that setup our database
These should be called once upon instantiating our application
'''
import sqlite3 as sql
import csv
import config
from datetime import datetime as dt

inspections_schema = ("DROP TABLE IF EXISTS inspections;"
		"CREATE TABLE inspections ("
			"id INTEGER PRIMARY KEY AUTOINCREMENT,"
			"name VARCHAR(255),"
			"borough SMALLINT,"
			"address VARCHAR(255),"
			"zip CHARACTER(5),"
			"cuisine_type VARCHAR(255),"
			"inspection_date DATE,"
			"action CHARACTER(1),"
			"violation_code VARCHAR(5),"
			"score INTEGER,"
			"current_grade CHARACTER(1),"
			"lat DECIMAL(9,6),"
			"lng DECIMAL(9,6)"
		");")

violations_schema = ("DROP TABLE IF EXISTS violations;"
		"CREATE TABLE violations ("
			"id INTEGER PRIMARY KEY AUTOINCREMENT,"
			"code VARCHAR(5),"
			"description VARCHAR(1024)"
		");")

def new_db():
	'''
	Creates the datase with schema defined above
	Deletes existing database if it exists
	This is ok since our application is read only
	'''
	with sql.connect(config.DB_PATH) as con:
		con.cursor().executescript(inspections_schema)
		con.commit()
		con.cursor().executescript(violations_schema)
		con.commit()

def clean_boroughs():
	'''
	Both 0 and 1 indicate manhattan, so set all borough{0,1} = 1
	'''
	with sql.connect(config.DB_PATH) as con:
		query = "UPDATE inspections SET borough = ( CASE WHEN (borough=0) THEN 1 ELSE (borough) END );"
		con.cursor().execute(query)
		con.commit()

def load_violation_codes(path):
	'''
	Loads the relevant information from violation_codes.csv into database
	'''
	with open(path, 'rb') as f:
		reader = csv.reader(f)
		reader.next() # skip header
		rows = most_recent_violation_codes([{ "code" : unicode(r[3], "utf-8"), 
					"description" : unicode(r[4], "utf-8"),
					"start_date" : unicode(r[0], "utf-8")} for r in reader])
		to_db = [(e["code"], e["description"]) for e in rows]
		query = "INSERT INTO violations (code, description) VALUES (?,?);"
		con = sql.connect(config.DB_PATH)
		con.executemany(query, to_db)
		con.commit()

def optimize_inspections():
	'''
	Creates an index on the name column of inspections table
	'''
	with sql.connect(config.DB_PATH) as con:
				query = "CREATE INDEX name_index on inspections (name);"
				con.cursor().execute(query)
				con.commit()

def most_recent_violation_codes(rows):
	'''
	Returns a unique list of violation codes
	The list contains the most recent ones as defined by start_date
	'''
	d = {}
	for r in rows:
		try:
			if is_more_recent(r["start_date"], d[r["code"]]["start_date"]):
				d[r["code"]] = r
		except KeyError:
			d[r["code"]] = r
	return [val for val in d.values()]

def is_more_recent(t1, t2):
	'''
	Returns True if t1 is more recent than t2
	'''
	return dt.strptime(t1, "%Y-%m-%d") > dt.strptime(t2, "%Y-%m-%d")


def load_inspections(path):
	'''
	Takes the inspections.csv file and loads 
	the relevant information into database
	'''
	with open(path, 'rbU') as f:
		reader = csv.reader(f)
		reader.next() # skip header
		
		rows = [{"name" : unicode(r[1], "utf-8"),
				"borough" : unicode(r[2], "utf-8"),
				"address" : (unicode(r[3], "utf-8") + " " + unicode(r[4], "utf-8")),
				"zip" : unicode(r[5], "utf-8"),
				"cuisine_type" : unicode(r[7], "utf-8"),
				"inspection_date" : unicode(r[9], "utf-8"),
				"action" : unicode(r[10], "utf-8"),
				"violation_code" : unicode(r[11], "utf-8"),
				"score" : unicode(r[12], "utf-8"),
				"current_grade" : unicode(r[13], "utf-8"),
				"lat" : unicode(r[17], "utf-8"),
				"lng" : unicode(r[18], "utf-8")} for r in reader]
		to_db = [(e["name"], 
				e["borough"],
				e["address"],
				e["zip"],
				e["cuisine_type"],
				e["inspection_date"],
				e["action"],
				e["violation_code"],
				e["score"],
				e["current_grade"],
				e["lat"],
				e["lng"]) for e in rows]
		query = ("INSERT INTO inspections (name,"
			"borough,"
			"address,"
			"zip,"
			"cuisine_type,"
			"inspection_date,"
			"action,"
			"violation_code,"
			"score,"
			"current_grade,"
			"lat,"
			"lng) VALUES (?,?,?,?,?,?,?,?,?,?,?,?);")
		con = sql.connect(config.DB_PATH)
		con.executemany(query, to_db)
		con.commit()


if __name__=="__main__":
	new_db()
	load_inspections(DB_DIR + "/final_latlng.csv")
	load_violation_codes(DB_DIR + "/violation_codes.csv")







