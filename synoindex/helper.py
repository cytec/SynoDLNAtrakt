import re, os
from ConfigParser import SafeConfigParser
from xml.dom.minidom import parse, parseString
from lib.themoviedb import tmdb
from lib.tvdb_api import tvdb_api
from synoindex import config

seriesregex = "(?P<name>.*).?[sS](?P<season>\d{1,2})[eE|xX|epEP|\.|-]?(?P<episode>\d{1,2})"
movieregex = "(?P<name>.*).?(?P<year>\d{4})"


def getVideoPath(theid):
	#/usr/syno/pgsql/bin/psql mediaserver admin -tA -c "select path from video where id = theid"
	return "/volume1/Datengrab/Serien/Psych/Staffel 04/Psych.s04e14.Spagat.zwischen.Attentat.und.Heldentat.SD.DVD.avi"

def getVideoDuration(theid):
	#/usr/syno/pgsql/bin/psql mediaserver admin -tA -c "select duration from video where id = 13282"
	return 2478


def isMediaType(filepath):
	response = {}
	for curdir in config.seriesdir:
  		if curdir in filepath:
  			response["directory"] = curdir
  			response["type"] = "series"
   			return response

  	for curdir in config.moviedir:
  		if curdir in filepath:
  			response["directory"] = curdir
  			response["type"] = "movie"
   			return response
	return False


def getSeries(filepath, curdir):
	myfilestring = filepath.replace(curdir,'')
	series, season, filename = myfilestring.split('/')

	print "DEBUG\t: splitting {0} -> Series: {1}, Season: {2}, Filename: {3}".format(filepath, series, season, filename)

def durationStamps(time):
  	h, m, s = time.split(":")
  	time = int(h*60)
  	time = (time + int(m))*60
  	time = (time + int(s))
  	return time

def getProcess(length, viewed):
  	minpercent = 80
  	length = durationStamps(length)
  	viewed = durationStamps(viewed)
  	percent = viewed / (length / 100)
  	print "DEBUG\t: Duration: {0}s, Viewed: {1}s = {2}% watched".format(length, viewed, percent)
  	return percent
  	# if percent > 80:
  	#   print "going to scrobble"
  	# else:
  	#   print "{0}% is not enoutgh to scrobble... you need at least {1}".format(percent, minpercent)


def checkNFO(filepath, nfotype):
	#check the nfo for the needed id stuff...
	#check if there is an nfo file... if not, fuck it and try to get infos from tvdb...
	if nfotype == "series":
		directory = os.path.dirname(filepath)
		directory = re.sub(r'Staffel \d{2}|Season \d{2}', '', directory)
		# nfofile = directory + "tvshow.nfo"
		nfofile = "tvshow.nfo"
		try:
			dom = parse(nfofile)
			seriesidTag = dom.getElementsByTagName('id')[0].toxml()
			seriesid=seriesidTag.replace('<id>','').replace('</id>','')
			nameTag = dom.getElementsByTagName('showtitle')[0].toxml()
			name=nameTag.replace('<showtitle>','').replace('</showtitle>','')
			print "DEBUG\t: SeriesID for {0} is: {1}".format(name, seriesid)
			return seriesid, name
		except:
			print "ERROR\t: cant find/open file: {0}".format(nfofile)
			return 0

		#new way:
		if os.fileexist("tvshow.nfo"):
			#do xml parsing
		else:
			print "DEBUG\t: No tvshow.nfo found..."
			if config.try_guessing:
				print "DEBUG\t: Trying to guess infos from Filename..."
				seriesname = os.path.basename(filepath)
				p = re.match(seriesregex, seriesname)
				name = p.group("name").replace(".", " ").strip()
				season = p.group("season")
				episode = p.group("episode")
				print "DEBUG\t: Type: {3}, Name: {0}, Season: {1}, Episode: {2}".format(name, season, episode, nfotype) 
				t = tvdb_api.Tvdb()
				showinfo = t[name]	
				tvdb_id = showinfo["id"]
				realname = showinfo["seriesname"]
				year = showinfo["firstaired"]
				print "DEBUG\t: tvdb gave the following keys: {0}".format(showinfo.data.keys())
				print "DEBUG\t: Found result for {0} -> Fullname: {1}, tvdb_id: {2}, Year: {3}".format(name, realname, tvdb_id, year)
				return tvdb_id, realname
			else:
				"ERROR\t: Please enable try_guessing in settings or place an tvshow.nfo for: {0}".format(directory)
				return 0
		

	if nfotype == "episode":
		filename, extension = os.path.splitext(filepath)
		nfofile = filename + ".nfo"
		try:
			dom = parse(nfofile)
			try:
				episodeTag = dom.getElementsByTagName('episode')[0].toxml()
				episode=episodeTag.replace('<episode>','').replace('</episode>','')
				seasonTag = dom.getElementsByTagName('season')[0].toxml()
				season=seasonTag.replace('<season>','').replace('</season>','')
				episodeTag = dom.getElementsByTagName('episode')[0].toxml()
				episode=episodeTag.replace('<episode>','').replace('</episode>','')
				print 'INFO\t: TVSHOW info -> Season: {0}, Episode: {1}'.format(season, episode)
				return season, episode
			except:
				episodeTag = dom.getElementsByTagName('episode')[0].toxml()
				episode=episodeTag.replace('<episode>','').replace('</episode>','')
				seasonTag = dom.getElementsByTagName('season')[0].toxml()
				season=seasonTag.replace('<season>','').replace('</season>','')
				episodeTag = dom.getElementsByTagName('episode')[0].toxml()
				episode=episodeTag.replace('<episode>','').replace('</episode>','')
				print 'ERROR\t: unable to parse {0}'.format(filepath)
				return 0
		except:
			print "ERROR\t: Cant find/open file: {0}".format(nfofile)
			return 0

		#new way:
		if os.fileexist(nfofile):
			#do xml parsing
		else:
			print "DEBUG\t: {0} not found...".format(nfofile)
			if config.try_guessing:
				print "DEBUG\t: Trying to guess infos from Filename..."
				seriesname = os.path.basename(filepath)
				p = re.match(seriesregex, seriesname)
				name = p.group("name").replace(".", " ").strip()
				season = p.group("season")
				episode = p.group("episode")
				print "DEBUG\t: Type: {3}, Series: {0}, Season: {1}, Episode: {2}".format(name, season, episode, nfotyoe) 
				return season, episode
			else:
				"ERROR\t: Please enable try_guessing in settings or place an tvshow.nfo for: {0}".format(directory)
				return 0

	if nfotype == "movie":
		filename, extension = os.path.splitext(filepath)
		nfofile = filename + ".nfo"
		try:
			dom = parse(nfofile)
			try:
				tvdb_idtag = dom.getElementsByTagName('tvdb_id')[0].toxml()
				tvdb_id=tvdb_idtag.replace('<tvdb_id>','').replace('</tvdb_id>','')
				nametag = dom.getElementsByTagName('name')[0].toxml()
				name=nametag.replace('<name>','').replace('</name>','')
				yeartag = dom.getElementsByTagName('year')[0].toxml()
				year=yeartag.replace('<year>','').replace('</year>','')
				print 'INFO\t: Movie info -> Name: {0}, Year: {1}, imdb_id: {2}'.format(name, year, tvdb_id)
				return season, episode
			except:
				print 'ERROR\t: unable to parse {0}'.format(filepath)
				return 0
		except:
			print "ERROR\t: Cant find/open file: {0}".format(nfofile)
			return 0

		#new way:
		if os.fileexist(nfofile):
			#do xml parsing
		else:
			print "DEBUG\t: {0} not found...".format(nfofile)
			if config.try_guessing:
				print "DEBUG\t: Trying to guess infos from Filename..."
				moviename = os.path.basename(movie)
				p = re.match(movieregex, moviename)
				name = p.group("name").replace("."," ").strip()
				year = p.group("year")
				searchstring = "{0} ({1})".format(name, year)
				print "DEBUG\t: Type: {3}, Name: {0}, Year: {1}, Searchstring: {2}".format(name, year, searchstring, nfotype)
				#we need imdb id for scrobbleing to trakt, so lets make a moviedb lookup here to get these infos (especially if there is no year in the name....)
				#this ALWAYS uses the first resault that comes from tmdb...
				results = tmdb.search(searchstring)
				if results:
					firstresult = results[0]
					movieinfo = firstresult.info()
					imdb_id = movieinfo["imdb_id"]
					#print "DEBUG: tmdb gave the following keys: {0}".format(movieinfo.keys())
					title = movieinfo["original_name"]
					print "DEBUG: Found result for {0} -> Fullname: {1} imdb_id: {2}".format(searchstring, title, imdb_id)
					return title, imdb_id, year
				else:
					print "ERROR: Can't find any matches for {0}: {1}".format(mediatype, searchstring)
			else:
				"ERROR\t: Please enable try_guessing in settings or place an nfo for: {0}".format(filepath)
				return 0