import re, os
from lib.themoviedb import tmdb
from lib.tvdb_api import tvdb_api

try_guessing = 1
scrobble_movies = 1
scrobble_series = 1

moviedir = "/volume1/Datengrab/Filme/"
seriesdir = "/volume1/Datengrab/Serien/"

serie = "/volume1/Datengrab/Serien/Psych/Staffel 04/Psych.s04e14.Insert.Episodenamehere.avi"
movie = "/volume1/Datengrab/Filme/Captain America (2011)/21.Jump.Street.2012.mkv"

seriesregex = "(?P<name>.*).?[sS](?P<season>\d{1,2})[eE|xX|epEP|\.|-]?(?P<episode>\d{1,2})"
movieregex = "(?P<name>.*).?(?P<year>\d{4})"
moviefolderregex = "(?P<name>.*).?\(?(?P<year>\d{4})\)?"


#folder = os.path.dirname(movie).replace(moviedir,"")
#print folder

#p = re.match(moviefolderregex, folder)
#print p.group("name")
#print p.group("year")



if scrobble_movies:
	if moviedir in movie:
		mediatype = "Movie"
		if try_guessing:
			moviename = os.path.basename(movie)
			p = re.match(movieregex, moviename)
			name = p.group("name").replace("."," ").strip()
			year = p.group("year")
			searchstring = "{0} ({1})".format(name, year)
			print "DEBUG: Type: Movie, Name: {0}, Year: {1}, Searchstring: {2}".format(name, year, searchstring)
			#we need imdb id for scrobbleing to trakt, so lets make a moviedb lookup here to get these infos (especially if there is no year in the name....)
			#this ALWAYS uses the first resault that comes from tmdb...
			results = tmdb.search(searchstring)
			if results:
				firstresult = results[0]
				movieinfo = firstresult.info()
				imdb_id = movieinfo["imdb_id"]
				#print "DEBUG: tmdb gave the following keys: {0}".format(movieinfo.keys())
				title = movieinfo["original_name"]
				print "DEBUG: Found result for {0} -> Fullname: {1} imdb_id: {2}".format(searchstring, title, imdb_id)
				#return title, imdb_id
			else:
				print "ERROR: Can't find any matches for {0}: {1}".format(mediatype, searchstring)
if scrobble_series:	
	if seriesdir in serie:
		mediatype = "Series"
		if try_guessing:
			seriesname = os.path.basename(serie)
			p = re.match(seriesregex, seriesname)
			name = p.group("name").replace(".", " ").strip()
			season = p.group("season")
			episode = p.group("episode")
			print "DEBUG: Type: Series, Name: {0}, Season: {1}, Episode: {2}".format(name, season, episode) 
			t = tvdb_api.Tvdb()
			showinfo = t[name]	
			tvdb_id = showinfo["id"]
			realname = showinfo["seriesname"]
			year = showinfo["firstaired"]
			print "DEBUG: tvdb gave the following keys: {0}".format(showinfo.data.keys())
			print "DEBUG: Found result for {0} -> Fullname: {1}, tvdb_id: {2}, Year: {3}".format(name, realname, tvdb_id, year)
			#return tvdb_api, realname, season, episode
			
