import logging
from synoindex import config

logger = logging.getLogger("SynoDLNAtrakt")
hdlr = logging.FileHandler("SynoDLNAtrakt.log")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)
