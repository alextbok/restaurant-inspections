#!/usr/bin/python

from flask import Flask, render_template, url_for, request
import config
import itertools
from application import app
from application.db import db
from application.util import util

violations = util.get_client_violations()
restaurant_names = util.get_client_names()
cuisine_types = util.get_cuisine_types()
default_results = [x for _, x in zip(range(100), db.select({"violation_code" : "06I"}))]

@app.route('/', methods=['GET'])
def index():
	print request.args
	print util.is_args_empty(request.args)
	print "number of default results: " + str(len(default_results))
	js_url = url_for('static', filename='index.js')
	css_url = url_for('static', filename='index.css')
	typeahead_url = url_for('static', filename='typeahead.js')
	png_url = url_for('static', filename='hazard.png')
	return render_template('index.html', 
		js_url=js_url,
		typeahead_url=typeahead_url,
		css_url=css_url,
		png_url=png_url,
		google_api_key=config.GOOGLE_API_KEY,
		violations=violations,
		restaurant_names=restaurant_names,
		cuisine_types=cuisine_types,
		results=default_results if util.is_args_empty(request.args) else [x for _, x in zip(range(100), db.select(request.args))])