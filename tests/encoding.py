#!/usr/bin/python

import os

from synodlnatrakt import config
from synodlnatrakt import encodingKludge as ek

print config.SYS_ENCODING

buggyname = "Hawaii.Five-0.s02e14.Das.P\xc3\xa4ckchen.SD.TV.avi"

try:
	fixedname = ek.ek(os.path.abspath, buggyname)
except:
	fixedname = ek.fixStupidEncodings(buggyname)


print buggyname, fixedname