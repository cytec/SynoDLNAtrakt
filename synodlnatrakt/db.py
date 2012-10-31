from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from synodlnatrakt import config
from os import path


dbpath = path.join(config.BASEPATH, "SynoDLNAtrakt.db")
engine = create_engine('sqlite:///{0}'.format(dbpath), echo=False)

Base = declarative_base()

class Scrobble(Base):
	__tablename__ = 'scrobble'

	id = Column(Integer, primary_key=True)
	thepath = Column(String)
	name = Column(String)
	process = Column(Integer)
	lastviewed = Column(Integer)
	imdb_id = Column(String)
	tvdb_id = Column(Integer)
	viewed = Column(Integer)
	type = Column(String)
	directory = Column(String)
	year = Column(Integer)
	season = Column(Integer)
	episode = Column(Integer)
	scrobbled = Column(Integer)

	def __init__(self, thepath, name, process, lastviewed, imdb_id, tvdb_id, viewed, type, directory, year, season, episode, scrobled):
		self.thepath = thepath
		self.name = name
		self.process = process
		self.lastviewed = lastviewed
		self.imdb_id = imdb_id
		self.tvdb_id = tvdb_id
		self.viewed = viewed
		self.type = type
		self.directory = directory
		slef.year = year
		self.season = season
		self.episode = episode
		self.scrobled = scrobled

	def __repr__(self):
		return u"<Scrobble('{0}{1}{2}{3})>".format(self.name, self.tvdb_id, self.season, self.episode)

Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()