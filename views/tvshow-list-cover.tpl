%include incl_top title=title, topmenu=topmenu

  <div role="main">
	<div class="container movie-list">
    %counter = 0
    %for entry in content:
    %if counter == 0:
      <div class="row movie" >
    %end if
      
    %counter = counter + 1


  
  <div class="span2">
    <img src="/cache/cover/{{entry.tvdb_id}}.jpg" />

  </div>
  %if counter == 6:
    %counter = 0
  %end if
  %if counter == 0:
      </div>
  %end if
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
  <script src="/static/js/script.js"></script>  
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
  </script>
  <!-- end scripts -->


</body>
</html>


	