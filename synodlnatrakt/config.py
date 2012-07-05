# Author: cytec <iamcytec@googlemail.com>
# URL: http://github.com/cytec/SynoDLNAtrakt/
#
# This file is part of SynoDLNAtrakt.

import os, sys, locale
from lib.configobj import ConfigObj
#from synoindex.logger import logger
#import logging gave error cause of endless redirects -.-

CFG = ConfigObj("SynoDLNAtrakt.ini")
CONFIG_FILE = "SynoDLNAtrakt.ini"
SYS_ENCODING = ''

try:
    locale.setlocale(locale.LC_ALL, "")
    SYS_ENCODING = locale.getpreferredencoding()
except (locale.Error, IOError):
    pass

# for OSes that are poorly configured I'll just force UTF-8
if not SYS_ENCODING or SYS_ENCODING in ('ANSI_X3.4-1968', 'US-ASCII', 'ASCII'):
    SYS_ENCODING = 'UTF-8'


def CheckSection(sec):
    """ Check if INI section exists, if not create it """
    try:
        CFG[sec]
        return True
    except:
        CFG[sec] = {}
        return False

def check_setting_str(config, cfg_name, item_name, def_val, log=True):
    try:
        my_val = config[cfg_name][item_name]
    except:
        my_val = def_val
        try:
            config[cfg_name][item_name] = my_val
        except:
            config[cfg_name] = {}
            config[cfg_name][item_name] = my_val

    # if log:
    #     #logger.debug("{0} -> {1}".format(item_name, my_val))
    #     print "{0} -> {1}".format(item_name, my_val)
    # else:
    #     #logger.debug("{0} -> ******".format(item_name))
    #     print "{0} -> ******".format(item_name)
    return my_val


def check_setting_int(config, cfg_name, item_name, def_val):
    try:
        my_val = int(config[cfg_name][item_name])
    except:
        my_val = def_val
        try:
            config[cfg_name][item_name] = my_val
        except:
            config[cfg_name] = {}
            config[cfg_name][item_name] = my_val
    #logger.debug("{0} -> {1}".format(item_name, str(my_val)))
    #print "{0} -> {1}".format(item_name, str(my_val))
    return my_val
    

CheckSection('General')
CheckSection('Advanced')
CheckSection('Trakt')
CheckSection('Boxcar')

#general
psql = check_setting_str(CFG, 'General', 'psql', '/usr/syno/pgsql/bin/psql')
accesslog = check_setting_str(CFG, 'General', 'accesslog', '/var/log/lighttpd/access.log')
moviedir = check_setting_str(CFG, 'General', 'moviedir', ['/path/to/moviedir/', '/path/to/2nd/moviedir/'])
seriesdir = check_setting_str(CFG, 'General', 'seriesdir', ['/path/to/seriesdir/', '/path/to/2nd/seriesdir/'])
try_guessing = bool(check_setting_int(CFG, 'General', 'try_guessing', 1))
delete_logs = bool(check_setting_int(CFG, 'General', 'delete_logs', 0))
scrobble_series = bool(check_setting_int(CFG, 'General', 'scrobble_series', 1))
use_database = bool(check_setting_int(CFG, 'General', 'use_database', 1))
scrobble_movies = bool(check_setting_int(CFG, 'General', 'scrobble_movies', 1))


#adcanced
logtoconsole = bool(check_setting_int(CFG, 'Advanced', 'logtoconsole', 0))
debugmode = bool(check_setting_int(CFG, 'Advanced', 'debugmode', 0))
min_progress = check_setting_int(CFG, 'Advanced', 'min_progress', 80)
interval = check_setting_int(CFG, 'Advanced', 'interval', 12)

#trakt
trakt_pass = check_setting_str(CFG, 'Trakt', 'trakt_pass', '')
trakt_user = check_setting_str(CFG, 'Trakt', 'trakt_user', '')
trakt_key = check_setting_str(CFG, 'Trakt', 'trakt_key', '')

#boxcar
use_boxcar = bool(check_setting_int(CFG, 'Boxcar', 'use_boxcar', 0))
boxcar_username = check_setting_str(CFG, 'Boxcar', 'boxcar_username', '')

def save_config():

    new_config = ConfigObj()
    new_config.filename = CONFIG_FILE

    new_config['General'] = {}
    new_config['General']['psql'] = psql
    new_config['General']['accesslog'] = accesslog
    new_config['General']['moviedir'] = moviedir
    new_config['General']['seriesdir'] = seriesdir
    new_config['General']['try_guessing'] = int(try_guessing)
    new_config['General']['delete_logs'] = int(delete_logs)
    new_config['General']['scrobble_series'] = int(scrobble_series)
    new_config['General']['use_database'] = int(use_database)
    new_config['General']['scrobble_movies'] = int(scrobble_movies)
    
    new_config['Advanced'] = {}
    new_config['Advanced']['logtoconsole'] = int(logtoconsole)
    new_config['Advanced']['debugmode'] = int(debugmode)
    new_config['Advanced']['min_progress'] = min_progress
    new_config['Advanced']['interval'] = interval

    new_config['Trakt'] = {}
    new_config['Trakt']['trakt_pass'] = trakt_pass
    new_config['Trakt']['trakt_user'] = trakt_user
    new_config['Trakt']['trakt_key'] = trakt_key

    new_config['Boxcar'] = {}
    new_config['Boxcar']['use_boxcar'] = int(use_boxcar)
    new_config['Boxcar']['boxcar_username'] = boxcar_username

    new_config.write()

save_config()