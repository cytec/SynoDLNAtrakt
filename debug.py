#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
base_path = os.path.dirname(os.path.abspath(__file__))

# Insert local directories into path
sys.path.append(os.path.join(base_path, 'lib'))


from synodlnatrakt.timer import sched
from synodlnatrakt import config

config.initialize()
config.save_config()

from datetime import datetime, timedelta


from synodlnatrakt import web
from synodlnatrakt import main, versioncheck
from lib.bottle import TEMPLATE_PATH

config.initialize()
config.save_config()

versioncheck.getVersion()
versioncheck.checkGithub()

parse_logs_int = int(config.interval)
mediaserver_int = int(config.interval)
trakt_sync_int = 240  # int(config.interval) * 8

starttime = datetime.now()

@sched.interval_schedule(minutes=parse_logs_int, start_date=starttime + timedelta(minutes=1))
def parse_logs():
    main.scanlogs()

@sched.interval_schedule(minutes=mediaserver_int, start_date=starttime + timedelta(minutes=1))
def mediaserver():
    main.import_mediaserver()

@sched.interval_schedule(minutes=trakt_sync_int, start_date=starttime + timedelta(minutes=2))
def sync_trakt():
    main.update_movies()

@sched.interval_schedule(minutes=trakt_sync_int, start_date=starttime + timedelta(minutes=1))
def update_checker():
    main.checkupdate()

@sched.interval_schedule(minutes=trakt_sync_int ,start_date=starttime + timedelta(seconds=10))
def generate_stats():
    main.generate_stats()

if config.delete_orphans:
    @sched.interval_schedule(minutes=480, start_date=starttime+timedelta(minutes=60))
    def delete_orphans():
        main.delete_orphans()

sched.start()
main.update_db()
#sched.print_jobs()

TEMPLATE_PATH.insert(0, config.templatedir)

web.run(host='0.0.0.0', port=config.port, debug=True)

while True:
    pass