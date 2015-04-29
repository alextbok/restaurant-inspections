from flask import Flask, redirect
app = Flask(__name__)

# setup the database
import os
import config
from application.db import setup
if not os.path.isfile(config.DB_PATH):
	print "Creating database..."
	setup.do_setup()
	print "...Finished"

import application.views




app.config.from_object('config')

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return redirect('/'), 302