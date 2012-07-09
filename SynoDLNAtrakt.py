# Author: cytec <iamcytec@googlemail.com>
# URL: http://github.com/cytec/SynoDLNAtrakt/
#
# This file is part of SynoDLNAtrakt.

import os, sys, re, datetime, time, shutil
import calendar

from lib.apachelog import apachelog as apachelog
from synodlnatrakt.logger import logger
from synodlnatrakt.boxcar import BoxcarNotifier
from synodlnatrakt import helper
from synodlnatrakt import config
from synodlnatrakt import trakt

p = apachelog.parser(apachelog.formats['lighttpd'])
time_format = "[%d/%b/%Y:%H:%M:%S +0200]"

idtimes = {}

# Root path
path = os.path.dirname(os.path.abspath( __file__ ))

# Insert local directories into path
sys.path.insert(0, os.path.join(path, 'lib'))

#TODO: cleanup!

#check if debugmode is acitvated
try:
	debugfile = open('/var/packages/MediaServer/etc/dmsinfo.conf')
	filelines = debugfile.readlines()
	debugfile.close()
	value = filelines[-1].replace("loglevel_mediaservice=\"","").replace("\"\n","")
	if int(value) < 3:
		logger.error(u"MediaServer not running in Debugmode!")
		sys.exit(u"Please enable Debugmode for MediaServer first!")
	else:
		logger.debug(u"MediaServer running in Debugmode")
except:
	logger.error(u"Can't check if your MeidaServer runs in Debugmode or not...")

def getDurationFromLog(theid):
	dates = idtimes[theid]
	
	startdate = dates[0]
	try:
		enddate = dates[-1]
	except:
		enddate = startdate

	duration = enddate - startdate
	
	logger.debug(u"Fileid: " + str(theid))
	logger.debug(u"Viewed: " + str(duration))
	h, m, s = str(duration).split(":")
	time = int(h)*60
	time = (time + int(m))*60
	time = (time + int(s))
	logger.debug(u"Viewed Timestamp: {0}".format(time))
	logger.debug(u"Last viewed: {0}, for: {1}".format(enddate, duration))
	return time, enddate

def buildMediaElement(mediaelement, theid):
	#check if given id is already in Database and get the lastviewed value to compare if its the same entry.
	if mediaelement:
		logger.info(u"processing file: {0}".format(mediaelement["thepath"]))
		logger.debug(u"mediatype: {0}, directory: {1}".format(mediaelement["type"], mediaelement["directory"]))
		mediaelement["id"] = theid
		mediaelement["duration"] = helper.getVideoDuration(theid)
		mediaelement["viewed"], mediaelement["lastviewed"] = getDurationFromLog(theid)
		mediaelement["process"] = helper.getProcess(mediaelement["duration"], mediaelement["viewed"])
		
		#quit here if process is not enough... (saves time)
		if int(mediaelement["process"]) < int(config.min_progress):
			logger.error(u"File with the ID: {0}, has been viewed {1}% we need at least {2}%... skipping it".format(mediaelement["id"], mediaelement["process"], config.min_progress))
			return None
		else:
			#currently only used for movies... idk if its possible to scrobble this for series.
			#mediaelement["lastviewedstamp"] = calendar.timegm(mediaelement["lastviewed"].timetuple())
			mediaelement["lastviewedstamp"] = time.mktime(mediaelement["lastviewed"].timetuple())
			#generate timestamp from lastviewed (datetime obj)
			#d = datetime.datetime.now()
			#calendar.timegm(d.timetuple())
	
			#timestamp is needed for scrobbling last viewed date and to save it in database...
	
			#generate datetime from timestamp
			#datetime.datetime.utcfromtimestamp(1341237828)
			
			#handling for mediatype series
			if mediaelement["type"] == "series":
				try:
					mediaelement["tvdb_id"], mediaelement["name"] = helper.checkNFO(mediaelement["thepath"], "series")
					mediaelement["season"], mediaelement["episode"] = helper.checkNFO(mediaelement["thepath"], "episode")
				except:
					logger.error(u"Could not create {0} MediaElement".format(mediaelement["type"]))
					return None
			#handling for mediatype movies
			if mediaelement["type"] == "movie":
				try:
					mediaelement["name"], mediaelement["imdb_id"], mediaelement["year"] = helper.checkNFO(mediaelement["thepath"], "movie")
				except:
					logger.error(u"Could not create {0} MediaElement".format(mediaelement["type"]))
					return None

			#log the created mediaobject in debug mode
			logger.debug(u"MediaElement successfully created: {0}".format(mediaelement))
			
			#insert created infos in database if activated
			if config.use_database:
				helper.mediaelementToDatabase(mediaelement)
				
			return mediaelement
	else:
		logger.error(u"File with the ID: {0} seems not to be a media file that i currently support")
		return None


logger.info(u"Starting SynoDLNAtrakt...")

#check for accesslog and exit if not found
if not os.path.exists(config.accesslog):
	logger.info(u"{0} doesn't exist please check your settings and make sure you enabled MediaServers Debug mode".format(config.accesslog))
	sys.exit(1)


#this may should be moved to helper.py too

if os.path.getsize(config.accesslog) > 0:
	logger.info(u"Parsing MediaServer log file from: {0}".format(config.accesslog))
	for line in open(config.accesslog):
		try:
			data = p.parse(line)
			try:
				x = re.match(config.logregex, data["%r"])
				theid = x.group("theid")
				extension = x.group("ext")
			except:
				theid, extension = data["%r"].replace("GET /v/NDLNA/",'').replace(' HTTP/1.1','').split('.')
	
			if extension not in config.medialist:
				continue
			
			#calculate the actual date from the log (for timedelta calculations)
			thedate = datetime.datetime.fromtimestamp(time.mktime(time.strptime(data["%t"], time_format)))
			try:
				if not idtimes.has_key(theid):
					thedate = [thedate]
					idtimes[theid]=thedate
				else:
					datelist = idtimes[theid]
					checkdate = datelist[0]
					#first access plus 6 hours timeframe...
					expirationdate = checkdate + datetime.timedelta(hours=6)
					#if its between the 6hours timeframe, add it else skipp it...
					#print "First view: {0}, Falid till: {1}".format(checkdate, expirationdate)
					if expirationdate > thedate:
						datelist.append(thedate)
						idtimes[theid]=datelist
					else:
						#when its outside the timframe, try to overwrite it with the newer date...
						logger.debug("{0} is more than 6hours after the first access to: {1}".format(thedate, theid))
						logger.debug("Overwriting {0} with new startdate: {1}".format(theid, thedate))
						thedate = [thedate]
						idtimes[theid]=thedate
			except:
				logger.error(u"Sorry something went wrong here, can't create dictionary")
	          
		except:
			logger.error(u"Unable to parse line: {0}".format(line))
	logger.info(u"Parsing: {0} gave {1} entry(s)".format(config.accesslog, len(idtimes)))
	
	scrobblers = 0
	for key in idtimes.keys():
		mediaelement = helper.isMediaType(key)
		if mediaelement:
			if config.use_database:
				isinDB = helper.FileInDB(key)
				if not isinDB:
					scrobbledict = buildMediaElement(mediaelement, key)
					if scrobbledict:
						trakt.scrobble(scrobbledict)
						scrobblers = scrobblers + 1
				else:
					logger.info(u"File with id: \"{0}\" is already in Database and scrobbled to trakt. Skipping it".format(key))
			else:
				scrobbledict = buildMediaElement(mediaelement, key)
				if scrobbledict:
					trakt.scrobble(scrobbledict)
					scrobblers = scrobblers + 1
	
	#send boxcar notifications if activated
	if config.use_boxcar:
		if scrobblers > 0:
			box = BoxcarNotifier()
			box._notifyBoxcar(u"SynoDLNAtrakt","Scrobbled {0} of {1} entrys to trakt".format(scrobblers, len(idtimes)))

	#move accesslog away for faster handling on the next time ;)
	if config.delete_logs:
		if not os.path.exists(path + "/accesslog-backups/"):
			os.makedirs(path + "/accesslog-backups/")
		newlogpath = path + "/accesslog-backups/{0}-access.log".format(datetime.date.today())
		
		shutil.copy(config.accesslog, newlogpath)
		#truncate accesslog (jsut clean it)
		open(config.accesslog, 'w').close()
		logger.info(u"{0} moved to backup directory: {1}".format(config.accesslog, newlogpath))
else:
	logger.info(u"{0} seems to be empty, please play some stuff first".format(config.accesslog))		