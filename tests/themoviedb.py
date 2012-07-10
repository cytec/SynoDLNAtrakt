from lib.themoviedb import tmdb
import urllib
import os

searchstring = "The Avengers"
results = tmdb.search(searchstring)
#print results
cachedir = "data/cache/"
name = cachedir + results[0]["imdb_id"] + '.jpg'

url = results[0]["images"][0]["original"]
imagedata = urllib.urlopen(url).read()
f = open(name, 'w')
f.write(imagedata)
f.close()