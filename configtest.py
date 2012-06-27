import os, sys
from synoindex import helper

# Root path
path = os.path.dirname(os.path.abspath( __file__ ))

# Insert local directories into path
sys.path.insert(0, os.path.join(path, 'lib'))

from synoindex import config

print config.accesslog

theid = 1234

mediaelement = helper.isMediaType("/volume1/Datengrab/Filme/Psych/Staffel 04/Psych.s04e14.Spagat.zwischen.Attentat.und.Heldentat.SD.DVD.avi")

if mediaelement:
	buildMediaElement(mediaelement, theid)

	print mediaelement

def buildMediaElement(mediaelement, theid):
	if mediaelement:
		print "DEBUG:\tMediatype: {0}, Directory: {1}".format(mediaelement["type"], mediaelement["directory"])
		mediaelement["id"] = theid
		mediaelement["duration"] = helper.getVideoDuration(theid)
		mediaelement["viewed"] = helper.getVideoDuration(theid)
		mediaelement["process"] = helper.getProcess(mediaelement["duration"], mediaelement["viewed"])
	
		if mediaelement["type"] == "series":
			mediaelement["tvdb_id"], mediaelement["name"] = helper.checkNFO("/volume1/Datengrab/Filme/Psych/Staffel 04/Psych.s04e14.Spagat.zwischen.Attentat.und.Heldentat.SD.DVD.avi", "series")
			mediaelement["season"], mediaelement["episode"] = helper.checkNFO("/volume1/Datengrab/Filme/Psych/Staffel 04/Psych.s04e14.Spagat.zwischen.Attentat.und.Heldentat.SD.DVD.avi", "episode")
	
		if mediaelement["type"] == "movie":
			mediaelement["imdb_is"] = 1234
	
	else:
		print "xx Seems not to be a mediafile that i currently support.."
	
	print mediaelement	