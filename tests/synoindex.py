# Author: cytec <iamcytec@googlemail.com>
# URL: http://github.com/cytec/SynoDLNAtrakt/
#
# This file is part of SynoDLNAtrakt.

import os, sys, re, datetime, time
from ConfigParser import SafeConfigParser
from lib.apachelog import apachelog as apachelog
#import apachelog
import synoindex.helper as helper
import logging
from synoindex import db

import synoindex.trakt as trakt

import hashlib
import simplejson as json

# Root path
path = os.path.dirname(os.path.abspath( __file__ ))

# Insert local directories into path
sys.path.insert(0, os.path.join(path, 'lib'))

parser = SafeConfigParser()
parser.read(path + '/synoindex.ini')

accesslog = parser.get('General', 'accesslog')
psql = parser.get('General', 'psql')
seriesdir = parser.get('General', 'seriesdir').split(',')
print seriesdir, psql
#print accesslog

logging.basicConfig(filename='synoDLNAtrakt.log',format='%(asctime)s: %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)

def Log(string):
    # Probably want to pass through log type along with string. Can alsonuse logging.debug(string) and logging.warning(string)
    logging.info(string)
    print string


#read the accesslog
medialist = [ "avi", "mkv"]
p = apachelog.parser(apachelog.formats['lighttpd'])

# timestring = "2005-09-01 12:30:09"
# time_format = "%Y-%m-%d %H:%M:%S"

# timestring = "[20/Jun/2012:21:58:21 +0200]"
time_format = "[%d/%b/%Y:%H:%M:%S +0200]"

# print datetime.datetime.fromtimestamp(time.mktime(time.strptime(timestring, time_format)))
idtimes = {}

for line in open(accesslog):
        try:
           data = p.parse(line)
           #print data["%t"], data["%r"]

           #split request into id and ext
           theid, extension = data["%r"].replace("GET /v/NDLNA/",'').replace(' HTTP/1.1','').split('.')

           if extension not in medialist:
           	# print extension
           	continue
           
           #calculate the actual date from the log (for timedelta calculations)
           thedate = datetime.datetime.fromtimestamp(time.mktime(time.strptime(data["%t"], time_format)))

           # print theid, thedate
           #datelist = []
           
           #print idtimes[theid]
           try:
           	#idtimes[theid]=datelist
           	if not idtimes.has_key(theid):
           		thedate = [thedate]
           		idtimes[theid]=thedate
           	else:
           		# datelist = []
           	 	datelist = idtimes[theid]
           	  	datelist.append(thedate)
           	  	idtimes[theid]=datelist
           	 	#print "a"

           	#idtodict(theid, thedate)
           except:
           	print "no"

           # if not idtimes[theid]:
           # 	idtimes[theid][thedate]
           
        except:
           #sys.stderr.write("Unable to parse %s" % line)
           print "no"



def getDurations(id):

	dates = idtimes[id]
	startdate = dates[1]
	enddade = dates[-1]
	
	print "Fileid: " + str(id)
	print "Duration: " + str(enddade - startdate)


# for indexid in idtimes:
# 	getDurations(indexid)
# 	test = helper.getVideoPath(indexid)
# 	print "File Path: " + test

getDurations("13282")
filepath = helper.getVideoPath("13282")
print "File Path: " + filepath

if helper.fileIsSeries(filepath):
  print "DEBUG : {0} seems to be a series in the folder: {1}".format(filepath, helper.fileIsSeries(filepath))
  myseries = helper.getSeries(filepath, helper.fileIsSeries(filepath))
  series_id, series_name = helper.checkNFO(filepath,"series")
  series_season, series_episode = helper.checkNFO("Psych.s04e14.Spagat.zwischen.Attentat.und.Heldentat.SD.DVD.avi", "episode")
  #epid = helper.checkNFO(filepath, "episode")

  if series_id and series_season and series_episode:
    print "INFO : Sending infos to trakt.tv -> Name: {0} tvdbid: {1}, season {2}, episode {3}".format(series_name, series_id, series_season, series_episode)
  else:
    print "ERROR : Cant send informations for file {0} to trakt.tv".format(filepath)


trakt.scrobble(series_name, series_id, series_season, series_episode)
#trakt.testTrakt()


timestamp = helper.getVideoDuration("13282")
print time.gmtime(timestamp)
