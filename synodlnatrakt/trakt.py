# Author: cytec <iamcytec@googlemail.com>
# URL: http://github.com/cytec/SynoDLNAtrakt/
#
# This file is part of SynoDLNAtrakt.


from synodlnatrakt import config
from synodlnatrakt.logger import logger
from lib import requests
import json

#config.sha1hash=hashlib.sha1(config.trakt_pass).hexdigest()


def sendRequest(mediaelement, returnStatus=False):
	if mediaelement.progress < config.min_progress and mediaelement.progress > 7:
		response = watching(mediaelement)
	elif mediaelement.progress < 7:
		logger.info(u"not scrobbleing because you watched less than 7%")
		response = "not scrobbleing because you watched less than 7%"
	else:
		response = scrobble(mediaelement)
		if not response:
			logger.debug(u"Scrobble failed, trying to mark as seen manually...")
			response = seen(mediaelement)
	return response


def seen(mediaelement, returnStatus=False):
	if mediaelement.mediatype=="series":
		req="/show/episode/seen/%%API_KEY%%"

		args={
			"username": config.trakt_user,
			"password": config.sha1hash,
			"tvdb_id": mediaelement.show_id,
			"title": mediaelement.name,
			#"year": dict["year"],
			"episodes": [
        		{
            		"season": mediaelement.season,
            		"episode": mediaelement.episode
        		}
   			]
		}

	if mediaelement.mediatype=="movie":
		req="/movie/seen/%%API_KEY%%"

		args={
    		"username": config.trakt_user,
    		"password": config.sha1hash,
    		"movies": [
        		{
            		"imdb_id": mediaelement.imdb_id,
            		"title": mediaelement.name,
            		"year": mediaelement.year,
            		#"plays": 1,
            		#"last_played": mediaelement["lastviewedstamp"]
        		}
    		]
		}
	return send("POST", req, args, returnStatus)

def watching(mediaelement, returnStatus=False):
	if mediaelement.mediatype=="series":
		req="/show/watching/%%API_KEY%%"
		args={
    		"username": config.trakt_user,
    		"password": config.sha1hash,
    		#"imdb_id": "tt1520211",
    		"tvdb_id": mediaelement.show_id,
    		"title": mediaelement.name,
    		#"year": 2010,
    		"season": mediaelement.season,
    		"episode": mediaelement.episode,
    		"progress": mediaelement.progress,
    		"duration": int(mediaelement.duration) / 60
    		#"plugin_version": "1.0",
    		#"media_center_version": "10.0",
    		#"media_center_date": "Dec 17 2010"
		}

	if mediaelement.mediatype=="movie":
		req="/movie/watching/%%API_KEY%%"

		args={
    		"username": config.trakt_user,
    		"password": config.sha1hash,
    		"imdb_id": mediaelement.imdb_id,
    		"title": mediaelement.name,
    		"year": mediaelement.year,
    		#"duration": 141,
    		"progress": mediaelement.progress,
    		"duration": int(mediaelement.duration) / 60
    		#"plugin_version": "1.0",
    		#"media_center_version": "10.0",
    		#"media_center_date": "Dec 17 2010"
		}

	return send("POST", req, args, returnStatus)

def scrobble(mediaelement, returnStatus=False):
	if mediaelement.mediatype=="series":
		req="/show/scrobble/%%API_KEY%%"
		
		args={
			"username": config.trakt_user,
			"password": config.sha1hash,
			"tvdb_id": mediaelement.show_id,
			"title": mediaelement.name,
			#"year": dict["year"],
			"progress": mediaelement.progress,
			"season": mediaelement.season,
			"episode": mediaelement.episode,
			"duration": int(mediaelement.duration) / 60
		}

	if mediaelement.mediatype=="movie":
		req="/movie/scrobble/%%API_KEY%%"

		args={
			"username": config.trakt_user,
			"password": config.sha1hash,
			"imdb_id": mediaelement.imdb_id,
			"title": mediaelement.name,
			"year": mediaelement.year,
			# "plays": 1,
			"progress": mediaelement.progress,
			"duration": int(mediaelement.duration) / 60
			#"last_played": dict["lastviewedstamp"]
		}
	return send("POST", req, args, returnStatus)
		
#additional stuff (add to list, create list, get ratings)

def addList(listname="Syno Stuff", description="Stuff i have to view", private="private", show_numbers=True, returnStatus=False):
	'''list can be private, friends, or public default is private'''
	req = "/lists/add/%%API_KEY%%"
	args={
			"username": config.trakt_user,
			"password": config.sha1hash,
    		"name": listname,
    		"description": description,
    		"privacy": private,
    		"show_numbers": "true",
    		"allow_shouts":"true"
	}
	return send("POST", req, args, returnStatus)

def add_to_list(mediaelement, listname="syno-stuff", returnStatus=False):
	
	if mediaelement.mediatype == "series" and listname != "watchlist":
		req = "/lists/items/add/%%API_KEY%%"
		args = {
			"username": config.trakt_user,
    		"password": config.sha1hash,
    		"slug": listname,
    		"items": [
    			{
    	        	"type": "episode",
    	        	"tvdb_id": mediaelement.tvdb_id,
    	        	"title": mediaelement.name,
    	        	"season": mediaelement.season,
    	        	"episode": mediaelement.episode
    	    	}
    		]
		}
	if mediaelement.mediatype == "movie" and listname == "watchlist":
		req = "/movie/watchlist/%%API_KEY%%"
		args = {
			"username": config.trakt_user,
    		"password": config.sha1hash,
    		"movies": [
    			{
    	        	"imdb_id": mediaelement.imdb_id,
    	        	"title": mediaelement.name,
    	        	"year": mediaelement.year,
    	    	}
    		]
		}
	return send("POST", req, args, returnStatus)
	
def rate(mediaelement, rating, returnStatus=False):
	'''rate an episode/movie'''

	if mediaelement.type == "series":
		req = "/rate/episode/%%API_KEY%%"
		args = {
			"username": config.trakt_user,
			"password": config.sha1hash,
			"tvdb_id": mediaelement.show_id,
			#"title": mediaelement.showname,
			#"year": mediaelement.year,
			"season": mediaelement.season,
			"episode": mediaelement.episode,
			"rating": rating
		}
	if mediaelement.type == "movie":
		req = "/rate/movie/%%API_KEY%%"
		args = {
			"username": config.trakt_user,
			"password": config.sha1hash,
			"imdb_id": mediaelement.imdb_id,
			"title": mediaelement.name,
			"year": mediaelement.year,
			"rating": rating
		}

	return send("POST", req, args, returnStatus)


def getWatched(mediatype, returnStatus=True):
	'''get watched movies/episodes'''
	if mediatype == "series":
		req = "/user/library/shows/watched.json/%%API_KEY%%/%%USERNAME%%"

	if mediatype == "movie":
		req = "/user/library/movies/watched.json/%%API_KEY%%/%%USERNAME%%"

	return send("GET", req, None, returnStatus)

def getRatings(mediatype, returnStatus=True):
	'''get ratings for episodes/movies'''
	if mediatype == "series":
		req = "/user/ratings/episodes.json/%%API_KEY%%/%%USERNAME%%/all"

	if mediatype == "movie":
		req = "/user/ratings/movies.json/%%API_KEY%%/%%USERNAME%%/all"

	return send("GET", req, None, returnStatus)


def send(method, req, args={}, returnStatus=False, debug=config.debugmode):
	'''GET/POST request to req URL with the given args...'''
	req = req.replace("%%API_KEY%%",config.trakt_key)
	req = req.replace("%%USERNAME%%",config.trakt_user)
	url = "http://api.trakt.tv/{0}".format(req)


	if method == "GET":
		response = requests.get(url)
	elif method == "POST":
		response = requests.post(url, json.dumps(args))

	else:
		return None

	logargs = args
	if logargs and "password" in logargs.keys():
		logargs["password"] = "XXXXXXXXXXXXX"

	logger.debug(u"Sending infos to trakt: URL: {0}, Data: {1}, Method: {2}".format(url, logargs, method))

	if response and debug:
		logger.debug(u"Trakt Response: {0}".format(response.json))

	if returnStatus:
		return response.json
	else:
		if response.json["status"] == "success":
			return True
		else:
			return None
	