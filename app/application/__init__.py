from flask import Flask, redirect
app = Flask(__name__)

import application.views
import config
import os
from application.db import setup

if not os.path.isfile(config.DB_PATH):
	print "Creating database..."
	setup.new_db()
	setup.load_inspections(config.DB_DIR + "/final_latlng.csv")
	setup.load_violation_codes(config.DB_DIR + "/violation_codes.csv")
	setup.clean_boroughs()
	setup.optimize_inspections()

app.config.from_object('config')

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return redirect('/'), 302