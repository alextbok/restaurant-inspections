#!/usr/bin/python

from flask import Flask, render_template, url_for
import config
app = Flask(__name__)

@app.route("/")
def index():
	js_url = url_for('static', filename='index.js')
	css_url = url_for('static', filename='index.css')
	return render_template('index.html', 
		js_url=js_url, 
		css_url=css_url,
		google_api_key=config.GOOGLE_API_KEY)

if __name__ == "__main__":
	app.run(debug=True)