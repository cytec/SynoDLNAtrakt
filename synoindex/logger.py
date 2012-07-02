import logging
from synoindex import config

logger = logging.getLogger("SynoDLNAtrakt")

hdlr = logging.FileHandler("SynoDLNAtrakt.log")
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s','%d.%m.%Y %H:%M:%S')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 

#log to console:
if config.logtoconsole:
	console = logging.StreamHandler()
	console.setFormatter(formatter)
	logger.addHandler(console) 

logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
