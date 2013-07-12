# Author: cytec <iamcytec@googlemail.com>
# URL: http://github.com/cytec/SynoDLNAtrakt/
#
# This file is part of SynoDLNAtrakt.

import re
import os
import shutil
import subprocess
import datetime
import codecs
from urllib import urlretrieve
from xml.dom.minidom import parse, parseString
from lib.apachelog import apachelog as apachelog
from lib.themoviedb import tmdb
from lib.tvdb_api import tvdb_api
from synodlnatrakt import config, db, pgsql, images, ui
from synodlnatrakt.logger import logger
from synodlnatrakt.name_parser import parser
import lib.enzyme as enzyme


def updateMediaflags():
    movies = db.session.query(db.Movies).filter(db.Movies.acodec == None).all()
    for m in movies:
        # path = m.path.replace("/volume1/", "/Volumes/")

        m.mediaflags()

    episode = db.session.query(db.TVEpisodes).filter(db.TVEpisodes.acodec == None).all()
    for m in episode:
        # path = m.path.replace("/volume1/", "/Volumes/")

        m.mediaflags()

    # db.session.commit()
    ui.notifications.success("Madiaflags", 'successfully generated')


def updateMovie(synoindex, imdb_id):
    movie = tmdb.getMovieInfo(imdb_id, lang=config.language)
    result = db.session.query(db.Movies).filter(db.Movies.synoindex == synoindex).first()
    if result:
        oldname = result.name
        oldyear = result.year
        result.name = movie["name"]
        result.description = movie["overview"]
        result.imdb_id = movie["imdb_id"]
        result.tmdb_id = movie["id"]
        result.year = movie["released"].split("-")[0]
        result.rating = 0
        result.lastseen = ""
        result.progress = 0
        result.scrobbled = 0
    db.session.merge(result)
    db.session.commit()
    images.get_images(imdb_id, "movie")
    ui.notifications.success(movie["name"], 'updated {0} ({1}) with {2} ({3})'.format(
        oldname, oldyear, movie["name"], movie["released"].split("-")[0]))
    # answer = {u"status":u"success", u"message": u"updated {0} with {1}".format(oldname, movie["name"]), u"title": movie["name"]}
    # return answer


def get_media_type(theid):
    mediatype = None
    theid = int(theid)
    dbresult = pgsql.session.query(pgsql.Video).filter(pgsql.Video.id == theid).first()
    if dbresult:
        logger.debug(u"synoindex result for {0} -> {1}".format(dbresult.id, dbresult.path))
        path = dbresult.path
        duration = dbresult.duration
        for curdir in config.seriesdir:
            # print curdir, self.path
            if curdir in dbresult.path:
                mediatype = "series"
                directory = curdir
        for curdir in config.moviedir:
            if curdir in dbresult.path:
                mediatype = "movie"
                directory = curdir
        return mediatype
    else:
        logger.error(u"No entry found for ID {0}".format(theid))
        return None


def startupCheck():
    try:
        debugfile = open('/var/packages/MediaServer/etc/dmsinfo.conf')
        filelines = debugfile.readlines()
        debugfile.close()
        value = filelines[-1].replace("loglevel_mediaservice=\"", "").replace("\"\n", "")
        if int(value) < 3:
            logger.error(u"MediaServer not running in Debugmode!")
            sys.exit(u"Please enable Debugmode for MediaServer first!")
        else:
            logger.debug(u"MediaServer running in Debugmode")
    except:
        logger.error(u"Can't check if your MeidaServer runs in Debugmode or not...")

    if not os.path.exists(config.accesslog):
        logger.info(u"{0} doesn't exist please check your settings and make sure you enabled MediaServers Debug mode".format(
            config.accesslog))
        sys.exit(1)

    logger.info(u"Starting SynoDLNAtrakt...")


def createWatchedFile(mediaelement):
    watched = u"{0}.watched".format(mediaelement.path)
    if not os.path.isfile(watched):
        f = open(watched, 'w')
        f.close()
        logger.debug(u"Created watched file: {0}".format(watched))


def parseLog():
    idtimes = {}
    BLACKLIST = []
    p = apachelog.parser(apachelog.formats['lighttpd'])
    time_format = '[%d/%b/%Y:%H:%M:%S]'

    if os.path.exists(config.accesslog):
        logger.info(u"Parsing MediaServer log file from: {0}".format(config.accesslog))
        for line in open(config.accesslog):
            try:
                data = p.parse(line)
                x = re.match(config.logregex, data["%r"])
                theid = x.group("theid")
                extension = x.group("ext")

                if (config.use_whitelist and data["%{User-Agent}i"] not in config.whitelist):
                    if not (data["%{User-Agent}i"] in BLACKLIST):
                        logger.error(u"User Agent not in Whitelist: {0}".format(data["%{User-Agent}i"]))
                        BLACKLIST.append(data["%{User-Agent}i"])

                    continue

                if extension not in config.medialist:
                    continue

                # print data["%t"].re.replace("+[0-9]*","")
                data["%t"] = re.sub(" \+[0-9]*", "", data["%t"])
                    # calculate the actual date from the log (for timedelta calculations)
                thedate = datetime.datetime.strptime(data["%t"], time_format)
                try:
                    if theid not in idtimes:
                        thedate = [thedate]
                        idtimes[theid] = thedate
                    else:
                        datelist = idtimes[theid]
                        checkdate = datelist[0]
                        # first access plus 6 hours timeframe...
                        expirationdate = checkdate + datetime.timedelta(hours=6)
                        # if its between the 6hours timeframe, add it else skipp it...
                        # print "First view: {0}, Falid till: {1}".format(checkdate, expirationdate)
                        if expirationdate > thedate:
                            datelist.append(thedate)
                            idtimes[theid] = datelist
                        else:
                            # when its outside the timframe, try to overwrite it with the newer date...
                            logger.debug(u"{0} is more than 6hours after the first access to: {1}".format(thedate, theid))
                            logger.debug(u"Overwriting {0} with new startdate: {1}".format(theid, thedate))
                            thedate = [thedate]
                            idtimes[theid] = thedate
                except:
                    logger.error(u"Sorry something went wrong here, can't create dictionary")

            except:
                logger.error(u"Unable to parse line: {0}".format(line))
        logger.info(u"Parsing: {0} gave {1} entry(s)".format(config.accesslog, len(idtimes)))

        if config.delete_logs and len(idtimes) > 0:
            if not os.path.exists(config.datadir + "/accesslog-backups/"):
                os.makedirs(config.datadir + "/accesslog-backups/")
            newlogpath = config.datadir + "/accesslog-backups/{0}-access.log".format(datetime.datetime.now()
                                                                                     .strftime('%y%m%d-%H%M%S'))

            shutil.copy(config.accesslog, newlogpath)

            # truncate accesslog (just clean it)
            open(config.accesslog, 'w').close()
            logger.info(u"{0} moved to backup directory: {1}".format(config.accesslog, newlogpath))
        return idtimes
    else:
        logger.error(u"PLEASE ENABLE DEBUG MODE FOR YOUR DLNA SERVER")
        return None


def cache_cover(theid, mediatype):
    if mediatype == "series":
        t = tvdb_api.Tvdb(language=config.language)
        theid = theid.replace("fanart/", "")
        showinfo = t[int(theid)]
        cachedir = os.path.join(config.templatedir, "cache/")
        if not os.path.exists(os.path.join(cachedir, "cover/{0}.jpg".format(theid))):
            urlretrieve(showinfo['poster'], os.path.join(cachedir, "cover/{0}.jpg".format(theid)))
        if not os.path.exists(os.path.join(cachedir, "/fanart/{0}.jpg".format(theid))):
            urlretrieve(showinfo['fanart'], os.path.join(cachedir, "fanart/{0}.jpg".format(theid)))


def tmdbsearch(searchstring):
    logger.debug(u"searching tmdb for: {0}".format(searchstring))
    if searchstring[:2] == "tt":
        movieinfo = tmdb.getMovieInfo('{0}'.format(searchstring), lang=config.language)
    else:
        results = tmdb.search(searchstring, lang=config.language)
        if results:
            firstresult = results[0]
            movieinfo = firstresult.info(lang=config.language)
        else:
            # search again for movie without the year
            searchstring = re.sub(" \([0-9]{4}\)", "", searchstring)
            results = tmdb.search(searchstring, lang=config.language)
            if results:
                firstresult = results[0]
                movieinfo = firstresult.info(lang=config.language)
            else:
                logger.error(u"Can't find any matches for {0}".format(searchstring))
                return None, None, None, None
    imdb_id = movieinfo["imdb_id"]
    tmdb_id = movieinfo["id"]
    title = movieinfo["name"]
    try:
        year = movieinfo["released"].split("-")[0]
    except:
        year = 0000
    logger.info(u"Found result for {0} -> Fullname: {1}, year {3}, imdb_id: {2}".format(searchstring, title, imdb_id, year))
    return title, imdb_id, tmdb_id, year


def parse_name(filename):
    """
    Parse filename. Tries to get title of the movie/tv-series etc.
    @param filename: Path of the movie
    @return: Title
"""
    filename = filename.lower()
    filename = os.path.split(filename)[1]
    filename = os.path.splitext(filename)[0]

    for item in config.TITLE_STRIP_SEARCH:
        filename = filename.replace(item, ' ')

    for item in config.TITLE_SPLIT_KEYWORDS:
        filename = filename.split('%s' % item)[0]
    filename = filename.strip()

    return filename


def checkNFO(filepath, nfotype):
    hasnfo = False
    # check the nfo for the needed id stuff...
    # check if there is an nfo file... if not, fuck it and try to get infos from tvdb...
    if nfotype == "series":
        directory = os.path.dirname(filepath)
        directory = re.sub(r'Staffel.\d{1,2}|Season.\d{1,2}|', '', directory)
        nfofile = os.path.join(directory, "tvshow.nfo")
        try:
            dom = parse(nfofile)
            seriesidTag = dom.getElementsByTagName('id')[0].toxml()
            seriesid = seriesidTag.replace('<id>', '').replace('</id>', '')
            try:
                nameTag = dom.getElementsByTagName('showtitle')[0].toxml()
                name = nameTag.replace('<showtitle>', '').replace('</showtitle>', '')
            except:
                nameTag = dom.getElementsByTagName('title')[0].toxml()
                name = nameTag.replace('<title>', '').replace('</title>', '')
            logger.debug(u"SeriesID for {0} is: {1}".format(name, seriesid))
            return seriesid, name
        except:
            # TODO: fix some unicode errors here...
            logger.error(u"cant find/open file: {0}".format(nfofile))
            if config.try_guessing:
                logger.info(u"Trying to guess infos from Filename...")
                seriesname = os.path.basename(filepath)
                # p = re.match(config.seriesregex, seriesname)
                # name = p.group("name").replace(".", " ").strip()
                # if name == "":
                # 	name = os.path.split(os.path.dirname(nfofile))[1]
                # season = p.group("season")
                # episode = p.group("episode")
                np = parser.NameParser()
                parsed = np.parse(seriesname)
                name = parsed.series_name
                season = parsed.season_number
                episode = parsed.episode_numbers[0]
                logger.debug(u"Type: {3}, Name: {0}, Season: {1}, Episode: {2}".format(name, season, episode, nfotype))
                # strip out and, &
                andstrings = [" and ", " & "]
                for string in andstrings:
                    if string in name:
                        name = name.replace(string, " ")
                try:
                    t = tvdb_api.Tvdb(language=config.language)
                    showinfo = t[name]
                    tvdb_id = showinfo["id"]
                    realname = showinfo["seriesname"]
                    year = showinfo["firstaired"]
                    # logger.debug("tvdb gave the following keys: {0}".format(showinfo.data.keys()))
                    logger.info(u"Found result for {0} -> Fullname: {1}, tvdb_id: {2}, Year: {3}".format(
                        name, realname, tvdb_id, year))
                    return tvdb_id, realname
                except tvdb_api.tvdb_shownotfound:
                    logger.error(u"Unable to find {0} on thetvdb.com".format(name))
                    return 0, None
            else:
                logger.error(u"Please enable try_guessing in settings or create an tvshow.nfo for: {0}".format(directory))
            return 0, None

    if nfotype == "episode":
        filename, extension = os.path.splitext(filepath)
        nfofile = filename + ".nfo"
        try:
            dom = parse(nfofile)
            episodeTag = dom.getElementsByTagName('episode')[0].toxml()
            episode = episodeTag.replace('<episode>', '').replace('</episode>', '')
            seasonTag = dom.getElementsByTagName('season')[0].toxml()
            season = seasonTag.replace('<season>', '').replace('</season>', '')
            episodeTag = dom.getElementsByTagName('episode')[0].toxml()
            episode = episodeTag.replace('<episode>', '').replace('</episode>', '')
            logger.info(u'TVSHOW info -> Season: {0}, Episode: {1}'.format(season, episode))
            return season, episode
        except:
            logger.error(u"Cant find/open/parse file: {0}".format(nfofile))
            if config.try_guessing:
                logger.info(u"try to guess infos from Filename...")
                seriesname = os.path.basename(filepath)
                # p = re.match(config.seriesregex, seriesname)
                # name = p.group("name").replace(".", " ").strip()
                # season = p.group("season")
                # episode = p.group("episode")
                np = parser.NameParser()
                parsed = np.parse(seriesname)
                name = parsed.series_name
                season = parsed.season_number
                episode = parsed.episode_numbers[0]
                logger.debug(u"Type: {3}, Series: {0}, Season: {1}, Episode: {2}".format(seriesname, season, episode, nfotype))
                return season, episode
            else:
                logger.error(u"Please enable try_guessing in settings or create an .nfo for: {0}".format(directory))
            return 0, 0

    if nfotype == "movie":
        # order of use: .nfo, .imdb, try_guessing
        filename, extension = os.path.splitext(filepath)
        nfofile = filename + ".nfo"
        if "cd2" in filename.lower():
            return None, None, None
        try:
            dom = parse(nfofile)
            imdb_idtag = dom.getElementsByTagName('id')[0].toxml()
            imdb_id = imdb_idtag.replace('<id>', '').replace('</id>', '')
            nametag = dom.getElementsByTagName('title')[0].toxml()
            name = nametag.replace('<title>', '').replace('</title>', '')
            yeartag = dom.getElementsByTagName('year')[0].toxml()
            year = yeartag.replace('<year>', '').replace('</year>', '')
            if not imdb_id.startswith("tt") and int(imdb_id):
                imdb_id = "tt{0}".format(imdb_id)
            logger.info(u'Movie info -> Name: {0}, Year: {1}, imdb_id: {2}'.format(name, year, imdb_id))
            return name, imdb_id, year
        except:
            logger.error(u"Cant find/open file: {0}".format(nfofile))

            # only use try_guessing if there was no imdb file...
            if config.try_guessing:
                logger.info(u"try to guess infos from Filename: {0}".format(filepath))

                searchstring = []

                # try folder and movie for names
                for element in os.path.split(filepath):
                    moviename = parse_name(element)
                    searchstring.append(u"{0}".format(moviename))

                logger.debug(u"Parsed {0} to {1}".format(filepath, searchstring))
                # first search file...
                #searchstring.reverse()
                for entry in searchstring:
                    title, imdb_id, tmdb_id, year = tmdbsearch(entry)
                    if imdb_id:
                        myreturn = title, imdb_id, year
                        break
                    else:
                        myreturn = None, None, None

                # if myreturn == (None, None, None):
                #     f = codecs.open(os.path.join(config.datadir, "error.txt"), "a", encoding="utf-8")
                #     f.write(u"{0}\n".format(filepath))
                #     f.close()

                return myreturn

                # logger.debug(u"Type: {3}, Name: {0}, Year: {1}, Searchstring: {2}".format(name, year, searchstring, nfotype))
            else:
                logger.error(u"Please enable try_guessing in settings or create an .nfo for: {0}".format(filepath))
                return 0
