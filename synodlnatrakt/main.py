from synodlnatrakt import helper, config
from synodlnatrakt.mediaelement import Episode, Movie
from synodlnatrakt import pgsql, trakt, db, pgsql, trakt, ui, versioncheck

import datetime, sys, os, subprocess

from synodlnatrakt.logger import logger

def setup():
	#create directorys...
	pass

def restart():
	logger.info(u"restarting SynoDLNAtrakt...")
	args = [sys.executable, os.path.join(config.basedir, "SynoDLNAtrakt.py"), "restart", "--config={0}".format(config.cfg_path)]
	logger.debug(u"restart args: {0}".format(args))
	#/var/packages/synodlnatrakt/scripts/start-stop-status start
	#maybe ill shoud use the spk python?
	os.execv(sys.executable, args)
	#subprocess.call(['/Library/Frameworks/Python.framework/Versions/2.7/bin/python', '/Users/workstation/Documents/github/SynoDLNAtrakt/SynoDLNAtrakt','restart',"--config={0}".format(config.cfg_path)])

def checkupdate():
	versioncheck.getVersion()
	versioncheck.checkGithub()

def scanlogs(force=False):
	if force:
		logger.info(u"FORCING SCROBBLE...")
	logger.info(u"READLOG STARTED")
	logelement = helper.parseLog()
	m = None
	for key in logelement.keys():
		mediatype = helper.get_media_type(key)
		if mediatype == "series":
			m = Episode(key, logelement[key], database=True)
		if mediatype == "movie":
			m = Movie(key, logelement[key], database=True)
		if m:
			if not m.progress:
				logger.info(u"generate new Mediaelement for: {0}".format(key))
				m.generate()
				if m.progress > config.min_progress:
					if config.watched_flags:
						helper.createWatchedFile(m)
					scrobble = trakt.sendRequest(m)
					if scrobble:
						m.scrobbled = 1
						m.progress = 100
				m.to_database()
			else:
				if m.progress > config.min_progress and m.scrobbled == 1:
					logger.debug(u"already scrobbled: {0}".format(key))

				if m.progress < config.min_progress:
					m._calc_runtime()
					m.to_database()

				if m.progress > config.min_progress and m.scrobbled != 1:
					logger.info(u"loaded Mediaelement from db: {0}".format(key))
					scrobble = trakt.sendRequest(m)
					if config.watched_flags:
						helper.createWatchedFile(m)
					if scrobble:
						m.scrobbled = 1
						m.progress = 100
					m.to_database()
	logger.info(u"READLOG FINISHED")


	response = {
		'status': 'success',
		'message': 'added {0} series/movies to synodlnatrakt'.format(len(logelement))
	}

	if len(logelement) > 0:
		ui.notifications.success("Yeah",'parsed {0} series/movies from log'.format(len(logelement)))

	return response

def import_mediaserver(force=False, max_entrys=20):
	counter = 0
	if force:
		logger.info(u"FORCING MEDIASERVER IMPORT...")
	logger.info(u"IMPORT FROM MEDIASERVER STARTED")
	dbresult = pgsql.session.query(pgsql.Video).order_by(pgsql.Video.date.desc()).limit(max_entrys)
	for result in dbresult:
		mediatype = helper.get_media_type(result.id)
		if mediatype == "series":
			m = Episode(result.id, None, database=True)
		elif mediatype == "movie":
			m = Movie(result.id, None, database=True)
		else:
			continue
		if m:
			if not m.path:
				logger.info(u"generate new Mediaelement for: {0}".format(result.id))
				m.generate()
				if m.progress > config.min_progress:
					scrobble = trakt.sendRequest(m)
					if scrobble:
						m.scrobbled = 1
						m.progress = 100
				m.to_database()
				counter = counter + 1
			else:
				#logger.info(u"already scrobbled: {0}".format(result.id))
				logger.debug(u"loaded Mediaelement from db: {0}".format(result.id))
				if m.progress > config.min_progress and m.scrobbled != 1:

					scrobble = trakt.sendRequest(m)
					if scrobble:
						m.scrobbled = 1
						m.progress = 100
					m.to_database()
				else:
					#m._calc_runtime()
					logger.debug(u"no changes")

	logger.info(u"IMPORT FROM MEDIASERVER FINISHED")

	response = {
		'status': 'success',
		'message': 'added {0} series/movies to synodlnatrakt'.format(counter)
	}
	ui.notifications.success("Yeah",'added {0} series/movies to synodlnatrakt'.format(counter))
	pgsql.session.remove()
	return response


def update_movies(force=False):
	if force:
		logger.info(u"FORCING TRAKT SYNC...")
	logger.info(u"TRAKT SYNC STARTED")
	logger.info(u"SYNCING MOVIES...")
	traktmovies = trakt.getWatched("movie")

	movielist = []

	for a in traktmovies:
		#print a
		movielist.append(a["imdb_id"])


	allmovies = db.session.query(db.Movies).filter(db.Movies.scrobbled == 0).all()

	for movie in allmovies:
		if movie.imdb_id in movielist:
			logger.info(u"Movie: {0} -> {1} marked as seen because of trakt".format(movie.imdb_id, movie.name))
			movie.progress = 100
			movie.scrobbled = 1
			movie.lastseen = datetime.datetime(2000,1,1).strftime('%Y-%m-%d %H:%M:%S')
			db.session.merge(movie)

	db.session.commit()


	traktratings = trakt.getRatings("movie")
	allmovies = db.session.query(db.Movies).all()

	ratings = []

	for movie in allmovies:
		ratings.append(u"{0}".format(movie.imdb_id))


	for a in traktratings:

		if a["imdb_id"] in ratings:

			result = (
				db.session.query(db.Movies)
					.filter(db.Movies.imdb_id == a["imdb_id"])
					.filter(db.Movies.rating != a["rating_advanced"]).first()
				)

			if result:
				logger.info(u"Setting rating for {0} to {1}".format(a["title"], a["rating_advanced"]))
				result.rating = a["rating_advanced"]
				db.session.merge(result)
				db.session.commit()

	update_series()
	db.session.remove()


def update_series():
	logger.info(u"SYNCING SERIES...")
	serieslist = []

	allseries = db.session.query(db.TVShows).all()

	for series in allseries:
		serieslist.append(u"{0}".format(series.tvdb_id))

	traktseries = trakt.getWatched("series")
	for show in traktseries:
		if show["tvdb_id"] in serieslist:
			for season in show["seasons"]:
				result = (
					db.session.query(db.TVEpisodes)
						.filter(db.TVEpisodes.show_id == show["tvdb_id"])
						.filter(db.TVEpisodes.season == season["season"])
						.filter(db.TVEpisodes.scrobbled == 0).all()
					)

				if result:
					logger.info(u"Watched {0} Season {1} Episodes {2}".format(show["title"], season["season"], season["episodes"]))

				for a in result:
					if a.episode in season["episodes"]:
						a.progress = 100
						a.scrobbled = 1
						a.lastseen = datetime.datetime(2000,1,1).strftime('%Y-%m-%d %H:%M:%S')
						db.session.merge(a)
						logger.info(u"marked {0}: {2}x{3} \"{1}\" as watched".format(show["title"], a.name, a.season, a.episode))
				db.session.commit()

	traktseries = trakt.getRatings("series")

	allepisodes = db.session.query(db.TVEpisodes).all()
	eplist = []
	for ep in allepisodes:
		eplist.append(ep.tvdb_id)

	for result in traktseries:
		if result["episode"]["tvdb_id"] in eplist:
			myep = (
				db.session.query(db.TVEpisodes)
					.filter(db.TVEpisodes.tvdb_id == result["episode"]["tvdb_id"])
					.filter(db.TVEpisodes.rating != result["rating_advanced"]).first()
				)

			if myep:
				logger.debug(u"Setting rating for {0} to {1}".format(result["episode"]["title"], result["rating_advanced"]))
				myep.rating = result["rating_advanced"]
				db.session.merge(myep)
				db.session.commit()

	logger.info(u"TRAKT SYNC ENDED")
	db.session.remove()

	myanswer = {
		u'status': u'success',
		u'message': u'Synced successfully'
	}
	ui.notifications.success("Yeah",'Synced successfully')
	db.session.remove()
	return myanswer
