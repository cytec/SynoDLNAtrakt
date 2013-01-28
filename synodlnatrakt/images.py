import Image
import ImageFilter
from lib.tvdb_api import tvdb_api
from lib.themoviedb import tmdb
import os
import requests

from synodlnatrakt.logger import logger
from synodlnatrakt import config



class MyGaussianBlur(ImageFilter.Filter):
    name = "GaussianBlur"

    def __init__(self, radius=2):
        self.radius = radius
    def filter(self, image):
        return image.gaussian_blur(self.radius)


def scale_dimensions(width, height, max_width):
    if width > max_width:
        ratio = max_width*1./width
        return (int(width*ratio), int(height*ratio))
    return (width, height)


def get_images(theid, thetype):
	#download the covers for series
	#download thumbs and fanart from fanart.tv
	#covers from tvdb or tmdb

	if not os.path.exists(os.path.join(config.cachedir,"cover/")):
		os.makedirs(os.path.join(config.cachedir,"cover/"))
	if not os.path.exists(os.path.join(config.cachedir,"fanart/")):
		os.makedirs(os.path.join(config.cachedir,"fanart/"))

	coverpath = os.path.join(config.cachedir,"cover/{0}.jpg".format(theid))
	fanartpath = os.path.join(config.cachedir,"fanart/{0}.jpg".format(theid))

	logger.debug(u"COVERPATH -> {0}".format(coverpath))
	logger.debug(u"FANARTPATH -> {0}".format(fanartpath))

	if thetype == "series":
		t = tvdb_api.Tvdb(language=config.language)
		show = t[int(theid)]
		
		if not os.path.exists(coverpath):
			try:
				#urllib.urlretrieve(show["poster"], coverpath)
				r = requests.get(show["poster"])
				if r.status_code == 200 and "image" in r.headers["content-type"]:
					f = open(coverpath, "w")
					f.write(r.content)
					f.close()
					logger.debug(u"Downloading Poster for {0}".format(theid))
			except:
				logger.debug(u"Unable to Download Poster for {0}".format(theid))
			
			if os.path.exists(coverpath):
				im = Image.open(coverpath)
				if im.size[0] > 320:
					new_size = scale_dimensions(im.size[0], im.size[1], 320)
					im = im.resize(new_size, Image.ANTIALIAS)
					im.save(coverpath)
		else:
			logger.debug(u"Cover already exists")

		
		if not os.path.exists(fanartpath):
			try:
				r = requests.get(show["fanart"])
				if r.status_code == 200 and "image" in r.headers["content-type"]:
					f = open(fanartpath, "w")
					f.write(r.content)
					f.close()
					logger.debug(u"Downloading Fanart for {0}".format(theid))
			except:
				logger.debug(u"Unable to Download Fanart for {0}".format(theid))
			
			if os.path.exists(fanartpath):
				im = Image.open(fanartpath)
				if im.size[0] > 1200:
					new_size = scale_dimensions(im.size[0], im.size[1], 1200)
					im = im.resize(new_size, Image.ANTIALIAS)
					logger.info(u"Resized Fanart")
					im = im.filter(MyGaussianBlur(radius=7))
					logger.info(u"Blured Fanart")
					im.save(fanartpath)
		else:
			logger.debug(u"Fanart already exists")
	

		

	
		
	if thetype == "movie":
		movieinfo = tmdb.getMovieInfo(theid, lang=config.language)
		if not os.path.exists(coverpath):
			try:
				r = requests.get(movieinfo["images"][0]["original"])

				if r.status_code == 200 and "image" in r.headers["content-type"]:
					f = open(coverpath, "w")
					f.write(r.content)
					f.close()
					logger.debug(u"Downloading Poster for {0}".format(theid))
			except:
				logger.debug(u"Unable to Download Poster for {0}".format(theid))

			if os.path.exists(coverpath):
				im = Image.open(coverpath)
				if im.size[0] > 320:
					new_size = scale_dimensions(im.size[0], im.size[1], 320)
					im = im.resize(new_size, Image.ANTIALIAS)
					im.save(coverpath)
	
		else:
			logger.debug(u"Cover already exists")

		if not os.path.exists(fanartpath):
			try:
				r = requests.get(movieinfo["images"][-1]["original"])
				if r.status_code == 200 and "image" in r.headers["content-type"]:
					f = open(fanartpath, "w")
					f.write(r.content)
					f.close()
					logger.debug(u"Downloading Fanart for {0}".format(theid))
			except:
				logger.debug(u"Unable to Download Fanart for {0}".format(theid))

			if os.path.exists(fanartpath):
				im = Image.open(fanartpath)
				if im.size[0] > 1200:
					new_size = scale_dimensions(im.size[0], im.size[1], 1200)
					im = im.resize(new_size, Image.ANTIALIAS)
					logger.info(u"Resized Fanart")
					im = im.filter(MyGaussianBlur(radius=7))
					logger.info(u"Blured Fanart")
					im.save(fanartpath)
		else:
			logger.debug(u"Fanart already exists")
	




