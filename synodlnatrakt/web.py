from synodlnatrakt.mediaelement import Episode, Movie
from synodlnatrakt import db, trakt, config
from datetime import datetime, timedelta
from synodlnatrakt.timer import sched
from synodlnatrakt import logger, helper, main, mediaimport
from lib.bottle import route, post, template, run, static_file, request, response
from apscheduler.scheduler import Scheduler
import json
from lib.themoviedb import tmdb
import os, re
from synodlnatrakt import ui, versioncheck
from math import ceil
import logging

def check_auth(username, password):
	if config.username != "":
		if username == config.username and password == config.password:
			return True
		else:
			return False
	else:
		return True
    
def authenticate(msg_string = "Authenticate."):
    response.content_type = "application/json"
    message = {'message': msg_string}
    resp = message
    response.status = "401 - Unauthorized"
    response.headers['WWW-Authenticate'] = 'Basic realm="SynoDLNAtrakt"'

    return resp

def requires_auth(f):
    def decorated(*args, **kwargs):
        #print request.auth
        auth = request.auth
        if not auth: 
            return authenticate()
        elif not check_auth(auth[0],auth[1]):
            response.status = "401 - Unauthorized"
            return authenticate("HTTP Authentication Failed.")
        else:
            return f(*args, **kwargs)
    return decorated



class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

@route('/')
@requires_auth
def index():
	content = db.session.query(db.TVShows).filter(db.TVEpisodes.show_id == db.TVShows.tvdb_id).order_by(db.TVEpisodes.added.desc()).limit(10)
	return template('tvshow-list', content=content, topmenu=u"home", title=u"Home")

### Series Pages...
@route('/series')
@requires_auth
def index():
	content = db.session.query(db.TVShows).filter(db.TVEpisodes.show_id == db.TVShows.tvdb_id).order_by(db.TVShows.name.asc())
	return template('tvshow-list', content=content, topmenu=u"series", title=u"TV-Shows")

@route('/series/unseen')
@requires_auth
def index():
	content = db.session.query(db.TVEpisodes).filter(db.TVEpisodes.progress == 0).order_by(db.TVEpisodes.added.desc())
	return template('list', content=content, topmenu=u"series", title=u"TV-Shows - unseen")

@route('/series/unrated')
@requires_auth
def index():
	content = db.session.query(db.TVEpisodes).filter(db.TVEpisodes.rating == 0).order_by(db.TVEpisodes.added.desc())
	return template('list', content=content, topmenu=u"series", title=u"TV-Shows - unrated")

@route('/series/lastseen')
@requires_auth
def index():
	content = db.session.query(db.TVEpisodes).filter(db.TVEpisodes.progress > 75).order_by(db.TVEpisodes.lastseen.desc())
	return template('list', content=content, topmenu=u"series", title=u"TV-Shows - lastseen")

@route('/series/lastadded')
@requires_auth
def index():
	content = db.session.query(db.TVEpisodes).order_by(db.TVEpisodes.added.desc()).limit(30)
	return template('list', content=content, topmenu=u"series", title=u"TV-Shows - lastadded")


#list by cover not fanart...
@route('/series/cover')
@requires_auth
def index():
	content = db.session.query(db.TVShows).filter(db.TVEpisodes.show_id == db.TVShows.tvdb_id).order_by(db.TVShows.name.asc())
	return template('tvshow-list-cover', content=content, topmenu=u"series", title=u"TV-Shows - Cover view")

#view a specific series by its tvdb_id
@route('/series/view/<tvdb_id:int>')
@requires_auth
def index(tvdb_id):
	show = db.session.query(db.TVShows).filter(db.TVShows.tvdb_id == tvdb_id).first()
	content = db.session.query(db.TVEpisodes).filter(db.TVEpisodes.show_id == tvdb_id).order_by(db.TVEpisodes.season.desc()).order_by(db.TVEpisodes.episode.desc())
	return template('single-show', show=show, content=content, topmenu=u"series", title=u"TV-Shows - {0}".format(show.name))


### Movies Pages
@route('/movies')
@route('/movies/page/<mypage:int>')
@requires_auth
def index(mypage=1):
	myoffset = (mypage -1) * int(config.page_limit)
	count = db.session.query(db.Movies).order_by(db.Movies.name.asc()).count()
	pagination = Pagination(mypage, config.page_limit, count)
	content = db.session.query(db.Movies).order_by(db.Movies.name.asc()).offset(myoffset).limit(config.page_limit)
	return template('movie-list', pagination=pagination, content=content, topmenu=u"movie", title=u"Movies")

@route('/movies/unseen')
@route('/movies/unseen/page/<mypage:int>')
@requires_auth
def index(mypage=1):
	myoffset = (mypage -1) * int(config.page_limit)
	count = db.session.query(db.Movies).filter(db.Movies.progress == 0).order_by(db.Movies.name.asc()).count()
	pagination = Pagination(mypage, config.page_limit, count)
	content = db.session.query(db.Movies).filter(db.Movies.progress == 0).order_by(db.Movies.name.asc()).offset(myoffset).limit(config.page_limit)
	return template('movie-list', pagination=pagination, content=content, topmenu=u"movie", title=u"Movies - unseen")

@route('/movies/unrated')
@route('/movies/unrated/page/<mypage:int>')
@requires_auth
def index(mypage=1):
	myoffset = (mypage -1) * int(config.page_limit)
	count = db.session.query(db.Movies).filter(db.Movies.rating == 0).order_by(db.Movies.name.asc()).count()
	pagination = Pagination(mypage, config.page_limit, count)
	content = db.session.query(db.Movies).filter(db.Movies.rating == 0).order_by(db.Movies.name.asc()).offset(myoffset).limit(config.page_limit)
	return template('movie-list', pagination=pagination, content=content, topmenu=u"movie", title=u"Movies - unrated")

@route('/movies/lastseen')
@route('/movies/lastseen/page/<mypage:int>')
@requires_auth
def index(mypage=1):
	myoffset = (mypage -1) * int(config.page_limit)
	count = db.session.query(db.Movies).filter(db.Movies.progress > config.min_progress).order_by(db.Movies.lastseen.desc()).count()
	pagination = Pagination(mypage, config.page_limit, count)
	content = db.session.query(db.Movies).filter(db.Movies.progress > config.min_progress).order_by(db.Movies.lastseen.desc()).offset(myoffset).limit(config.page_limit)
	return template('movie-list', pagination=pagination, content=content, topmenu=u"movie", title=u"Movies - lastseen")

@route('/movies/lastadded')
@route('/movies/lastadded/page/<mypage:int>')
@requires_auth
def index(mypage=1):
	myoffset = (mypage -1) * int(config.page_limit)
	count = db.session.query(db.Movies).order_by(db.Movies.added.desc()).count()
	pagination = Pagination(mypage, config.page_limit, count)
	content = db.session.query(db.Movies).order_by(db.Movies.added.desc()).offset(myoffset).limit(config.page_limit)
	return template('movie-list', pagination=pagination, content=content, topmenu=u"movie", title=u"Movies - lastadded")

@route('/movies/cover')
@route('/movies/cover/page/<mypage:int>')
@requires_auth
def index(mypage=1):
	myoffset = (mypage -1) * int(config.page_limit)
	count = db.session.query(db.Movies).order_by(db.Movies.name.asc()).count()
	pagination = Pagination(mypage, config.page_limit, count)
	content = db.session.query(db.Movies).order_by(db.Movies.name.asc()).offset(myoffset).limit(config.page_limit)
	return template('movie-list-cover', content=content, topmenu=u"movie", title=u"Movies - Cover view")

@route('/movies/view/<synoindex>')
@requires_auth
def index(synoindex):
	movie = db.session.query(db.Movies).filter(db.Movies.synoindex == synoindex).first()
	return template('single-movie', movie=movie, topmenu=u"movie", title=u"Movie - {0}".format(movie.name))

@post('/update/movie')
@requires_auth
def index():
	name  = request.forms.get("name")
	movies = tmdb.search(name)
	return json.dumps(movies)

# @route('/save/movie/<synoindex>/<imdb_id>')
# def index(synoindex, imdb_id):
# 	result = helper.updateMovie(synoindex, imdb_id)
# 	return result

@post('/search')
def index():
	whattosearch = request.forms.get("searchfor")
	searchterm = request.forms.get("searchterm")
	searchterm = searchterm.decode('utf-8')
	if whattosearch == "series":
		result = db.session.query(db.TVShows).filter(db.TVShows.name.like(u'%{0}%'.format(searchterm))).all()
		mytemplate = "tvshow-list"
	if whattosearch == "episodes":
		result = db.session.query(db.TVEpisodes).filter(db.or_(db.TVEpisodes.name.like(u'%{0}%'.format(searchterm)), db.TVEpisodes.description.like(u'%{0}%'.format(searchterm)))).all()
		mytemplate = "list"
	if whattosearch == "movies":
		result = db.session.query(db.Movies).filter(db.or_(db.Movies.name.like(u'%{0}%'.format(searchterm)), db.Movies.description.like(u'%{0}%'.format(searchterm)))).all()
		mytemplate = "movie-list"
	return template(mytemplate, topmenu=u'search', title=u'Searchresults for {0}'.format(searchterm), content=result, pagination=None)

@post('/save/movie')
def update():
	synoindex = request.forms.get('synoindex')
	imdb_id = request.forms.get('imdb_id')
	result = helper.updateMovie(synoindex, imdb_id)
	return result

@route('/settings')
@requires_auth
def index():
	return template('settings', topmenu=u'settings', title=u'Settings')

@route('/settings/force')
@requires_auth
def index():
	return template('settings-force', topmenu=u'settings', title=u'Force Options')


@post('/settings/force/import')
@requires_auth
def index():
	max_entrys = request.forms.get('max_entrys')
	folder = request.forms.get('folder')
	mediatype = request.forms.get('mediatype')

	exec_date = datetime.now() + timedelta(seconds=2)
	
	if not max_entrys:
		max_entrys = 20

	if int(max_entrys) == 0:
		max_entrys = 99999
	
	answer = {'status':'error','message':'Something went wrong while forceing this action'}

	#when none is selected query all...
	if not mediatype and not folder:
		#myresponse = main.import_mediaserver(force=True, max_entrys=int(max_entrys))
		sched.add_date_job(main.import_mediaserver, exec_date, [1,max_entrys])
		answer = {'status':'success','message':'force mediaserver import of {0} elements'.format(max_entrys)}

	elif mediatype == "series":
		#myresponse = mediaimport.series(max_entrys=int(max_entrys))
		sched.add_date_job(mediaimport.series, exec_date, [max_entrys])
		answer = {'status':'success','message':'force series import of {0} elements'.format(max_entrys)}

	elif mediatype == "movies":
		#myresponse = mediaimport.movies(max_entrys=int(max_entrys))
		sched.add_date_job(mediaimport.movies, exec_date, [max_entrys])
		answer = {'status':'success','message':'force mediaserver movie of {0} elements'.format(max_entrys)}

	elif folder and folder != "":
		#myresponse = mediaimport.folder(folder, max_entrys=int(max_entrys))
		sched.add_date_job(mediaimport.folder, exec_date, [folder,max_entrys])
		answer = {'status':'success','message':'force import of {0} elements from folder \"{1}\"'.format(max_entrys, folder)}

	return answer

@route('/settings/force/update')
@requires_auth
def index():
	if config.commits_behind >= 1:
		versioncheck.update()
		main.restart()
	else:
		versioncheck.getVersion()
		versioncheck.checkGithub()
		if config.commits_behind >= 1:
			versioncheck.update()
			main.restart()

@post('/settings/force/sync')
@requires_auth
def index():
	exec_date = datetime.now() + timedelta(seconds=2)
	sched.add_date_job(main.update_movies, exec_date, [True])
	myresponse = {'status':'success','message':'forced trakt.tv sync'}
	#main.update_movies(force=True)
	return myresponse

@post('/settings/force/scrobble')
@requires_auth
def index():
	exec_date = datetime.now() + timedelta(seconds=2)
	sched.add_date_job(main.scanlogs, exec_date, [True])
	myresponse = {'status':'success','message':'forced scrobble'}
	#myresponse = main.scanlogs(force=True)
	return myresponse

@route('/logs/<loglevel>')
@requires_auth
def logs(loglevel):
	minLevel = getattr(logger.logging, loglevel)

	regex = "^(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})\s([A-Z]+)\s*(.+?)\s*(.*)$"

	data = []

	if os.path.isfile(logger.LOG_FILENAME):
		f = open(logger.LOG_FILENAME)
		data = f.readlines()

		f.close()

	finalData = []
	numLines = 1
	lastLine = False
	maxLines = 500
	numToShow = min(maxLines, len(data))

	reverseNames = {u'ERROR': logger.logging.ERROR,
                u'WARNING': logger.logging.WARNING,
                u'INFO': logger.logging.INFO,
                u'DEBUG': logger.logging.DEBUG}


	for x in reversed(data):
		x = x.decode('utf-8')
		match = re.match(regex, x)


		if match:
			level = match.group(3)
			if level not in reverseNames:
				lastLine = False
				continue

			#print "level ", reverseNames[level]

			if reverseNames[level] >= minLevel:
				lastLine = True
				finalData.append(x)
			else:
				lastLine = False
				continue

		elif lastLine:
			finalData.append("AA"+x)

		numLines += 1

		if numLines >= numToShow:
			break

	result = "".join(finalData)

	

	return template('logs', result=result, topmenu=u"logs", title=u"Logs - {0}".format(loglevel))

#static routes...
# @route('/cover/<filepath:path>')
# def server_static(filepath):
# 	return static_file(filepath, root="/Users/workstation/Documents/bitbucket/synodlnatrakt/views/")

@post('/save/config')
@requires_auth
def saveConfig():

	#set checkbox values to false by default...
	config.try_guessing = False
	config.delete_logs = False
	config.absolute_ep_anime = False
	config.hide_watched = False
	config.logtoconsole = False
	config.debugmode = False
	config.watched_flags = False


	#print config.moviedir

	for a in request.forms:
		#print "Setting config.{0} to {1}".format(a, request.forms.get(a))
		if request.forms.get(a) == "on":
			setattr(config, a, True)
		elif request.forms.get(a) == "0":
			setattr(config, a, False)
		elif request.forms.get(a) == "" or request.forms.get(a) == " ":
			setattr(config, a, getattr(config,a))
		else:
			setattr(config, a, request.forms.get(a))

		if a == "moviedir" and request.forms.get("moviedir") != "":
			movielist = request.forms.get("moviedir").split(',')
			newMovielist = []
			for x in movielist:
				newMovielist.append(x.strip())
			config.moviedir = newMovielist
			print config.moviedir

		if a == "seriesdir" and request.forms.get("seriesdir") != "":
			serieslist = request.forms.get("seriesdir").split(',')
			newserieslist = []
			for x in serieslist:
				newserieslist.append(x.strip())
			config.seriesdir = newserieslist
			print config.seriesdir
		#print type(request.forms.get(a))
	try:
		config.save_config()
		ui.notifications.success("Yeah","settings saved successfully")
	except:
		ui.notifications.error("Whooopsy...","settings not saved")


@post('/scrobble')
@requires_auth
def scrobble():
	mediatype = request.forms.get('type')
	synoindex = request.forms.get('synoindex')
	if mediatype == "series":
		m = Episode(synoindex, None)
	elif mediatype == "movie":
		m = Movie(synoindex, None)
	if m:
		answer = trakt.seen(m, returnStatus=True)
		m.scrobbled = 1
		m.progress = 100
		m.to_database()
		return answer
	else:
		return False

@post('/delete')
@requires_auth
def delete():
	mediatype = request.forms.get('type')
	synoindex = request.forms.get('synoindex')
	if mediatype == "series":
		result = db.session.query(db.TVEpisodes).filter(db.TVEpisodes.synoindex == synoindex).first()
	if mediatype == "movie":
		result = db.session.query(db.Movies).filter(db.Movies.synoindex == synoindex).first()
	db.session.delete(result)
	db.session.commit()
	return {"status":"success"}

@post('/stream')
@requires_auth
def streaming():
	mediatype = request.forms.get('type')
	synoindex = request.forms.get('synoindex')
	if mediatype == "series":
		result = db.session.query(db.TVEpisodes).filter(db.TVEpisodes.synoindex == synoindex).first()
		return template('stream', path=result.path, cover=result.show_id)
	if mediatype == "movie":
		result = db.session.query(db.Movies).filter(db.Movies.synoindex == synoindex).first()
		return template('stream', path=result.path, cover=result.imdb_id)
	

@post('/rate')
@requires_auth
def rating():
	mediatype = request.forms.get('type')
	synoindex = request.forms.get('synoindex')
	rating = request.forms.get('score')

	if mediatype == "series":
		content = db.session.query(db.Series).filter(db.Series.synoindex == synoindex).first()
	elif mediatype == "movie":
		content = db.session.query(db.Movies).filter(db.Movies.synoindex == synoindex).first()

	content.rating = rating
	db.session.merge(content)
	db.session.commit()
	answer = trakt.rate(content, rating, returnStatus=True)
	return answer

@route('/watch/<filepath:path>')
def server_static(filepath):
	print filepath
	if not os.path.exists(filepath):
		filepath = filepath.replace("/volume1/","/Volumes/")
		print filepath
	if os.path.splitext(filepath)[1] == ".m4v":
		return static_file(filepath, root="/", mimetype="video/mp4")
	else:
		return static_file(filepath, root="/")

@route('/static/<filepath:path>')
@requires_auth
def server_static(filepath):
    return static_file(filepath, root=config.templatedir)

@route('/cache/<filepath:path>')
@requires_auth
def server_static(filepath):
    return static_file(filepath, root=config.cachedir)

@route('/ui')
def index():
	myip = request["REMOTE_ADDR"]
	messages = {}
	cur_notification_num = 1
	for cur_notification in ui.notifications.get_notifications(myip):
		messages['notification-'+str(cur_notification_num)] = {'title': cur_notification.title, 'message': cur_notification.message, 'type': cur_notification.type}
		cur_notification_num += 1

	return json.dumps(messages)

@route('/stats')
def inder():
	return template("stats", topmenu=u"settings", title=u"Stats")


@post('/ui/addNotification')
def add_notification():
	notetype = request.forms.get('type')
	notetitle = request.forms.get('title')
	notemessage = request.forms.get('message')

	if notetype == "success":
		ui.notifications.success(notetitle, notemessage)
	elif notetype == "error":
		ui.notifications.error(notetitle, notemessage)
	else:
		ui.notifications.message(notetitle, notemessage)

#run(host='0.0.0.0', port=1337, reloader=True)