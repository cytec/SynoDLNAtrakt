import re, os
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('synoindex.ini')

accesslog = parser.get('General', 'accesslog')
psql = parser.get('General', 'psql')
seriesdir = parser.get('General', 'seriesdir').split(',')
moviedir = parser.get('General', 'moviedir').split(',')
scrobble_series = parser.get('General', 'scrobble_series')
scrobble_movies = parser.get('General', 'scrobble_movies')
try_guessing = parser.get('General', 'try_guessing')
trakt_user = parser.get('Trakt', 'trakt_user')
trakt_pass = parser.get('Trakt', 'trakt_pass')
trakt_key = parser.get('Trakt', 'trakt_key')
