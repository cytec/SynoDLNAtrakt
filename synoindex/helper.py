import re, os
from ConfigParser import SafeConfigParser
from xml.dom.minidom import parse, parseString
from lib.themoviedb import tmdb
from lib.tvdb_api import tvdb_api
from synoindex import config
from synoindex import db
from synoindex.logger import logger

seriesregex = "(?P<name>.*).?[sS](?P<season>\d{1,2})[eE|xX|epEP|\.|-]?(?P<episode>\d{1,2})"
movieregex = "(?P<name>.*).?\(?(?P<year>\d{4})\)?"


def getVideoPath(theid):
	#/usr/syno/pgsql/bin/psql mediaserver admin -tA -c "select path from video where id = theid"
	thepath = os.popen('{0} mediaserver admin -tA -c "select path from video where id = {1}"'.format(config.psql, theid)).read().strip()
	return thepath

def getVideoDuration(theid):
	#/usr/syno/pgsql/bin/psql mediaserver admin -tA -c "select duration from video where id = 13282"
	duration = os.popen('{0} mediaserver admin -tA -c "select duration from video where id = {1}"'.format(config.psql, theid)).read().strip()
	return duration

def isMediaType(theid):
	response = {}
	thepath = os.popen('{0} mediaserver admin -tA -c "select path from video where id = {1}"'.format(config.psql, theid)).read().strip()
	if thepath:
		for curdir in config.seriesdir:
			if curdir in thepath:
				response["directory"] = curdir
				response["type"] = "series"
				response["thepath"] = thepath
	 			return response
	
		for curdir in config.moviedir:
			if curdir in thepath:
				response["directory"] = curdir
				response["type"] = "movie"
				response["thepath"] = thepath
	 			return response
	return False

def getSeries(filepath, curdir):
	myfilestring = filepath.replace(curdir,'')
	series, season, filename = myfilestring.split('/')
	logger.debug("Splitting {0} -> Series: {1}, Season: {2}, Filename: {3}".format(filepath, series, season, filename))

def durationStamps(time):
	try:
		h, m, s = time.split(":")
		timestamp = int(h*60)
		timestamp = (timestamp + int(m))*60
		timestamp = (timestamp + int(s))
		logger.debug("timestamp for: {0} is {1}".format(time, timestamp))
	except:
		timestamp = time
		logger.debug("{0} seems to be a timestamp already".format(time))
	return timestamp

def getProcess(length, viewed):
	minpercent = 80
	length = durationStamps(length)
	viewed = durationStamps(viewed)
	percent = int(viewed) / (int(length) / 100)
	logger.debug("Duration: {0}s, Viewed: {1}s = {2}% watched".format(length, viewed, percent))
	return percent

def getDurationFromLog(id):
	dates = idtimes[id]
	startdate = dates[1]
	enddade = dates[-1]

	duration = enddade - startdate
	
	logger.debug("Fileid: " + str(id))
	logger.debug("Duration: " + str(duration))
	h, m, s = str(duration).split(":")
	time = int(h)*60
	time = (time + int(m))*60
	time = (time + int(s))
	logger.debug("Duration Timestamp: {0}".format(time))
	logger.debug("Last viewed: {0}, for: {1}".format(enddade, duration))
	return time, enddade

def mediaelementToDatabase(mediaelement):
	#create db if not exist...
	db.checkDB()
	myDB = db.DBConnection()
	myDB.upsert("scrobble",{'id': mediaelement["id"], 'lastviewed': mediaelement["lastviewedstamp"], 'process': mediaelement["process"], 'name':mediaelement["name"], 'thepath': mediaelement["thepath"], 'viewed':mediaelement["viewed"], 'duration':mediaelement["duration"], 'directory':mediaelement["directory"], 'type':mediaelement["type"]},{'id': mediaelement["id"]})
	if mediaelement["type"] == "series":
		myDB.upsert("scrobble",{'season': mediaelement["season"], 'episode': mediaelement["episode"], 'tvdb_id': mediaelement["tvdb_id"]},{'id': mediaelement["id"]})
	if mediaelement["type"] == "movie":
		myDB.upsert("scrobble",{'imdb_id': mediaelement["imdb_id"], 'year':mediaelement["year"]},{'id': mediaelement["id"]})

def markScrobbled(theid):
	db.checkDB()
	myDB = db.DBConnection()
	myDB.upsert("scrobble",{'scrobbled': 1},{'id': theid})

def mediaelementFromDatabase(theid):
	db.checkDB()
	myDB = db.DBConnection()
	response = myDB.select("SELECT * from scrobble WHERE id = {0}".format(theid))
	return response

def FileInDB(theid):
	db.checkDB()
	myDB = db.DBConnection()
	response = myDB.select("SELECT scrobbled from scrobble WHERE id = {0}".format(theid))
	return response

def checkNFO(filepath, nfotype):
	#check the nfo for the needed id stuff...
	#check if there is an nfo file... if not, fuck it and try to get infos from tvdb...
	if nfotype == "series":
		directory = os.path.dirname(filepath)
		directory = re.sub(r'Staffel \d{2}|Season \d{2}', '', directory)
		nfofile = directory + "tvshow.nfo"
		try:
			dom = parse(nfofile)
			seriesidTag = dom.getElementsByTagName('id')[0].toxml()
			seriesid=seriesidTag.replace('<id>','').replace('</id>','')
			try:
				nameTag = dom.getElementsByTagName('showtitle')[0].toxml()
				name=nameTag.replace('<showtitle>','').replace('</showtitle>','')
			except:
				nameTag = dom.getElementsByTagName('title')[0].toxml()
				name=nameTag.replace('<title>','').replace('</title>','')
			logger.debug("SeriesID for {0} is: {1}".format(name, seriesid))
			return seriesid, name
		except:
			logger.error("cant find/open file: {0}".format(nfofile))
			if config.try_guessing:
				logger.info("Trying to guess infos from Filename...")
				seriesname = os.path.basename(filepath)
				p = re.match(seriesregex, seriesname)
				name = p.group("name").replace(".", " ").strip()
				season = p.group("season")
				episode = p.group("episode")
				logger.debug("Type: {3}, Name: {0}, Season: {1}, Episode: {2}".format(name, season, episode, nfotype))
				t = tvdb_api.Tvdb()
				showinfo = t[name]	
				tvdb_id = showinfo["id"]
				realname = showinfo["seriesname"]
				year = showinfo["firstaired"]
				#logger.debug("tvdb gave the following keys: {0}".format(showinfo.data.keys()))
				logger.info("Found result for {0} -> Fullname: {1}, tvdb_id: {2}, Year: {3}".format(seriesname, realname, tvdb_id, year))
				return tvdb_id, realname
			else:
				logger.error("Please enable try_guessing in settings or place an tvshow.nfo for: {0}".format(directory))
			return 0

		

	if nfotype == "episode":
		filename, extension = os.path.splitext(filepath)
		nfofile = filename + ".nfo"
		try:
			dom = parse(nfofile)
			episodeTag = dom.getElementsByTagName('episode')[0].toxml()
			episode=episodeTag.replace('<episode>','').replace('</episode>','')
			seasonTag = dom.getElementsByTagName('season')[0].toxml()
			season=seasonTag.replace('<season>','').replace('</season>','')
			episodeTag = dom.getElementsByTagName('episode')[0].toxml()
			episode=episodeTag.replace('<episode>','').replace('</episode>','')
			logger.info('TVSHOW info -> Season: {0}, Episode: {1}'.format(season, episode))
			return season, episode
		except:
			logger.error("Cant find/open/parse file: {0}".format(nfofile))
			if config.try_guessing:
				logger.info("Trying to guess infos from Filename...")
				seriesname = os.path.basename(filepath)
				p = re.match(seriesregex, seriesname)
				name = p.group("name").replace(".", " ").strip()
				season = p.group("season")
				episode = p.group("episode")
				logger.debug("Type: {3}, Series: {0}, Season: {1}, Episode: {2}".format(seriesname, season, episode, nfotype)) 
				return season, episode
			else:
				logger.error("Please enable try_guessing in settings or place an nfo for: {0}".format(directory))
			return 0

	if nfotype == "movie":
		filename, extension = os.path.splitext(filepath)
		nfofile = filename + ".nfo"
		try:
			dom = parse(nfofile)
			tvdb_idtag = dom.getElementsByTagName('id')[0].toxml()
			tvdb_id=tvdb_idtag.replace('<id>','').replace('</id>','')
			nametag = dom.getElementsByTagName('title')[0].toxml()
			name=nametag.replace('<title>','').replace('</title>','')
			yeartag = dom.getElementsByTagName('year')[0].toxml()
			year=yeartag.replace('<year>','').replace('</year>','')
			logger.info('Movie info -> Name: {0}, Year: {1}, imdb_id: {2}'.format(name, year, tvdb_id))
			return season, episode
		except:
			logger.error("Cant find/open file: {0}".format(nfofile))
			if config.try_guessing:
				logger.info("Trying to guess infos from Filename...")
				
				try:
					moviename = os.path.basename(filepath)
					p = re.match(movieregex, moviename)
					name = p.group("name").replace("."," ").replace("-"," ").strip()
					year = p.group("year")
					searchstring = "{0} ({1})".format(name, year)
				except:
					moviename = os.path.dirname(filepath)
					directory, moviename = os.path.split(moviename)
					p = re.match(movieregex, moviename)
					name = p.group("name").replace("."," ").strip()
					year = p.group("year")
					searchstring = "{0} ({1})".format(name, year)

				logger.debug("Type: {3}, Name: {0}, Year: {1}, Searchstring: {2}".format(name, year, searchstring, nfotype))
				#we need imdb id for scrobbleing to trakt, so lets make a moviedb lookup here to get these infos (especially if there is no year in the name....)
				#this ALWAYS uses the first resault that comes from tmdb...
				results = tmdb.search(searchstring)
				if results:
					firstresult = results[0]
					movieinfo = firstresult.info()
					imdb_id = movieinfo["imdb_id"]
					#logger.debug("tmdb gave the following keys: {0}".format(movieinfo.keys()))
					title = movieinfo["original_name"]
					logger.info("Found result for {0} -> Fullname: {1} imdb_id: {2}".format(searchstring, title, imdb_id))
					return title, imdb_id, year
				else:
					logger.error("Can't find any matches for {0}: {1}".format(nfotype, searchstring))
			else:
				logger.error("Please enable try_guessing in settings or place an nfo for: {0}".format(filepath))
				return 0

def buildMediaElement(mediaelement, theid):
	#check if given id is already in Database and get the lastviewed value to compare if its the same entry.
	if mediaelement:
		logger.info("Processing File: {0}".format(mediaelement["thepath"]))
		logger.debug("Mediatype: {0}, Directory: {1}".format(mediaelement["type"], mediaelement["directory"]))
		mediaelement["id"] = theid
		mediaelement["duration"] = getVideoDuration(theid)
		mediaelement["viewed"], mediaelement["lastviewed"] = getDurationFromLog(theid)
		mediaelement["process"] = getProcess(mediaelement["duration"], mediaelement["viewed"])
		
		#quit here if process is not enough... (saves time)
		if int(mediaelement["process"]) < int(config.min_progress):
			logger.error("File with id: {0}, was watched {1}% we need at least {2}%... skipping it".format(mediaelement["id"], mediaelement["process"], config.min_progress))
			return None
		else:

			mediaelement["lastviewedstamp"] = calendar.timegm(mediaelement["lastviewed"].timetuple())
			#generate timestamp from lastviewed (datetime obj)
			#d = datetime.datetime.now()
			#calendar.timegm(d.timetuple())
	
			#timestamp is needed for scrobbling last viewed date and to save it in database...
	
			#generate datetime from timestamp
			#datetime.datetime.utcfromtimestamp(1341237828)
	
			if mediaelement["type"] == "series":
				mediaelement["tvdb_id"], mediaelement["name"] = checkNFO(mediaelement["thepath"], "series")
				mediaelement["season"], mediaelement["episode"] = checkNFO(mediaelement["thepath"], "episode")
		
			if mediaelement["type"] == "movie":
				try:
					mediaelement["name"], mediaelement["imdb_id"], mediaelement["year"] = checkNFO(mediaelement["thepath"], "movie")
				except:
					logger.error("cant make medialement")
					return None
			logger.debug("created mediaobject: {0}".format(mediaelement))
			#insert created infos in database...
			mediaelementToDatabase(mediaelement)
			return mediaelement
	else:
		logger.error("Seems not to be a mediafile that i currently support..")
		return None		