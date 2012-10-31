from synodlnatrakt import config
from synodlnatrakt import helper

print config.BASEPATH

videoinfo = helper.getVideoInfo(13363)
print videoinfo.path, videoinfo.duration

helper.markScrobbled(3)

dbobj = helper.mediaelementFromDatabase(3)
print dbobj.name