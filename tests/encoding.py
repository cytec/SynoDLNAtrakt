#!/usr/bin/python
# Author: cytec <iamcytec@googlemail.com>
# URL: http://github.com/cytec/SynoDLNAtrakt/
#
# This file is part of SynoDLNAtrakt.

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