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
        ratio = max_width * 1. / width
        return (int(width * ratio), int(height * ratio))
    return (width, height)


def get_images(theid, thetype):
        # download the covers for series
        # download thumbs and fanart from fanart.tv
        # covers from tvdb or tmdb

    if not os.path.exists(os.path.join(config.cachedir, "cover/")):
        os.makedirs(os.path.join(config.cachedir, "cover/"))
    if not os.path.exists(os.path.join(config.cachedir, "fanart/")):
        os.makedirs(os.path.join(config.cachedir, "fanart/"))

    coverpath = os.path.join(config.cachedir, "cover/{0}.jpg".format(theid))
    fanartpath = os.path.join(config.cachedir, "fanart/{0}.jpg".format(theid))

    logger.debug(u"COVERPATH -> {0}".format(coverpath))
    logger.debug(u"FANARTPATH -> {0}".format(fanartpath))

    if thetype == "series":
        url = "http://api.trakt.tv/show/summary.json/{0}/{1}".format(config.trakt_key, theid)

    if thetype == "movie":
        url = "http://api.trakt.tv/movie/summary.json/{0}/{1}".format(config.trakt_key, theid)

    if not os.path.exists(coverpath) or not os.path.exists(fanartpath):
        r = requests.get(url)
        if r and r.status_code == 200:
            cover_url = "{0}-300.jpg".format(os.path.splitext(r.json()["images"]["poster"])[0])
            fanart_url = "{0}-940.jpg".format(os.path.splitext(r.json()["images"]["fanart"])[0])
            logger.debug(u"{0}, {1}".format(cover_url, fanart_url))

            if not os.path.exists(coverpath):
                try:
                    cover = requests.get(cover_url)
                    if cover.status_code == 200 and "image" in cover.headers["content-type"]:
                        f = open(coverpath, "w")
                        f.write(cover.content)
                        f.close()
                        logger.debug(u"downloaded poster for {0}".format(theid))
                except:
                    logger.debug(u"unable to download poster for {0}".format(theid))

            if not os.path.exists(fanartpath):
                try:
                    fanart = requests.get(fanart_url)
                    if fanart.status_code == 200 and "image" in fanart.headers["content-type"]:
                        f = open(fanartpath, "w")
                        f.write(fanart.content)
                        f.close()
                        logger.debug(u"downloaded fanart for {0}".format(theid))
                except:
                    logger.debug(u"unable to download fanart for {0}".format(theid))

                if os.path.exists(fanartpath) and config.blur_images:
                    im = Image.open(fanartpath)
                    im = im.filter(MyGaussianBlur(radius=7))
                    logger.debug(u"blured fanart for {0}".format(theid))
                    im.save(fanartpath)
