from datetime import datetime
from bottle import route, post, template, run, static_file, request, response
import json
import os, re

# options:
# get last seen episodes/series/movies
# index file from mediaserver by id/path

apikeyinvalid = {
	'status': 'error',
	'message': 'Invalid API key'
}


@route('/aps/<apikey>')
def index(apikey):
	if apikey != 123:
		content = apikeyinvalid
		response.status = 404
	else:

		content = {
			'status': 'success',
			'message': 'your api key is valid'
		}

	response.content_type = "application/json"
	
	return content

@route('/api/<apikey:int>/<option>')
def index():

	synoindex = request.get('synoindex')
	path = request.get('path')

	if synoindex:
		pqsql


run(host='0.0.0.0', port=1337, reloader=True)