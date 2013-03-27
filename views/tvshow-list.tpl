%include incl_top title=title, topmenu=topmenu

  <div role="main">
  <div class="container series-list">
    %for entry in content:
    <div class="row">



  <div class="span12" style="background-image: url(/cache/fanart/{{entry.tvdb_id}}.jpg)">
    <a class="media-element" href="/series/view/{{entry.tvdb_id}}">
      <h1>{{entry.name}}</h1>
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



