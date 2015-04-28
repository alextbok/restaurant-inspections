#!/usr/bin/python

from flask import Flask, render_template, url_for, request
import config
import itertools
from application import app
from application.db import db
from application.util import util

@app.route('/', methods=['GET'])
def index():
	print request.args
	js_url = url_for('static', filename='index.js')
	css_url = url_for('static', filename='index.css')
	return render_template('index.html', 
		js_url=js_url, 
		css_url=css_url,
		google_api_key=config.GOOGLE_API_KEY,
		violations=util.get_client_violations(),
		cuisine_types=util.get_cuisine_types())#,
		#results=[x for _, x in zip(range(100), db.select(request.args))])

if __name__ == "__main__":
	app.run(debug=True)