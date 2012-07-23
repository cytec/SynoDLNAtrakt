# Author: cytec <iamcytec@googlemail.com>
# URL: http://github.com/cytec/SynoDLNAtrakt/
#
# This file is part of SynoDLNAtrakt.
from synodlnatrakt import trakt
import urllib2
import json

# scrobbledict = {
# 	"type": "series",
#     "tvdb_id": 153021,
#     "name": "The Walking Dead",
#     "year": 2010,
#     "season": 1,
#     "episode": 1,
#     "process": 100,
# }

postdata = {
	"type": "movie",
    "imdb_id": "tt0372784",
    "name": "Batman Begins",
    "year": 2005,
    "duration": 8400,
    "progress": 85,
    "process": 85,
}

if trakt.sendRequest(postdata):
 	print "jeah"
else:
 	print "oh noes!"

 						