#!/usr/bin/python

from flask import Flask, render_template, url_for, request, jsonify
import config
import itertools
import json
from application import app
from application.db import db
from application.util import util, memoized
from werkzeug import datastructures

violations = util.get_client_violations()
restaurant_names = util.get_client_names()
cuisine_types = util.get_cuisine_types()
default_results = util.process_query_results(db.select({'violation_code' : '04L'}))

@app.route('/', methods=['GET'])
def index():
	print get_results_cached.cache_info()
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
		num_results=len(default_results),
		results=get_results(request.args)[:config.STEP_SIZE])

@app.route('/update/', methods=['GET'])
def update():
	if "page_number" in request.args:
		page_number = int(request.args["page_number"])
		if page_number < 0:
			data = get_results(request.args)
			d = { 'data' : data[:config.STEP_SIZE], 'num_results' : len(data), 'page_change' : False }
		else:
			data = get_results(request.args)
			d = { 'data' : data[config.STEP_SIZE*page_number:(config.STEP_SIZE*page_number + config.STEP_SIZE)], 'num_results' : len(data), 'page_change' : True }
	else: 
		data = get_results(request.args)
		d = { 'data' : data[:config.STEP_SIZE], 'num_results' : len(data), 'page_change' : True }
	if len(d['data']) == 0:
		d['page_change'] = False
	return json.dumps(d)

@memoized.lru_cache(maxsize=config.CACHE_SIZE)
def get_results_cached(args):
	'''
	Decorated with a least recently used cache. Cache hits will not be evaluated by the database
	'''
	return default_results if util.is_args_empty(args) else util.process_query_results(db.select(args))

def get_results(args):
	'''
	Wrapper for above method. Creates a new immutable (i.e. hashable) dict from the GET parameters
	and ignores the 'page_number' parameter, as we do not want to consider it for caching
	'''
	return get_results_cached(datastructures.ImmutableMultiDict(mapping={ k : args[k] for k in args if k != 'page_number' }))









