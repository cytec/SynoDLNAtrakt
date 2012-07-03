import cherrypy, os
from Cheetah.Template import Template

from synodlnatrakt import helper
from synodlnatrakt.logger import logger
from synodlnatrakt import config
from synodlnatrakt import db

APPDIR = os.path.dirname(os.path.abspath(__file__))
INI_FILENAME = os.path.join(APPDIR, "webserve.ini")

class Root(object):
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
		filename = os.path.join(APPDIR, "data/logs.tmpl")
		template = Template(file = filename)

		template.title = "SynoDLNAtrakt Logs"
		template.content = logcontent
		return str(template)  
	log.exposed = True
	index.exposed = True

	def runSyno(self):
		os.popen("python SynoDLNAtrakt.py")
	log.runSyno = True
	index.runSyno = True

def main():
	cherrypy.quickstart(Root(), config = INI_FILENAME)


if __name__ == "__main__":
	main()