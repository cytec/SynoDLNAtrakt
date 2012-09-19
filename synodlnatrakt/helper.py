# Author: cytec <iamcytec@googlemail.com>
# URL: http://github.com/cytec/SynoDLNAtrakt/
#
# This file is part of SynoDLNAtrakt.

import re, os, shutil, subprocess
from ConfigParser import SafeConfigParser
from xml.dom.minidom import parse, parseString
from lib.themoviedb import tmdb
from lib.tvdb_api import tvdb_api
from synodlnatrakt import config
from synodlnatrakt import db
from synodlnatrakt.logger import logger
from synodlnatrakt import encodingKludge as ek


seriesregex = "(?P<name>.*).?[sS](?P<season>\d{1,2})[eE|xX|epEP|\.|-]?(?P<episode>\d{1,2})"
movieregex = "(?P<name>.*).?\(?(?P<year>\d{4})\)?"


def getVideoPath(theid):
	#/usr/syno/pgsql/bin/psql mediaserver admin -tA -c "select path from video where id = theid"
	thepath = os.popen('{0} mediaserver admin -tA -c "select path from video where id = {1}"'.format(config.psql, theid)).read().strip()
	#get it as utf-8
	#thepath = os.popen('{0} mediaserver admin -tA -c "select path from video where id = {1}"'.format(config.psql, theid)).read().strip().decode('utf-8')
	return unicode(thepath, 'utf-8')

def getVideoDuration(theid):
	#/usr/syno/pgsql/bin/psql mediaserver admin -tA -c "select duration from video where id = 13282"
	duration = os.popen('{0} mediaserver admin -tA -c "select duration from video where id = {1}"'.format(config.psql, theid)).read().strip()
	return u"{0}".format(duration)

def isMediaType(theid):
	response = {}
	thepath = os.popen('{0} mediaserver admin -tA -c "select path from video where id = {1}"'.format(config.psql, theid)).read().strip()
	#thepath = ek.ek(os.path.abspath, thepath)
	thepath = unicode(thepath, 'utf-8')
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
	logger.debug(u"Splitting {0} -> Series: {1}, Season: {2}, Filename: {3}".format(filepath, series, season, filename))

def durationStamps(time):
	try:
		h, m, s = time.split(":")
		timestamp = int(h*60)
		timestamp = (timestamp + int(m))*60
		timestamp = (timestamp + int(s))
		logger.debug(u"timestamp for: {0} is {1}".format(time, timestamp))
	except:
		timestamp = time
		logger.debug(u"{0} seems to be a timestamp already".format(time))
	return timestamp

def getProcess(length, viewed):
	minpercent = 80
	length = durationStamps(length)
	viewed = durationStamps(viewed)
	percent = int(viewed) / (int(length) / 100)
	logger.debug(u"Duration: {0}s, Viewed: {1}s = {2}% watched".format(length, viewed, percent))
	if percent > 100:
		percent=100
	return percent

def getDurationFromLog(id):
	dates = idtimes[id]
	startdate = dates[1]
	enddade = dates[-1]

	duration = enddade - startdate
	
	logger.debug(u"Fileid: " + str(id))
	logger.debug(u"Duration: " + str(duration))
	h, m, s = str(duration).split(":")
	time = int(h)*60
	time = (time + int(m))*60
	time = (time + int(s))
	logger.debug(u"Duration Timestamp: {0}".format(time))
	logger.debug(u"Last viewed: {0}, for: {1}".format(enddade, duration))
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
	try:
		return response[0]["scrobbled"]
	except:
		return None

def checkNFO(filepath, nfotype):
	#check the nfo for the needed id stuff...
	#check if there is an nfo file... if not, fuck it and try to get infos from tvdb...
	if nfotype == "series":
		directory = os.path.dirname(filepath)
		directory = re.sub(r'Staffel \d{2}|Season \d{2}', '', directory)
		nfofile = os.path.join(directory, "tvshow.nfo")
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
			logger.debug(u"SeriesID for {0} is: {1}".format(name, seriesid))
			return seriesid, name
		except:
			#TODO: fix some unicode errors here...
			logger.error(u"cant find/open file: {0}".format(nfofile))
			if config.try_guessing:
				logger.info(u"Trying to guess infos from Filename...")
				seriesname = os.path.basename(filepath)
				p = re.match(seriesregex, seriesname)
				name = p.group("name").replace(".", " ").strip()
				season = p.group("season")
				episode = p.group("episode")
				logger.debug(u"Type: {3}, Name: {0}, Season: {1}, Episode: {2}".format(name, season, episode, nfotype))
				t = tvdb_api.Tvdb()
				showinfo = t[name]	
				tvdb_id = showinfo["id"]
				realname = showinfo["seriesname"]
				year = showinfo["firstaired"]
				#logger.debug("tvdb gave the following keys: {0}".format(showinfo.data.keys()))
				logger.info(u"Found result for {0} -> Fullname: {1}, tvdb_id: {2}, Year: {3}".format(seriesname, realname, tvdb_id, year))
				return tvdb_id, realname
			else:
				logger.error(u"Please enable try_guessing in settings or create an tvshow.nfo for: {0}".format(directory))
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
			logger.info(u'TVSHOW info -> Season: {0}, Episode: {1}'.format(season, episode))
			return season, episode
		except:
			logger.error(u"Cant find/open/parse file: {0}".format(nfofile))
			if config.try_guessing:
				logger.info(u"try to guess infos from Filename...")
				seriesname = os.path.basename(filepath)
				p = re.match(seriesregex, seriesname)
				name = p.group("name").replace(".", " ").strip()
				season = p.group("season")
				episode = p.group("episode")
				logger.debug(u"Type: {3}, Series: {0}, Season: {1}, Episode: {2}".format(seriesname, season, episode, nfotype)) 
				return season, episode
			else:
				logger.error(u"Please enable try_guessing in settings or create an .nfo for: {0}".format(directory))
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
			if name[:4].lower() in config.the_srings:
				name = name[4:] + ', ' + name[:4].strip()
			yeartag = dom.getElementsByTagName('year')[0].toxml()
			year=yeartag.replace('<year>','').replace('</year>','')
			logger.info(u'Movie info -> Name: {0}, Year: {1}, imdb_id: {2}'.format(name, year, tvdb_id))
			return name, tvdb_id, year
		except:
			logger.error(u"Cant find/open file: {0}".format(nfofile))
			if config.try_guessing:
				logger.info(u"try to guess infos from Filename...")
				
				try:
					moviename = os.path.basename(filepath)
					for junk in config.removejunk:
						moviename = moviename.replace(junk,'')
					p = re.match(movieregex, moviename)
					name = p.group("name").replace("."," ").replace("-"," ").strip()
					if name[:4].lower() in config.the_srings:
						name = name[4:] + ', ' + name[:4].strip()
					year = p.group("year")
					searchstring = "{0} ({1})".format(name, year)
				except:
					moviename = os.path.dirname(filepath)
					directory, moviename = os.path.split(moviename)
					p = re.match(movieregex, moviename)
					name = p.group("name").replace("."," ").strip()
					year = p.group("year")
					searchstring = "{0} ({1})".format(name, year)

				logger.debug(u"Type: {3}, Name: {0}, Year: {1}, Searchstring: {2}".format(name, year, searchstring, nfotype))
				#we need imdb id for scrobbleing to trakt, so lets make a moviedb lookup here to get these infos (especially if there is no year in the name....)
				#this ALWAYS uses the first resault that comes from tmdb...
				results = tmdb.search(searchstring)
				if results:
					firstresult = results[0]
					movieinfo = firstresult.info()
					imdb_id = movieinfo["imdb_id"]
					#logger.debug("tmdb gave the following keys: {0}".format(movieinfo.keys()))
					title = movieinfo["original_name"]
					logger.info(u"Found result for {0} -> Fullname: {1} imdb_id: {2}".format(searchstring, title, imdb_id))
					return title, imdb_id, year
				else:
					logger.error(u"Can't find any matches for {0}: {1}".format(nfotype, searchstring))
			else:
				logger.error(u"Please enable try_guessing in settings or create an .nfo for: {0}".format(filepath))
				return 0

def checktmdb(filename):
	filename = filename + ".tmdb"
	if os.path.exist(filename):
		f = open(filename, "r")
		tmdb_id = f.read()
		f.close()
		logger.info(u"found a tmdb file with the ID: {0}".format(tmdb_id))
		return tmdb_id
	else:
		return None

def makeNFO(mediaelement):
	nfopath = os.path.splitext(mediaelement["thepath"])[0] + ".nfo"
	doc = Document()
	synodlnatrakt = doc.createElement("SynoDLNAtrakt")
	doc.appendChild(synodlnatrakt)
	#the id
	id = doc.createElement("id")
	idtext = doc.createTextNode(mediaelement["imdb_id"])
	id.appendChild(idtext)
	#the title of the movie
	title = doc.createElement("title")
	titletext = doc.createTextNode(mediaelement["name"])
	title.append(titletext)

	year = doc.createElement("year")
	yeartext = doc.createTextNode(mediaelement["year"])
	year.append(yeartext)

	synodlnatrakt.append(id)
	synodlnatrakt.append(title)
	synodlnatrakt.append(year)
	try:
		f = open(nfopath,"w")
		f.write(doc.toprettyxml(indent="  "))
		f.close()
		logger.info(u"nfo file for {0} created".format(mediaelement["name"]))
	except:
		logger.error(u"unable to create nfo for {0}".format(mediaelement["name"]))


def processWatched(mediaelement):
	if config.delete_from_index:
		subprocess.call('synoindex','-d', mediaelement["thepath"])
		logger.info(u"Deleted {0} from the synoindex database".format(mediaelement["thepath"]))
	if mediaelement["type"] == "movie" and config.move_watched_movies and mediaelement["process"] > 80:
		dirname = os.path.dirname(mediaelement["thepath"])
		path, filename = os.path.split(dirname)
		#newpath = os.path.join(config.move_movies_to_dir, foldername)
		#os.rename(dirname, newpath)
		newfullpath = os.path.join(config.move_movies_to_dir, filename)
		if os.path.exists(mediaelement["thepath"]) and not os.path.exists(newfullpath):
			shutil.move(dirname, config.move_movies_to_dir)
			logger.info(u"Moved {0} to {1}".format(mediaelement["thepath"], newfullpath))
			if config.update_synoindex:
				try:
					subprocess.call('synoindex','-N', newfullpath, mediaelement["thepath"])
				except:
					subprocess.call('synoindex','-d', mediaelement["thepath"])
				logger.info(u"Updated synoindex for {0} with {1}".format(mediaelement["thepath"], newfullpath))
		else:
			logger.info(u"Directory already exists")

	if mediaelement["type"] == "series" and config.move_watched_series:
		pass
		#move it to the new movie dir...

