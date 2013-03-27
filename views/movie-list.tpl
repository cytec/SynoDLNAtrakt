%include incl_top title=title, topmenu=topmenu

%from synodlnatrakt import config



  <div role="main">
	<div class="container movie-list">


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



    <div class="row movie-single-view {{addclass}}">
      %if " - " in title:
        %mybase = "/movies/{0}/page/".format(title.split(' - ')[1])
      %else:
        %mybase = "/movies/page/"
      %end if

  <div class="span12" style="background: url(/cache/fanart/{{entry.imdb_id}}.jpg)">
    <a class="media-element" href="/movies/view/{{entry.synoindex}}">
      <h1>{{entry.name}} <br /> {{entry.year}}</h1>
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
%if pagination:
  <div class="row" id="pagination" style="text-align: center; color:#444!important">
  %if pagination.has_prev:
      <a class="prev" style="text-align: center; color:#444!important" href="{{mybase}}{{pagination.page - 1}}">&laquo; Previous</a>
  %end if

  %for page in pagination.iter_pages():
    %if page:
      %if page != pagination.page:
        <a style="text-align: center; color:#444!important" href="{{mybase}}{{page}}">{{ page }}</a>
      %else:
        <strong>{{ page }}</strong>
      %end if
    %else:
      <span class="ellipsis">…</span>
    %end if
  %end for

  %if pagination.has_next:
      <a class="next" style="text-align: center; color:#444!important" href="{{mybase}}{{pagination.page + 1}}">Next &raquo;</a>
  %end if
  </div>
%end if
	</div>
  </div>
  <footer>

  </footer>


  <!-- JavaScript at the bottom for fast page loading -->

  <!-- Grab Google CDN's jQuery, with a protocol relative URL; fall back to local if offline -->


  <!-- scripts concatenated and minified via build script -->
  <script src="/static/js/bootstrap.min.js"></script>
  <script src="/static/js/plugins.js"></script>
  <script src="/static/js/script.js"></script>
  <script type="text/javascript" src="/static/js/jquery.ias.min.js"></script>
  <script type="text/javascript">
  $("a[data-toggle=dafuq]").click(function(event) {
event.preventDefault()
  var target = $(this).attr('data-target');
console.log(target)

  var url = $(this).attr('href');
  $(target).load(url)
$(target).modal('show')
})

  $("#myModal").modal('hide')

jQuery.ias({
  container : '.movie-list',
  item: '.movie-single-view',
  pagination: '#pagination',
  next: '.next',
  loader: '<img src="/static/img/loader.gif"/>',
  tresholdMargin: -600
});

  </script>
  <!-- end scripts -->


</body>
</html>



