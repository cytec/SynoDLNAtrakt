<!doctype html>
%from synodlnatrakt import db, config
%moviecount = db.session.query(db.Movies).count()
%seriescount = db.session.query(db.TVShows).count()
<html class="no-js" lang="de">
<head>
  <meta charset="utf-8">

  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

  <title>{{title}}</title>
  <meta name="description" content="">

  <meta name="viewport" content="width=device-width">

  <link rel="stylesheet" href="/static/css/bootstrap.css">
  <link rel="stylesheet" href="/static/css/bootstrap-responsive.css">
	<link rel="stylesheet" href="/static/css/font-awesome.css">
  <link rel="stylesheet" href="/static/css/notification.css">
  <link rel="stylesheet" href="/static/css/shadowbox.css">
  <link rel="stylesheet" href="/static/css/style.css">
  <link rel="stylesheet" href="/static/css/jquery.ias.css">
  <script src="/static/js/libs/jquery-1.8.1.min.js"></script>

  <script type="text/javascript">
    $(function() {
      $('.nav .{{topmenu}}').addClass("active")
    });   
  </script>

</head>
<body>  

  <header>
    <div class="navbar">
      <div class="navbar-inner">
        <div class="container">
          <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </a>
        <a class="brand" href="/">SynoDLNAtrakt</a>
        <div class="nav-collapse collapse">
          <ul class="nav">
            <li class="home"><a href="/">Home</a></li>
            <li class="dropdown series">
              <a href="/series" class="dropdown-toggle" data-toggle="dropdown">
                Series
                <b class="caret"></b> <span class="badge badge-inverse">{{seriescount}}</span>
              </a>
              <ul class="dropdown-menu">
                <li><a href="/series">A-Z</a></li>
                <li><a href="/series/lastseen">Lastseen</a></li>
                <li><a href="/series/unseen">Unseen</a></li>
                <li><a href="/series/lastadded">Lastadded</a></li>
                <li><a href="/series/unrated">Unrated</a></li>
              </ul>
            </li>
            <li class="dropdown movie">
              <a href="/movies" class="dropdown-toggle" data-toggle="dropdown">
                Movies 
                <b class="caret"></b> <span class="badge badge-inverse">{{moviecount}}</span>
              </a>
              <ul class="dropdown-menu">
                <li><a href="/movies">A-Z</a></li>
                <li><a href="/movies/lastseen">Lastseen</a></li>
                <li><a href="/movies/unseen">Unseen</a></li>
                <li><a href="/movies/lastadded">Lastadded</a></li>
                <li><a href="/movies/unrated">Unrated</a></li>
              </ul>
            </li>
            <li class="dropdown settings">
              <a href="/series" class="dropdown-toggle" data-toggle="dropdown">
                Settings
                <b class="caret"></b>
              </a>
              <ul class="dropdown-menu">
                <li><a href="/settings">General</a></li>
                <li><a href="/settings/force">Force</a></li>
              </ul>
            </li>
            <li class="dropdown logs">
              <a href="/logs" class="dropdown-toggle" data-toggle="dropdown">
                Logs
                <b class="caret"></b>
              </a>
              <ul class="dropdown-menu">
                <li><a href="/logs/INFO">INFO</a></li>
                <li><a href="/logs/ERROR">ERROR</a></li>
                <li><a href="/logs/WARNING">WARNING</a></li>
                <li><a href="/logs/DEBUG">DEBUG</a></li>
              </ul>
            </li>
              
          </ul>
          <form class="navbar-form pull-right" action="/search" method="POST">
            <select class="span1" name="searchfor">
              <option value="series">Series</option>
              <option value="episodes">Episodes</option>
              <option value="movies">Movies</option>
            </select>
            <input type="text" name="searchterm" placeholder="Search" class="span2">
            <button type="submit" class="btn">Submit</button>
          </form>
        </div>
      </div>
    </div>
  </header>
  %if config.commits_behind >= 1:
  <div id="update">
      <p class="alert alert-info">there is a <a href="http://github.com/cytec/SynoDLNAtrakt/compare/{{config.current_version}}...{{config.latest_version}}" target="_blank">newer version available</a> (you are <b>{{config.commits_behind}} commits behind</b>) - <a href="/settings/force/update">update now</a></p>
  </div>
  %end if
  <div id="back_to_top" style="border-radius: 10px; width: 40px; height: 40px; position:fixed; right: 40px; bottom:40px; background-color: #000; z-index: 10">
    <a href="#">back to top</a>
  </div>
  