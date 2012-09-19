# Author: cytec <iamcytec@googlemail.com>
# URL: http://github.com/cytec/SynoDLNAtrakt/
#
# This file is part of SynoDLNAtrakt.

import urllib2
import simplejson
import hashlib
import json
from synodlnatrakt import config
from synodlnatrakt import helper
from synodlnatrakt.logger import logger


responses = {
		100: ('Continue', 'Request received, please continue'),
		101: ('Switching Protocols',
					'Switching to new protocol; obey Upgrade header'),

		200: ('OK', 'Request fulfilled, document follows'),
		201: ('Created', 'Document created, URL follows'),
		202: ('Accepted',
					'Request accepted, processing continues off-line'),
		203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
		204: ('No Content', 'Request fulfilled, nothing follows'),
		205: ('Reset Content', 'Clear input form for further input.'),
		206: ('Partial Content', 'Partial content follows.'),

		300: ('Multiple Choices',
					'Object has several resources -- see URI list'),
		301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
		302: ('Found', 'Object moved temporarily -- see URI list'),
		303: ('See Other', 'Object moved -- see Method and URL list'),
		304: ('Not Modified',
					'Document has not changed since given time'),
		305: ('Use Proxy',
					'You must use proxy specified in Location to access this '
					'resource.'),
		307: ('Temporary Redirect',
					'Object moved temporarily -- see URI list'),

		400: ('Bad Request',
					'Bad request syntax or unsupported method'),
		401: ('Unauthorized',
					'Login failed'),
		402: ('Payment Required',
					'No payment -- see charging schemes'),
		403: ('Forbidden',
					'Request forbidden -- authorization will not help'),
		404: ('Not Found', 'Nothing matches the given URI'),
		405: ('Method Not Allowed',
					'Specified method is invalid for this server.'),
		406: ('Not Acceptable', 'URI not available in preferred format.'),
		407: ('Proxy Authentication Required', 'You must authenticate with '
					'this proxy before proceeding.'),
		408: ('Request Timeout', 'Request timed out; try again later.'),
		409: ('Conflict', 'Request conflict.'),
		410: ('Gone',
					'URI no longer exists and has been permanently removed.'),
		411: ('Length Required', 'Client must specify Content-Length.'),
		412: ('Precondition Failed', 'Precondition in headers is false.'),
		413: ('Request Entity Too Large', 'Entity is too large.'),
		414: ('Request-URI Too Long', 'URI is too long.'),
		415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
		416: ('Requested Range Not Satisfiable',
					'Cannot satisfy request range.'),
		417: ('Expectation Failed',
					'Expect condition could not be satisfied.'),

		500: ('Internal Server Error', 'Server got itself in trouble'),
		501: ('Not Implemented',
					'Server does not support this operation'),
		502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
		503: ('Service Unavailable',
					'The server cannot process the request due to a high load'),
		504: ('Gateway Timeout',
					'The gateway server did not receive a timely response'),
		505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
		}


sha1hash=hashlib.sha1(config.trakt_pass).hexdigest()

def sendRequest(mediaelement):
	if mediaelement["process"] < 80 and mediaelement["process"] > 2:
		response = watching(mediaelement)
	else:
		response = scrobble(mediaelement)
		if not response:
			logger.debug("Scrobble failed, trying to mark as seen manually...")
			response = seen(mediaelement)
	return response



def seen(mediaelement):
	if mediaelement["type"]=="series":
		action="show/episode/seen"

		postdata={
			"username": config.trakt_user,
			"password": sha1hash,
			"tvdb_id": mediaelement["tvdb_id"],
			"title": mediaelement["name"],
			#"year": dict["year"],
			"episodes": [
        		{
            		"season": mediaelement["season"],
            		"episode": mediaelement["episode"]
        		}
   			]
		}

	if mediaelement["type"]=="movie":
		action="movie/seen"

		postdata={
    		"username": config.trakt_user,
    		"password": sha1hash,
    		"movies": [
        		{
            		"imdb_id": mediaelement["imdb_id"],
            		"title": mediaelement["name"],
            		"year": mediaelement["year"],
            		#"plays": 1,
            		#"last_played": mediaelement["lastviewedstamp"]
        		}
    		]
		}
	return send(action, postdata, mediaelement)

def watching(mediaelement):
	if mediaelement["type"]=="series":
		action="show/watching"
		postdata={
    		"username": config.trakt_user,
    		"password": sha1hash,
    		#"imdb_id": "tt1520211",
    		"tvdb_id": mediaelement["tvdb_id"],
    		"title": mediaelement["name"],
    		#"year": 2010,
    		"season": mediaelement["season"],
    		"episode": mediaelement["episode"],
    		"progress": mediaelement["process"],
    		"duration": int(mediaelement["duration"]) / 60
    		#"plugin_version": "1.0",
    		#"media_center_version": "10.0",
    		#"media_center_date": "Dec 17 2010"
		}

	if mediaelement["type"]=="movie":
		action="movie/watching"

		postdata={
    		"username": config.trakt_user,
    		"password": sha1hash,
    		"imdb_id": mediaelement["imdb_id"],
    		"title": mediaelement["name"],
    		"year": mediaelement["year"],
    		#"duration": 141,
    		"progress": mediaelement["process"],
    		"duration": int(mediaelement["duration"]) / 60
    		#"plugin_version": "1.0",
    		#"media_center_version": "10.0",
    		#"media_center_date": "Dec 17 2010"
		}

	return send(action, postdata, mediaelement)

def scrobble(mediaelement):
	if mediaelement["type"]=="series":
		action="show/scrobble"
		
		postdata={
			"username": config.trakt_user,
			"password": sha1hash,
			"tvdb_id": mediaelement["tvdb_id"],
			"title": mediaelement["name"],
			#"year": dict["year"],
			"progress": mediaelement["process"],
			"season": mediaelement["season"],
			"episode": mediaelement["episode"],
			"duration": int(mediaelement["duration"]) / 60
		}

	if mediaelement["type"]=="movie":
		action="movie/scrobble"

		postdata={
			"username": config.trakt_user,
			"password": sha1hash,
			"imdb_id": mediaelement["imdb_id"],
			"title": mediaelement["name"],
			"year": mediaelement["year"],
			# "plays": 1,
			"progress": mediaelement["process"],
			"duration": int(mediaelement["duration"]) / 60
			#"last_played": dict["lastviewedstamp"]
		}
	return send(action, postdata, mediaelement)
		


	
def send(action, postdata, mediaelement):
	url = "http://api.trakt.tv/{0}/{1}".format(action, config.trakt_key)
	try:
		logger.info(u"Sending infos for {0} \"{1}\" to trakt".format(mediaelement["type"], mediaelement["name"]))
	except:
		logger.info(u"Sending infos to trakt")
	logger.debug(u"Sending infos to trakt: URL: {0}, Data: {1}".format(url, postdata))

	try:
		request = urllib2.Request(url, json.dumps(postdata))
		response = urllib2.urlopen(request)
		response = response.read()
		response = json.loads(response)
		
	except urllib2.HTTPError, e:
		response = {'status' : 'failure', 'error' : responses[e.code][1]}
		#return None
	except urllib2.URLError, e:
		response = {'status' : 'failure', 'error' : e.reason[0]}
		#return None
	logger.debug("response: {0}".format(response))
	if response['status'] == 'success':
		#create an nfo file for later use...
		helper.makeNFO(mediaelement)
		#marking the id as scrobbled inside the database...
		if not action.split("/")[-1] == "watching":
			if config.use_database:
				helper.markScrobbled(mediaelement["id"])
		return True
	else:
		return None
