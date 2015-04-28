#!/usr/bin/python

from flask import Flask, render_template, url_for, request
import config
from application import app
from application.db import db

@app.route('/')
def index():
	js_url = url_for('static', filename='index.js')
	css_url = url_for('static', filename='index.css')
	return render_template('index.html', 
		js_url=js_url, 
		css_url=css_url,
		google_api_key=config.GOOGLE_API_KEY)

@app.route('/search', methods=['GET'])
def search():
	#res = db.select(request.args)
	js_url = url_for('static', filename='index.js')
	css_url = url_for('static', filename='index.css')
	return render_template('index.html', 
		js_url=js_url, 
		css_url=css_url,
		google_api_key=config.GOOGLE_API_KEY)

if __name__ == "__main__":
	app.run(debug=True)