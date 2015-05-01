#!/usr/bin/python

from flask import Flask, render_template, url_for, request, jsonify
import config
import itertools
import json
from application import app
from application.db import db
from application.util import util, memoized

violations = util.get_client_violations()
restaurant_names = util.get_client_names()
cuisine_types = util.get_cuisine_types()
default_results = util.process_query_results(db.select({"violation_code" : "06I"}))

@app.route('/', methods=['GET'])
def index():
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
		results=get_results(request.args)[:config.STEP_SIZE])

@app.route('/update/', methods=['GET'])
def update():
	if "page_number" in request.args:
		page_number = int(request.args["page_number"])
		if page_number < 0:
			print "\t\t\t UPDATE 1" 
			d = { 'data' : get_results(request.args)[:config.STEP_SIZE], 'page_change' : False }
		else:
			print "\t\t\t UPDATE 2" 
			d = { 'data' : get_results(request.args)[config.STEP_SIZE*page_number:(config.STEP_SIZE*page_number + config.STEP_SIZE)], 'page_change' : True }
	else:
		print "\t\t\t UPDATE 3" 
		d = { 'data' : get_results(request.args)[:config.STEP_SIZE], 'page_change' : True }
	if len(d['data']) == 0:
		print "\t\t\t UPDATE 4" 
		d['page_change'] = False
	return json.dumps(d)

@memoized.Memoized
def get_results(args):
	return default_results if util.is_args_empty(args) else util.process_query_results(db.select(args))









