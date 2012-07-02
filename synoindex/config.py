import re, os, sys
from ConfigParser import SafeConfigParser, ConfigParser

configfile = "SynoDLNAtrakt.ini"

#TODO: check if everything we need is in config file...

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
	delete_logs = parser.getboolean('General','delete_logs')
	use_database = parser.getboolean('General','use_database')

	trakt_user = parser.get('Trakt', 'trakt_user')
	trakt_pass = parser.get('Trakt', 'trakt_pass')
	trakt_key = parser.get('Trakt', 'trakt_key')

	use_boxcar = parser.getboolean('Boxcar', 'use_boxcar')
	boxcar_username = parser.get('Boxcar', 'boxcar_username')

	debugmode = parser.getboolean('Advanced','debugmode')
	min_progress = parser.get('Advanced','min_progress')
	interval = parser.get('Advanced','interval')
	logtoconsole = parser.get('Advanced','logtoconsole')
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

	Config.add_section('Trakt')
	Config.set('Trakt','trakt_user','Username')
	Config.set('Trakt','trakt_pass', 'Password')
	Config.set('Trakt','trakt_key', 'API-Key')

	Config.add_section('Boxcar')
	Config.set('Boxcar','use_boxcar', 0)
	Config.set('Boxcar','boxcar_username', '')

	Config.add_section('Advanced')
	Config.set('Advanced','min_progress', 80)
	Config.set('Advanced','logtoconsole', 0)
	Config.set('Advanced','interval', 24)
	Config.set('Advanced','debugmode', 0)

	Config.write(cfgfile)
	cfgfile.close()
	print "Config file: {0} generated. please reastart me now.".format(configfile)
	sys.exit(0)

