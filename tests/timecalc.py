# Author: cytec <iamcytec@googlemail.com>
# URL: http://github.com/cytec/SynoDLNAtrakt/
#
# This file is part of SynoDLNAtrakt.

import time, datetime

gesehen = "00:38:23"
length = "00:48:18"

def durationStamps(time):
	h, m, s = time.split(":")
	time = int(h*60)
	time = (time + int(m))*60
	time = (time + int(s))
	return time

def getProcess(length, viewed):
	minpercent = 80
	length = durationStamps(length)
	viewed = durationStamps(viewed)
	percent = viewed / (length / 100)
	print "Duration: {0}s, Viewed: {1}s = {2}% watched".format(length, viewed, percent)
	if percent > 80:
		print "going to scrobble"
	else:
		print "{0}% is not enoutgh to scrobble... you need at least {1}".format(percent, minpercent)


getProcess(length, gesehen)