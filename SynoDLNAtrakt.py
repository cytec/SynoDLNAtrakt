import os, sys, re, datetime, time, shutil
from synoindex import helper
from synoindex import config
from synoindex import trakt

from lib.apachelog import apachelog as apachelog


p = apachelog.parser(apachelog.formats['lighttpd'])
time_format = "[%d/%b/%Y:%H:%M:%S +0200]"

idtimes = {}

# Root path
path = os.path.dirname(os.path.abspath( __file__ ))

# Insert local directories into path
sys.path.insert(0, os.path.join(path, 'lib'))

def buildMediaElement(mediaelement, theid):
	if mediaelement:
		print "DEBUG:\tMediatype: {0}, Directory: {1}".format(mediaelement["type"], mediaelement["directory"])
		mediaelement["id"] = theid
		mediaelement["thepath"] = helper.getVideoPath(theid)
		mediaelement["duration"] = helper.getVideoDuration(theid)
		mediaelement["viewed"] = helper.getVideoDuration(theid)
		mediaelement["process"] = helper.getProcess(mediaelement["duration"], mediaelement["viewed"])
	
		if mediaelement["type"] == "series":
			mediaelement["tvdb_id"], mediaelement["name"] = helper.checkNFO(mediaelement["thepath"], "series")
			mediaelement["season"], mediaelement["episode"] = helper.checkNFO(mediaelement["thepath"], "episode")
	
		if mediaelement["type"] == "movie":
			try:
				mediaelement["name"], mediaelement["imdb_id"], mediaelement["year"] = helper.checkNFO(mediaelement["thepath"], "movie")
			except:
				print "ERROR\t: cant make medialement"
				return None

		return mediaelement
	else:
		print "xx Seems not to be a mediafile that i currently support.."
		return None
	
# mediaelement = helper.isMediaType(filename)

# if mediaelement:
# 	buildMediaElement(mediaelement, theid)

# 	print mediaelement


# mediaelement = helper.isMediaType(filename2)

# if mediaelement:
# 	buildMediaElement(mediaelement, theid2)

# 	print mediaelement

def getDurationFromLog(id):
	dates = idtimes[id]
	startdate = dates[1]
	enddade = dates[-1]

	duration = enddade - startdate
	
	print "Fileid: " + str(id)
	print "Duration: " + str(duration)
	h, m, s = str(duration).split(":")
	time = int(h*60)
	time = (time + int(m))*60
	time = (time + int(s))
	print "Duration Timestamp: {0}".format(time)
	#return enddade - startdate, enddade

medialist = [ "avi", "mkv"]

for line in open(config.accesslog):
	try:
		data = p.parse(line)
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
			print "ERROR"
          
	except:
           #sys.stderr.write("Unable to parse %s" % line)
		print "Unable to parse line: {0}".format(line)


for key in idtimes.keys():
	#getDurationFromLog(key)
	mediaelement = helper.isMediaType(key)
	if mediaelement:
		scrobbledict = buildMediaElement(mediaelement, key)
		if scrobbledict:
			# print scrobbledict
			# print ""
			# print ""
			trakt.scrobble(scrobbledict)
			print ""
			print ""
	else:
		print ""

#move accesslog away for faster handling on the next time ;)
# if config.delete_logs:
	# newlogpath = path + "/accesslog-backups/{0}-access.log".format(datetime.date.today())
	
	# shutil.copy(config.accesslog, newlogpath)
	# truncate accesslog (jsut clean it)
	# open(config.accesslog, 'w').close()
	# print "ACCESSLOG moved to backup directory..."	