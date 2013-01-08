# Author: cytec <iamcytec@googlemail.com>
# URL: http://github.com/cytec/SynoDLNAtrakt/
#
# This file is part of SynoDLNAtrakt.

import logging
from synodlnatrakt import config
from os import path, makedirs

if not path.exists(path.join(config.datadir, "logs")):
	makedirs(path.join(config.datadir, "logs"))

ERROR = logging.ERROR
WARNING = logging.WARNING
MESSAGE = logging.INFO
DEBUG = logging.DEBUG

logger = logging.getLogger("SynoDLNAtrakt")

hdlr = logging.FileHandler(path.join(config.datadir, "logs/SynoDLNAtrakt.log"))
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s','%d.%m.%Y %H:%M:%S')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 

#log to console:
if config.logtoconsole:
	console = logging.StreamHandler()
	console.setFormatter(formatter)
	logger.addHandler(console) 

logger.addHandler(hdlr)

if config.debugmode:
	logger.setLevel(logging.DEBUG)
else:
	logger.setLevel(logging.INFO)