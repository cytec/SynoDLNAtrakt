from synodlnatrakt import helper, config
from synodlnatrakt.mediaelement import Episode, Movie
from synodlnatrakt import pgsql, trakt, db, pgsql, trakt, ui

import datetime

from synodlnatrakt.logger import logger


def series(max_entrys=20):
    counter = 0
    for folder in config.seriesdir:
        print folder
        result = (
            pgsql.session.query(pgsql.Video)
            .filter(pgsql.Video.path.like('{0}%'.format(folder)))
            .order_by(pgsql.Video.date.desc())
            .limit(max_entrys)
        )
        for episode in result:
            m = Episode(episode.id, None, database=True)
            if m.path:
                logger.info(u"loaded Mediaelement from db: {0}".format(episode.id))
            else:
                m.generate()
                m.to_database()
                counter = + 1
    response = {
        u'status': u'success',
        u'message': u'added {0} episodes to synodlnatrakt'.format(max_entrys)
    }

    ui.notifications.success("Yeah", "added {0} episodes to the database".format(counter))
    return response


def search(searchstring, max_entrys=20):
    counter = 0
    logger.info(u"searching for files which contain: '{0}'".format(searchstring))
    result = (
        pgsql.session.query(pgsql.Video)
        .filter(pgsql.Video.path.like('%{0}%'.format(searchstring)))
        .order_by(pgsql.Video.date.desc())
        .limit(max_entrys)
    )
    for entry in result:
        mediatype = helper.get_media_type(entry.id)
        if mediatype == "series":
            m = Episode(entry.id, None, database=True)
        elif mediatype == "movie":
            m = Movie(entry.id, None, database=True)

        if m.path:
            logger.info(u"loaded Mediaelement from db: {0}".format(episode.id))
        else:
            m.generate()
            m.to_database()
            counter = + 1

    response = {
        u'status': u'success',
        u'message': u'added {0} episodes to synodlnatrakt'.format(max_entrys)
    }

    ui.notifications.success("Yeah", "added {0} episodes to the database".format(counter))
    return response


def movies(max_entrys=20):
    counter = 0
    for folder in config.moviedir:
        print folder
        result = (
            pgsql.session.query(pgsql.Video)
            .filter(pgsql.Video.path.like('{0}%'.format(folder)))
            .order_by(pgsql.Video.date.desc())
            .limit(max_entrys)
        )
        for movie in result:
            m = Movie(movie.id, None, database=True)
            if m.path:
                logger.info(u"loaded Mediaelement from db: {0}".format(movie.id))
            else:
                m.generate()
                m.to_database()
                counter = + 1

    response = {
        u'status': u'success',
        u'message': u'added {0} movies to synodlnatrakt'.format(max_entrys)
    }
    ui.notifications.success("Yeah", "added {0} movies to the database".format(counter))
    return response
    # pass


def folder(folder, max_entrys=20):
    counter = 0
    result = (
        pgsql.session.query(pgsql.Video)
        .filter(pgsql.Video.path.like('{0}%'.format(folder)))
        .order_by(pgsql.Video.date.desc())
        .limit(max_entrys)
    )
    for entry in result:
        mediatype = helper.get_media_type(entry.id)
        if mediatype == "series":
            m = Episode(entry.id, None, database=True)
        elif mediatype == "movie":
            m = Movie(entry.id, None, database=True)
        else:
            continue

        if m:
            if m.path:
                logger.info(u"loaded Mediaelement from db: {0}".format(entry.id))
            else:
                m.generate()
                m.to_database()
                counter = + 1

    response = {
        u'status': u'success',
        u'message': u'added {0} entrys from folder {1} to synodlnatrakt'.format(max_entrys, folder)
    }
    ui.notifications.success("Yeah", "added {0} entrys to the database".format(counter))
    return response
