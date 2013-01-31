import os
import re

from synodlnatrakt import pgsql, config, db, helper, images, trakt
from synodlnatrakt.logger import logger

from lib.tvdb_api import tvdb_api
from lib.themoviedb import tmdb


class Movie(object):
	'''Movie object'''

	def __init__(self, synoindex, loglist, database=True):
		self.imdb_id = 0
		self.name = ""
		self.year = 0
		self.description = ""
		self.path = ""
		self.duration = ""
		self.progress = 0
		self.scrobbled = 0
		self.rating = 0
		self.lastseen = ""
		self.added = ""
		self.synoindex = int(synoindex)
		self.mediatype = "movie"
		self.tmdb_id = 0
		self.type = "movie"
		self._log = loglist

		if database:
			self.from_database()
		else:
			self.generate()

	def _calc_runtime(self):
		#enddate - startdate = duration
		#self.progress = 0
		try:
			duration = self._log[-1] - self._log[1]
		except:
			duration = self._log[1] - self._log[1]
		h, m, s = str(duration).split(":")
		viewed = int(h)*60
		viewed = (viewed + int(m))*60
		viewed = (viewed + int(s))
		self.lastseen = self._log[-1]
		if self.progress and config.delete_logs:
			self.progress = int(self.progress) + (int(viewed) / (int(self.duration) / 100))
		else:
			self.progress = int(viewed) / (int(self.duration) / 100)
		

		if self.progress > 100:
			self.progress = 100

	def from_database(self):
		result = (
			db.session.query(db.Movies)
				.filter(db.Movies.synoindex == self.synoindex).first()
			)

		if result:
			self.imdb_id = result.imdb_id
			self.name = result.name
			self.year = result.year
			self.description = result.description
			self.path = result.path
			self.duration = result.duration
			self.progress = result.progress
			self.scrobbled = result.scrobbled
			self.rating = result.rating
			self.lastseen = result.lastseen
			self.added = result.added
			self.synoindex = result.synoindex
			self.tmdb_id = result.tmdb_id

		return self

	def to_database(self):
		if self.imdb_id:
			insert = db.Movies(
				imdb_id = self.imdb_id,
				tmdb_id = self.tmdb_id,
				name = self.name,
				year = self.year,
				description = self.description,
				path = self.path,
				duration = self.duration,
				progress = self.progress,
				scrobbled = self.scrobbled,
				rating = self.rating,
				lastseen = self.lastseen,
				added = self.added,
				synoindex = self.synoindex
				)
			#dir(insert)
			db.session.merge(insert)
			db.session.commit()

	def generate(self):
		#stuff we get from synoindex db
		dbresult = pgsql.session.query(pgsql.Video).filter(pgsql.Video.id == self.synoindex).first()
		self.path = dbresult.path
		self.duration = dbresult.duration
		self.added = dbresult.date

		for curdir in config.moviedir:
			if curdir in self.path:
				self.mediatype = "movie"
				self.directory = curdir
		
		if self._log:
			self._calc_runtime()

		self.name, self.imdb_id, self.year = helper.checkNFO(self.path, "movie")

		if self.imdb_id:
	
			movie = tmdb.getMovieInfo(self.imdb_id, lang=config.language)
			self.description = movie["overview"]
			self.tmdb_id = movie["id"]
			images.get_images(self.imdb_id, "movie")

			if config.add_to_list:
				trakt.add_to_list(self, listname=config.list_name)

	def postprocess(self):
		if config.delete_from_disk and self.progress == 100:
			pass



class Episode(object):

	def __init__(self, synoindex, loglist, database=True):
		self.mediatype = "series"
		self.show_id = 0
		self.tvdb_id = 0
		self.name = None
		self.season = 0
		self.episode = 0
		self.description = None
		self.path = None
		self.duration = 0
		self.progress = 0
		self.scrobbled = 0
		self.rating = 0
		self.lastseen = 0
		self.added = 0
		self.synoindex = int(synoindex)
		self.location = None
		self.showname = None
		self._log = loglist
		self.is_anime = 0
		self.abs_ep = 0
		self.type = "series"
		if database:
			self = self.from_database()
		else:
			self.generate()


	def _calc_runtime(self):
		#enddate - startdate = duration
		#self.progress = 0
		try:
			duration = self._log[-1] - self._log[1]
		except:
			duration = self._log[1] - self._log[1]
		h, m, s = str(duration).split(":")
		viewed = int(h)*60
		viewed = (viewed + int(m))*60
		viewed = (viewed + int(s))
		self.lastseen = self._log[-1]
		if self.progress and config.delete_logs:
			self.progress = int(self.progress) + (int(viewed) / (int(self.duration) / 100))
		else:
			self.progress = int(viewed) / (int(self.duration) / 100)
		

		if self.progress > 100:
			self.progress = 100

	def from_database(self):
		result = (
			db.session.query(db.TVEpisodes)
				.filter(db.TVEpisodes.synoindex == self.synoindex).first()
			)
		if result:
			self.show_id = result.show_id
			self.tvdb_id = result.tvdb_id
			self.name = result.name
			self.season = result.season
			self.episode = result.episode
			self.description = result.description
			self.path = result.path
			self.duration = result.duration
			self.progress = result.progress
			self.scrobbled = result.scrobbled
			self.rating = result.rating
			self.lastseen = result.lastseen
			self.added = result.added
			self.synoindex = result.synoindex
			self.is_anime = result.is_anime
			self.abs_ep = result.abs_ep
			#self._calc_runtime()
			tmpname = db.session.query(db.TVShows.name).filter(db.TVShows.tvdb_id == self.show_id).first()
			self.showname = tmpname.name
		return self

	def to_database(self):
		if self.tvdb_id:
			insert = db.TVEpisodes(
				show_id = self.show_id,
				tvdb_id = self.tvdb_id,
				name = self.name,
				season = self.season,
				episode = self.episode,
				description = self.description,
				path = self.path,
				duration = self.duration,
				progress = self.progress,
				scrobbled = self.scrobbled,
				rating = self.rating,
				lastseen = self.lastseen,
				added = self.added,
				synoindex = self.synoindex,
				abs_ep = self.abs_ep,
				is_anime = self.is_anime
				)
	
			result = db.session.query(db.TVShows).filter(db.TVShows.tvdb_id == self.show_id).first()
			if not result:
				insert2 = db.TVShows(
						tvdb_id = self.show_id,
						location = self.location,
						name = self.showname,
						is_anime = self.is_anime
					)
				db.session.merge(insert2)
	
			db.session.merge(insert)
			
			db.session.commit()

	def generate(self):
		dbresult = pgsql.session.query(pgsql.Video).filter(pgsql.Video.id == self.synoindex).first()
		self.path = dbresult.path
		self.duration = dbresult.duration
		self.added = dbresult.date
		self.show_id, self.showname = helper.checkNFO(self.path, "series")
		self.season, self.episode = helper.checkNFO(self.path, "episode")

		for curdir in config.seriesdir:
			#print curdir, self.path
			if curdir in self.path:
				self.mediatype = "series"
				self.location = curdir

		if self.show_id:
			t = tvdb_api.Tvdb(language=config.language)
			#series = t[self.show_id]
			series = t[int(self.show_id)]
			self.tvdb_id = series[int(self.season)][int(self.episode)]["id"]
			self.name = series[int(self.season)][int(self.episode)]["episodename"]
			self.description = series[int(self.season)][int(self.episode)]["overview"]
	
			if "Animation" in series["genre"]:
				self.is_anime = 1
				self.abs_ep = series[int(self.season)][int(self.episode)]["absolute_number"]
	
			if self._log:
				self._calc_runtime()
	
			if self.show_id:
				images.get_images(self.show_id, "series")

				if config.add_to_list:
					trakt.add_to_list(self, listname=config.list_name)
