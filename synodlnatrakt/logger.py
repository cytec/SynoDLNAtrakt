# Author: cytec <iamcytec@googlemail.com>
# URL: http://github.com/cytec/SynoDLNAtrakt/
#
# This file is part of SynoDLNAtrakt.

import logging
import logging.handlers
from synodlnatrakt import config
from os import path, makedirs

if not path.exists(path.join(config.datadir, "logs")):
    makedirs(path.join(config.datadir, "logs"))

ERROR = logging.ERROR
WARNING = logging.WARNING
MESSAGE = logging.INFO
DEBUG = logging.DEBUG

LOG_FILENAME = path.join(config.datadir, "logs/SynoDLNAtrakt.log")

logger = logging.getLogger("SynoDLNAtrakt")
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s', '%d.%m.%Y %H:%M:%S')

rotation = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=5 * 1024 * 1024, backupCount=5)
rotation.setFormatter(formatter)
logger.addHandler(rotation)


# log to console:
if config.logtoconsole:
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

if config.debugmode:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
