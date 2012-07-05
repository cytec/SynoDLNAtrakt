# Author: cytec <iamcytec@googlemail.com>
# URL: http://github.com/cytec/SynoDLNAtrakt/
#
# This file is part of SynoDLNAtrakt.

import cherrypy
from Cheetah.Template import Template

from synodlnatrakt import helper
from synodlnatrakt.logger import logger
from synodlnatrakt import config
from synodlnatrakt import db

class MainWebsite(object):
	def index(self):
		return 'Please check your <a href="settings">settings</a><br /> or your <a href="log">logfile</a>'
	index.exposed = True
    
	def settings(self):
		return "Hello world!"
	settings.exposed = True
	index.exposed = True

	def log(self):
		logcontent = open('SynoDLNAtrakt.log').read()
		message = "<code>{0}</code>".format(logcontent)
		return logcontent
	log.exposed = True
	index.exposed = True

cherrypy.quickstart(MainWebsite())