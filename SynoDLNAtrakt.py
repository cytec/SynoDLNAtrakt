import os, sys, re, datetime, time, shutil
from synoindex import helper
from synoindex import config
from synoindex import trakt
import calendar

from lib.apachelog import apachelog as apachelog
from synoindex.logger import logger


p = apachelog.parser(apachelog.formats['lighttpd'])
time_format = "[%d/%b/%Y:%H:%M:%S +0200]"

idtimes = {}

# Root path
path = os.path.dirname(os.path.abspath( __file__ ))

# Insert local directories into path
sys.path.insert(0, os.path.join(path, 'lib'))

#TODO: cleanup!

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

def buildMediaElement(mediaelement, theid):
	#check if given id is already in Database and get the lastviewed value to compare if its the same entry.
	if mediaelement:
		logger.info("Processing File: {0}".format(mediaelement["thepath"]))
		logger.debug("Mediatype: {0}, Directory: {1}".format(mediaelement["type"], mediaelement["directory"]))
		mediaelement["id"] = theid
		#mediaelement["thepath"] = helper.getVideoPath(theid)
		mediaelement["duration"] = helper.getVideoDuration(theid)
		mediaelement["viewed"], mediaelement["lastviewed"] = getDurationFromLog(theid)
		mediaelement["process"] = helper.getProcess(mediaelement["duration"], mediaelement["viewed"])
		
		#quit here if process is not enough... (saves time)
		if int(mediaelement["process"]) < int(config.min_progress):
			logger.error("{0}, was watched {1}% we need at least {2}%... skipping it".format(mediaelement["thepath"], mediaelement["process"], config.min_progress))
			return None
		else:
			#generate timestamp from lastviewed (datetime obj)
			#d = datetime.datetime.now()
			#calendar.timegm(d.timetuple())
	
			#timestamp is needed for scrobbling last viewed date and to save it in database...
	
			#generate datetime from timestamp
			#datetime.datetime.utcfromtimestamp(1341237828)
	
			if mediaelement["type"] == "series":
				mediaelement["tvdb_id"], mediaelement["name"] = helper.checkNFO(mediaelement["thepath"], "series")
				mediaelement["season"], mediaelement["episode"] = helper.checkNFO(mediaelement["thepath"], "episode")
		
			if mediaelement["type"] == "movie":
				try:
					mediaelement["name"], mediaelement["imdb_id"], mediaelement["year"] = helper.checkNFO(mediaelement["thepath"], "movie")
				except:
					logger.error("cant make medialement")
					return None
			logger.debug("created mediaobject: {0}".format(mediaelement))
			#insert created infos in database...
			return mediaelement
	else:
		logger.error("Seems not to be a mediafile that i currently support..")
		return None



medialist = [ "avi","mkv","mov","mp4","m4v","ts","hdmov","wmv","mpg","mpeg","xvid"]
logregex = ".*(?P<theid>\d{5})\.(?P<ext>\w{3,5})"

logger.info("Starting SynoDLNAtrakt...")

if not os.path.exists(config.accesslog):
	logger.info("{0} doesn't exist please check your settings and make sure you anabled MediaServers Debug mode".format(config.accesslog))
	sys.exit(1)


#this may should be moved to helper.py too

if os.path.getsize(config.accesslog) > 0:
	logger.info("Parsing MediaServer log file from: {0}".format(config.accesslog))
	for line in open(config.accesslog):
		try:
			data = p.parse(line)
			try:
				x = re.match(logregex, data["%r"])
				theid = x.group("theid")
				extension = x.group("ext")
			except:
				theid, extension = data["%r"].replace("GET /v/NDLNA/",'').replace(' HTTP/1.1','').split('.')
	
			if extension not in medialist:
				continue
			
			#calculate the actual date from the log (for timedelta calculations)
			thedate = datetime.datetime.fromtimestamp(time.mktime(time.strptime(data["%t"], time_format)))
			try:
				if not idtimes.has_key(theid):
					thedate = [thedate]
					idtimes[theid]=thedate
				else:
					datelist = idtimes[theid]
					datelist.append(thedate)
					idtimes[theid]=datelist
			except:
				logger.error("Sorry something went wrong here, cant create dictionary")
	          
		except:
			logger.error("Unable to parse line: {0}".format(line))
	logger.info("Parsing for: {0} gave {1} entry(s)".format(config.accesslog, len(idtimes)))
	
	for key in idtimes.keys():
		mediaelement = helper.isMediaType(key)
		if mediaelement:
			scrobbledict = buildMediaElement(mediaelement, key)
			if scrobbledict:
				trakt.scrobble(scrobbledict)
					
	
	
	#move accesslog away for faster handling on the next time ;)
	if config.delete_logs:
		if not os.path.exists(path + "/accesslog-backups/"):
			os.makedirs(path + "/accesslog-backups/")
		newlogpath = path + "/accesslog-backups/{0}-access.log".format(datetime.date.today())
		
		shutil.copy(config.accesslog, newlogpath)
		#truncate accesslog (jsut clean it)
		open(config.accesslog, 'w').close()
		logger.info("{0} moved to backup directory: {1}".format(config.accesslog, newlogpath))
else:
	logger.info("{0} seems to be empty, please play some stuff first".format(config.accesslog))		