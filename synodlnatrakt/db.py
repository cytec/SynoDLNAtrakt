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

    def __init__(self, show_id, tvdb_id, name, season, episode, description, path, duration, progress, scrobbled, rating, lastseen, added, synoindex, is_anime, abs_ep):
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

    def __init__(self, imdb_id, tmdb_id, name, year, description, path, duration, progress, scrobbled, rating, lastseen, added, synoindex):
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

    def __repr__(self):
        return u"<Movies('{0}{1}{2}{3}{4})>".format(self.path, self.imdb_id, self.name, self.year)


Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = scoped_session(Session)
# session = Session()
