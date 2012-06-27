# /var/log/lighttpd/access.log


#192.168.0.10 192.168.0.55:50002 - [20/Jun/2012:21:44:43 +0200] "GET /v/NDLNA/13282.avi HTTP/1.1" 206 3557410 "-" "Mozilla/5.0 (compatible; LG-HttpClient-v1.0.3 UPnP/1.1; MSIE 8.0; Windows NT 5.1; LG_UA; AD_LOGON=LGE.NET; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; LG_UA; AD_LOGON=LGE.NET; LG NetCast.TV-2011)"

#13282.avi is the ID from the DB with extension...

# /usr/syno/pgsql/bin/psql mediaserver admin -tA -c "select path from video where id = 13282"

#/volume1/Datengrab/Serien/Psych/Staffel 04/Psych.s04e14.Spagat.zwischen.Attentat.und.Heldentat.SD.DVD.avi

# if in folder Series, then its a Series... go on and search for a nfo file thats named the same

#/volume1/Datengrab/Serien/Psych/Staffel 04/Psych.s04e14.Spagat.zwischen.Attentat.und.Heldentat.SD.DVD.nfo

#change sickbeard to reflect the epid in nfo files, too... so we can scrobble it to trakt.tv
#for now:

#go to series folder, check show id
#/volume1/Datengrab/Serien/Psych/tvshow.nfo
#    <id>79335</id>

#use the id to get S04E14 info from thetvdb via api and then scrobble it to trakt...
#calculate lenght of requests and only scrobble if more than 70% are viewed

#   Column     |            Type             |                     Modifiers                      | Description 
# ----------------+-----------------------------+----------------------------------------------------+-------------
#  id             | integer                     | not null default nextval('video_id_seq'::regclass) | 
#  path           | text                        | not null                                           | 
#  title          | text                        | not null                                           | 
#  filesize       | bigint                      | not null default 0                                 | 
#  album          | text                        |                                                    | 
#  frame_bitrate  | integer                     |                                                    | 
#  duration       | integer                     |                                                    | 
#  resolutionx    | integer                     |                                                    | 
#  resolutiony    | integer                     |                                                    | 
#  audio_bitrate  | integer                     |                                                    | 
#  frequency      | integer                     |                                                    | 
#  channel        | integer                     |                                                    | 
#  date           | timestamp without time zone |                                                    | 
#  mdate          | timestamp without time zone |                                                    | 
#  fs_uuid        | text                        |                                                    | 
#  fs_online      | boolean                     | default true                                       | 
#  container_type | text                        |                                                    | 
#  frame_rate_num | integer                     |                                                    | 
#  frame_rate_den | integer                     |                                                    | 
#  video_bitrate  | text                        |                                                    | 
#  video_codec    | text                        |                                                    | 
#  audio_codec    | text                        |                                                    | 
#  video_profile  | integer                     |                                                    | 
#  video_level    | integer                     |                                                    | 
# Indexes: 
#     "video_pkey" PRIMARY KEY, btree (id)
#     "video_path_idx" UNIQUE, btree (path)
#     "video_date_idx" btree (date)
#     "video_mdate_idx" btree (mdate)
#     "video_title_idx" btree (title)
# Has OIDs: no




##### Library setup:

table scrobble

id = id der serie, unique
scrobble = 1 / 0
prozess = 0-100%
date = watched date (timestamp) 
serie = serienname
episode = epnummer
Staffel = staffelnummer
Pfad = Pfad zur datei

table synoindex
version = versionnummer
lastscrobble = date from last scribble (timestamp)
