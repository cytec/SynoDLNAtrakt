# Author: cytec <iamcytec@googlemail.com>
# URL: http://github.com/cytec/SynoDLNAtrakt/
#
# This file is part of SynoDLNAtrakt.

import os
from lib.configobj import ConfigObj
import hashlib

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

datadir = basedir

cfg_path = os.path.join(datadir, "config.ini")


SYS_ENCODING = ''
BASEPATH = os.getcwd()

# list of mediafile extensions
medialist = ["avi", "mkv", "mov", "mp4", "m4v", "ts", "hdmov", "wmv", "mpg", "mpeg", "xvid"]

# regex for getting the id and extension from access.log
logregex = ".*/(?P<theid>\d{1,5})\.(?P<ext>\w{3,5}).*"
seriesregex = "(?P<name>.*).?[sS](?P<season>\d{1,2})[eE|xX|epEP|\.|-]?(?P<episode>\d{1,2})"
movieregex = "(?P<name>[^()]*)\.?\(?(?P<year>\d{4})\)?"

TITLE_SPLIT_KEYWORDS = [
    "[", "]", "~", "(", ")", "dvdscr", "dvdrip", "dvd-rip", "dvdr", "vcd",
    "divx", "xvid", "ac3", "r5", "pal", "readnfo", "uncut", "cd1", "cd2",
    "dvdiso", "md", "bdrip", "german", "french", "hdrip", "extended", "br-ripdvd",
    "complete", "720p", "1080p", "hdtv", "br-rip", "dubbed"
]

    # Title strip items
TITLE_STRIP_SEARCH = [".", "-", "_"]

# remove this trash from filename before trying to guess it... ex:
# My.Movie.German.2012.UNCUT.720p.AC3.mkv will become My.Movie.2012.mkv
removejunk = ["BR-Ripdvd", "BR-Rip", "DVDRip", "German", "Dubbed", "uncut", "extendet", "complete", "bluray", "720p",
              "1080p", "hdtv", "PAL", "DL", "AC3", "DVD-Rip", "dvd", "720P"]

trakt_key = "860f1d1eda847c3b934a2d942eef110e13d21b12"

the_srings = ["the ", "der ", "die ", "das "]


templatedir = os.path.join(basedir, "views/")
cachedir = os.path.join(datadir, "cache")

latest_version = None
current_version = None
commits_behind = 0

accesslog = None
moviedir = ""
seriesdir = ""
try_guessing = 1
delete_logs = 0
absolute_ep_anime = 1
hide_watched = 0
# datadir = None
logtoconsole = 0
debugmode = 1
min_progress = 80
interval = 30
language = "en"
port = 1337
username = None
password = None
page_limit = 50
trakt_pass = ""
trakt_user = None
use_boxcar = 0
boxcar_username = None
move_watched_movies = 0
move_watched_series = 0
move_movies_to_dir = None
move_series_to_dir = None
update_synoindex = 0
delete_from_index = 0
delete_from_disk = 0
watched_flags = 1
CFG = "aa"
sha1hash = None
add_to_list = 0
list_name = "watchlist"
blur_images = 1


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
    #     print "{0} -> {1}".format(item_name, my_val)
    # else:
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
    # print "{0} -> {1}".format(item_name, str(my_val))
    return my_val


def initialize():
    global CFG, username, password, accesslog, moviedir, seriesdir, try_guessing, delete_logs,\
        absolute_ep_anime, hide_watched, datadir, logtoconsole, debugmode, min_progress, interval, \
        language, port, page_limit, trakt_user, trakt_pass, use_boxcar, boxcar_username, \
        move_watched_movies, move_watched_series, move_movies_to_dir, move_series_to_dir, update_synoindex, \
        delete_from_index, delete_from_disk, cachedir, datadir, dbpath, sha1hash, add_to_list, list_name, blur_images

    CFG = ConfigObj(cfg_path)

    CheckSection('General')
    CheckSection('Advanced')
    CheckSection('Trakt')
    CheckSection('Boxcar')
    CheckSection('Postprocessing')

    # general
    accesslog = check_setting_str(CFG, 'General', 'accesslog', '/var/log/lighttpd/access.log')
    moviedir = check_setting_str(CFG, 'General', 'moviedir', '/path/to/moviedir/|/path/to/2nd/moviedir/').split('|')
    seriesdir = check_setting_str(CFG, 'General', 'seriesdir', '/path/to/seriesdir/|/path/to/2nd/seriesdir/').split('|')
    try_guessing = bool(check_setting_int(CFG, 'General', 'try_guessing', 1))
    delete_logs = bool(check_setting_int(CFG, 'General', 'delete_logs', 0))
    absolute_ep_anime = bool(check_setting_int(CFG, 'General', 'absolute_ep_anime', 1))
    hide_watched = bool(check_setting_int(CFG, 'General', 'hide_watched', 0))
    datadir = check_setting_str(CFG, 'General', 'datadir', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # adcanced
    logtoconsole = bool(check_setting_int(CFG, 'Advanced', 'logtoconsole', 0))
    debugmode = bool(check_setting_int(CFG, 'Advanced', 'debugmode', 1))
    min_progress = check_setting_int(CFG, 'Advanced', 'min_progress', 80)
    interval = check_setting_int(CFG, 'Advanced', 'interval', 30)
    language = check_setting_str(CFG, 'Advanced', 'language', 'en')
    port = check_setting_int(CFG, 'Advanced', 'port', 1337)
    username = check_setting_str(CFG, 'Advanced', 'username', '')
    password = check_setting_str(CFG, 'Advanced', 'password', '')
    page_limit = check_setting_str(CFG, 'Advanced', 'page_limit', 50)
    watched_flags = bool(check_setting_int(CFG, 'Advanced', 'watched_flags', 1))
    blur_images = bool(check_setting_int(CFG, 'Advanced', 'blur_images', 1))

    # trakt
    trakt_pass = check_setting_str(CFG, 'Trakt', 'trakt_pass', '')
    trakt_user = check_setting_str(CFG, 'Trakt', 'trakt_user', '')
    add_to_list = bool(check_setting_int(CFG, 'Trakt', 'add_to_list', 0))
    list_name = check_setting_str(CFG, 'Trakt', 'list_name', 'watchlist')

    # boxcar
    use_boxcar = bool(check_setting_int(CFG, 'Boxcar', 'use_boxcar', 0))
    boxcar_username = check_setting_str(CFG, 'Boxcar', 'boxcar_username', '')

    # postprocessing
    move_watched_movies = bool(check_setting_int(CFG, 'Postprocessing', 'move_watched_movies', 0))
    move_watched_series = bool(check_setting_int(CFG, 'Postprocessing', 'move_watched_series', 0))
    move_movies_to_dir = check_setting_str(CFG, 'Postprocessing', 'move_movies_to_dir', '/path/to/viewed/moviedir/')
    move_series_to_dir = check_setting_str(CFG, 'Postprocessing', 'move_series_to_dir', '/path/to/viewed/seriesdir/')
    update_synoindex = bool(check_setting_int(CFG, 'Postprocessing', 'update_synoindex', 0))
    delete_from_index = bool(check_setting_int(CFG, 'Postprocessing', 'delete_from_index', 0))
    delete_from_disk = bool(check_setting_int(CFG, 'Postprocessing', 'delete_from_disk', 0))

    cachedir = os.path.join(datadir, "cache")

    save_config()

    sha1hash = hashlib.sha1(trakt_pass).hexdigest()

    dbpath = os.path.join(datadir, "SynoDLNAtrakt.db")

    if not os.path.exists(datadir):
        os.makedirs(datadir)

    if not os.path.exists(cachedir):
        os.makedirs(cachedir)


def save_config():

    new_config = ConfigObj()
    new_config.filename = cfg_path

    new_config['General'] = {}
    new_config['General']['accesslog'] = accesslog
    new_config['General']['moviedir'] = '|'.join(moviedir)
    new_config['General']['seriesdir'] = '|'.join(seriesdir)
    new_config['General']['try_guessing'] = int(try_guessing)
    new_config['General']['delete_logs'] = int(delete_logs)
    new_config['General']['absolute_ep_anime'] = int(absolute_ep_anime)
    new_config['General']['hide_watched'] = int(hide_watched)
    new_config['General']['datadir'] = datadir

    new_config['Advanced'] = {}
    new_config['Advanced']['logtoconsole'] = int(logtoconsole)
    new_config['Advanced']['debugmode'] = int(debugmode)
    new_config['Advanced']['min_progress'] = int(min_progress)
    new_config['Advanced']['interval'] = int(interval)
    new_config['Advanced']['language'] = language
    new_config['Advanced']['port'] = int(port)
    new_config['Advanced']['username'] = username
    new_config['Advanced']['password'] = password
    new_config['Advanced']['page_limit'] = int(page_limit)
    new_config['Advanced']['watched_flags'] = int(watched_flags)
    new_config['Advanced']['blur_images'] = int(blur_images)

    new_config['Trakt'] = {}
    new_config['Trakt']['trakt_pass'] = trakt_pass
    new_config['Trakt']['trakt_user'] = trakt_user
    new_config['Trakt']['add_to_list'] = int(add_to_list)
    new_config['Trakt']['list_name'] = list_name

    new_config['Boxcar'] = {}
    new_config['Boxcar']['use_boxcar'] = int(use_boxcar)
    new_config['Boxcar']['boxcar_username'] = boxcar_username

    new_config['Postprocessing'] = {}
    new_config['Postprocessing']['move_watched_movies'] = int(move_watched_movies)
    new_config['Postprocessing']['move_watched_series'] = int(move_watched_series)
    new_config['Postprocessing']['move_movies_to_dir'] = move_movies_to_dir
    new_config['Postprocessing']['move_series_to_dir'] = move_series_to_dir
    new_config['Postprocessing']['update_synoindex'] = int(update_synoindex)
    new_config['Postprocessing']['delete_from_index'] = int(delete_from_index)
    new_config['Postprocessing']['delete_from_disk'] = int(delete_from_disk)

    new_config.write()
    sha1hash = hashlib.sha1(trakt_pass).hexdigest()
