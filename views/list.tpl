%include incl_top title=title, topmenu=topmenu

%from synodlnatrakt import config
%from synodlnatrakt import db


  <div role="main">
  <div class="container series-list">
    %for entry in content:
%addclass = ""

%if entry.scrobbled and config.hide_watched:
  %addclass = "hidden"
%elif entry.scrobbled:
  %addclass = "seen"
%end if

%if "lastseen" in title:
  %addclass = ""
%end if
    <div class="row {{addclass}}">

      %showname = db.session.query(db.TVShows).filter(db.TVShows.tvdb_id == entry.show_id).first()
      <div class="span12" style="background-image: url(/cache/fanart/{{entry.show_id}}.jpg)">
        <a href="/series/view/{{entry.show_id}}" class="media-element">
          <h1>{{showname.name}}</h1>
          <h2>{{entry.season}}x{{entry.episode}} {{entry.name}}</h2>
          %if config.mediaflags:
          <div class="codec span11">
            <!-- {{entry.vcodec}}  {{entry.acodec}} {{entry.vwidth}} -->

            %if entry.vcodec and entry.vcodec.lower() in config.CODEC_MAP.keys():
              <img src="/static/img/flags/videocodec/{{config.CODEC_MAP[entry.vcodec.lower()]}}.png" />
            %else:
              <img src="/static/img/flags/videocodec/default.png" />
            %end if

            %if entry.acodec and entry.acodec.lower() in config.CODEC_MAP.keys():
              <img src="/static/img/flags/audio/{{config.CODEC_MAP[entry.acodec.lower()]}}.png" />
            %else:
              <img src="/static/img/flags/audio/defaultsound.png" />
            %end if

            %if entry.vwidth < 768:
              <img src="/static/img/flags/resolution/480.png" />
            %elif entry.vwidth >= 768 and entry.vwidth < 1280:
              <img src="/static/img/flags/resolution/576.png" />
            %elif entry.vwidth >= 1280 and entry.vwidth < 1920:
              <img src="/static/img/flags/resolution/720.png" />
            %elif entry.vwidth >= 1920:
              <img src="/static/img/flags/resolution/1080.png" />
            %end if
          </div>
          %end if
        </a>
      </div>
    </div>
%end for
  </div>
  </div>
  <footer>

  </footer>


  <!-- JavaScript at the bottom for fast page loading -->

  <!-- Grab Google CDN's jQuery, with a protocol relative URL; fall back to local if offline -->
  <script src="/static/js/libs/jquery-1.8.1.min.js"></script>

  <!-- scripts concatenated and minified via build script -->
  <script src="/static/js/bootstrap.min.js"></script>
  <script src="/static/js/plugins.js"></script>
  <script type="text/javascript" src="/static/js/notifier.js"></script>
  <script src="/static/js/script.js"></script>
  <script type="text/javascript">

  </script>
  <!-- end scripts -->

</body>
</html>



