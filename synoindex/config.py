import re, os, sys
from ConfigParser import SafeConfigParser, ConfigParser

configfile = "SynoDLNAtrakt.ini"

if os.path.exists(configfile):
	parser = SafeConfigParser()
	parser.read(configfile)
	
	accesslog = parser.get('General', 'accesslog')
	psql = parser.get('General', 'psql')
	seriesdir = parser.get('General', 'seriesdir').split(',')
	moviedir = parser.get('General', 'moviedir').split(',')
	scrobble_series = parser.getboolean('General', 'scrobble_series')
	scrobble_movies = parser.getboolean('General', 'scrobble_movies')
	try_guessing = parser.getboolean('General', 'try_guessing')
	trakt_user = parser.get('Trakt', 'trakt_user')
	trakt_pass = parser.get('Trakt', 'trakt_pass')
	trakt_key = parser.get('Trakt', 'trakt_key')
	delete_logs = parser.getboolean('General','delete_logs')
	use_database = parser.getboolean('General','use_database')
	loglevel = parser.get('General','loglevel')
	min_progress = parser.get('Trakt','min_progress')
else:
	Config = ConfigParser()
	cfgfile = open(configfile,'w')

	# add the settings to the structure of the file, and lets write it out...
	Config.add_section('General')
	Config.set('General','accesslog','/var/log/lighttpd/access.log')
	Config.set('General','psql', '/usr/syno/pgsql/bin/psql')
	Config.set('General','seriesdir', '/path/to/seriesdir/,/another/path/to/dir/')
	Config.set('General','moviedir', '/path/to/moviedir/,/another/path/to/dir/')
	Config.set('General','scrobble_series', 1)
	Config.set('General','scrobble_movies', 1)
	Config.set('General','try_guessing', 1)
	Config.set('General','delete_logs', 0)
	Config.set('General','use_database', 1)
	Config.set('General','loglevel', 'INFO')

	Config.add_section('Trakt')
	Config.set('Trakt','trakt_user','Username')
	Config.set('Trakt','trakt_pass', 'Password')
	Config.set('Trakt','trakt_key', 'API-Key')
	Config.set('Trakt','min_progress', 80)
	Config.write(cfgfile)
	cfgfile.close()
	print "Config file: {0} generated. please reastart me now.".format(configfile)
	sys.exit(0)

