# Author: cytec <iamcytec@googlemail.com>
# URL: http://github.com/cytec/SynoDLNAtrakt/
#
# This file is part of SynoDLNAtrakt.
import os
import datetime
from synodlnatrakt import db

onlyuncomplete = False

db.checkDB()
myDB = db.DBConnection()

if onlyuncomplete:
  reslut = myDB.select("SELECT * from scrobble where process < 80")
else:
  reslut = myDB.select("SELECT * from scrobble")

if reslut:
  #print reslut
  for item in reslut:
    filename = os.path.split(item["thepath"])[1]
    thedate = datetime.datetime.fromtimestamp(float(item["lastviewed"]))

    timedelta = thedate + datetime.timedelta(weeks=4)
    if timedelta < datetime.datetime.now():
      print u"Deleting {0} from database because lastviewed more than 8 weeks ago".format(filename)
      myDB.action("DELETE from scrobble where id = {0}".format(item["id"]))
    else:
      print filename + " seems to be ok"
    #print item["lastviewed"], filename