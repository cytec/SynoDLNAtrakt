import apachelog, os, sys, re

accesslog = "logparser.log"

p = apachelog.parser(apachelog.formats['lighttpd'])
time_format = "[%d/%b/%Y:%H:%M:%S +0200]"
regex = ".*(?P<theid>\d{5})\.(?P<ext>\w{3,5})"

testlist = ["mkv","mp4","avi"]

for line in open(accesslog):
	try:
		data = p.parse(line)
		x = re.match(regex, data["%r"])
		
		if x.group("ext") not in testlist:
			continue

		print x.group("theid"),x.group("ext")
       
	except:
		sys.stderr.write("Unable to parse %s" % line)
           #print "no"