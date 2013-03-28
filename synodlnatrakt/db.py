from sqlalchemy import create_engine, MetaData, Column, Integer, String, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from synodlnatrakt import config, images

from os import path

from lib.tvdb_api import tvdb_api
from lib.themoviedb import tmdb


dbpath = path.join(config.datadir, "SynoDLNAtrakt.db")
engine = create_engine('sqlite:///{0}'.format(dbpath), echo=False)

Base = declarative_base()

class Version(Base):
    __tablename__ = 'alembic_version'

    version_num = Column(String, default=config.cur_version, primary_key=True)

    def __init__(self, version_num):
        self.version_num = version_num

    def __repr__(self):
        return u"<Version({})".format(self.version_num)

class TVShows(Base):
    __tablename__ = 'tv_shows'

    tvdb_id = Column(Integer, unique=True, primary_key=True)
    name = Column(String)
    location = Column(String)
    is_anime = Column(Integer)

    def __init__(self, tvdb_id, name, location, is_anime):
        self.tvdb_id = tvdb_id
        self.name = name
        self.location = location
        self.is_anime = is_anime

    def __repr__(self):
        return u"<TVShows('{0}{1}{2})>".format(self.location, self.tvdb_id, self.name)


class TVEpisodes(Base):
    __tablename__ = 'tv_episodes'

    show_id = Column(Integer)
    tvdb_id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    season = Column(Integer)
    episode = Column(Integer)
    description = Column(String)
    path = Column(String)
    duration = Column(Integer)
    progress = Column(Integer, default=0)
    scrobbled = Column(Integer, default=0)
    rating = Column(Integer)
    lastseen = Column(Integer)
    added = Column(Integer)
    synoindex = Column(Integer)
    is_anime = Column(Integer)
    abs_ep = Column(Integer)

    acodec = Column(String)
    vcodec = Column(String)
    vwidth = Column(Integer)

    def __init__(
        self, show_id, tvdb_id, name, season, episode, description, path,
        duration, progress, scrobbled, rating, lastseen, added, synoindex,
        is_anime, abs_ep, acodec, vcodec, vwidth
    ):
        self.show_id = show_id
        self.tvdb_id = tvdb_id
        self.name = name
        self.season = season
        self.episode = episode
        self.description = description
        self.path = path
        self.duration = duration
        self.progress = progress
        self.scrobbled = scrobbled
        self.rating = rating
        self.lastseen = lastseen
        self.added = added
        self.synoindex = synoindex
        self.abs_ep = abs_ep
        self.is_anime = is_anime
        self.acodec = acodec
        self.vcodec = vcodec
        self.vwidth = vwidth

    def __repr__(self):
        return u"<TVEpisodes('{0} {1} {2} {3} {4})>".format(self.progress, self.show_id, self.name, self.season, self.episode)


class Movies(Base):
    __tablename__ = 'movies'

    imdb_id = Column(String)
    tmdb_id = Column(Integer)
    name = Column(String)
    year = Column(Integer)
    description = Column(String)
    path = Column(String)
    duration = Column(Integer)
    progress = Column(Integer)
    scrobbled = Column(Integer)
    rating = Column(Integer)
    lastseen = Column(Integer)
    added = Column(Integer)
    synoindex = Column(Integer, unique=True, primary_key=True)

    acodec = Column(String)
    vcodec = Column(String)
    vwidth = Column(Integer)

    def __init__(
        self, imdb_id, tmdb_id, name, year, description, path,
        duration, progress, scrobbled, rating, lastseen, added,
        synoindex, acodec, vwidth, vcodec
    ):
        self.imdb_id = imdb_id
        self.tmdb_id = tmdb_id
        self.name = name
        self.year = year
        self.description = description
        self.path = path
        self.duration = duration
        self.progress = progress
        self.scrobbled = scrobbled
        self.rating = rating
        self.lastseen = lastseen
        self.added = added
        self.synoindex = synoindex
        self.acodec = acodec
        self.vcodec = vcodec
        self.vwidth = vwidth

    def __repr__(self):
        return u"<Movies('{0}{1}{2}{3}{4})>".format(self.path, self.imdb_id, self.name, self.year)


Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = scoped_session(Session)
# session = Session()
#
if session.query(Version).first() is None:
    session.merge(Version(version_num=config.cur_version))
    session.commit()
