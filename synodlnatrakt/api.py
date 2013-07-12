from synodlnatrakt.mediaelement import Episode, Movie
from synodlnatrakt import db, trakt, config
from datetime import datetime, timedelta
from synodlnatrakt.timer import sched
from synodlnatrakt import logger, helper, main, mediaimport
from lib.bottle import route, post, template, run, static_file, request, response
from apscheduler.scheduler import Scheduler
import json
from lib.themoviedb import tmdb
import os
import re
from synodlnatrakt import ui, versioncheck
from math import ceil



@route('/api/<api_key>')
def list_methods(api_key):
    if api_key == config.apikey:
        methods = []
        methods.append({"name": "list movies", "url": "/api/apikey/list/movies"})
        return json.dumps({"result": "success", "message": "Valid API key {0}", "data": methods})
    else:
        return json.dumps({"result": "error", "message": "Invalid API key {0}"})


@route('/api/<api_key>/list/<kind_of>')
def list_methods(api_key):
    if api_key == config.apikey:
        if kind_of == "movies":

        elif kind_of == "series":

        elif kind_of == "episode":

    else:
        pass

@route('/api/<api_key>/info/<kind_of>')
def list_methods(api_key):
    if api_key == config.apikey:
        if kind_of == "movies":

        elif kind_of == "series":

        elif kind_of == "episode":

    else:
        pass

