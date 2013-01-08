%include incl_top title=title, topmenu=topmenu

%from synodlnatrakt import config

    <div class="row banner-top" style="background-image: url(/cache/fanart/{{show.tvdb_id}}.jpg)">
      <h1>{{show.name}}</h1>
    </div>
  <div role="main">
	<div class="container">
    <div class="row">
      <div class="span12">
        %curseason = -1
        %for entry in content:
        
        %if entry.season != curseason:
          
          %curseason = entry.season
          </table>
          <h1>Season {{entry.season}}</h1>
          <table class="table table-striped">
        <thead>
          <tr>
            <th class="span1">Episode</th>
            <th class="hidden-phone span4">Name</th>
            <th class="span1">Progress</th>
            <th class="hidden-phone span3">Seen</th>
            <th class="span1 center-text">seen</th>
            <th class="span1 center-text">stream</th>
            <th class="span1 center-text">delete</th>
          </tr>
        </thead>
        %end if
      
    

        <tr ep-name="{{entry.name}}" syno-id="{{entry.synoindex}}">
          <td class="episode">{{entry.episode}}</td>
          %if entry.is_anime and entry.abs_ep:
            <td class="name hidden-phone">{{entry.abs_ep}} : {{entry.name}}</td>
          %else:
            <td class="name hidden-phone">{{entry.name}}</td>
          %end if
          <td>
            <div class="progress">
              %if entry.progress > config.min_progress:
                <div class="bar bar-success" style="width: {{entry.progress}}%;">{{entry.progress}}%</div>
              %else:
                <div class="bar" style="width: {{entry.progress}}%;">{{entry.progress}}%</div>
              %end if
            </div>
          </td>
          <td class="date hidden-phone">{{entry.lastseen}}</td>
          <td class="scrobble center-text">
            %if entry.scrobbled == 1:
              <i class="icon-eye-open"></i>
            %else:
              <i class="icon-eye-close"></i>
            %end if

          </td>
          <td class="stream center-text" href="/stream"><i class="icon-play"></i></td>
          <td class="delete center-text"><i class="icon-remove"></i></td>         
        </tr>
    
      
      %end for
    </div>
  </div>

  </div>
  </div>
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
  <script src="/static/js/shadowbox.js"></script>  
  <script type="text/javascript">

    Shadowbox.init({
    // let's skip the automatic setup because we don't have any
    // properly configured link elements on the page
    skipSetup: true
});

    $('.scrobble').click(function(){
      epname = $(this).parent().attr("ep-name")

      args = {
        'type' : 'series',
        'synoindex': $(this).parent().attr("syno-id")
      }    

      el = $(this)
      $.post("/scrobble", args, function(data){
        if (data["status"] == "success") {
          addNotification("success","Successfully", "marked \""+epname+"\" as seen")
          el.parent().find('.bar').addClass('bar-success').animate({"width":"100%"}).text("100%")
        } else {
          addNotification("error","Whooooopsy...", "There was an Error marking \""+epname+"\" as seen")
        }
      });
    });

    $('.delete').click(function(){
      epname = $(this).parent().attr("ep-name")
      tohide = $(this).parent()

      args = {
        'type' : 'series',
        'synoindex': $(this).parent().attr("syno-id")
      }

     $.post("/delete", args, function(data){
        if (data["status"] == "success") {
           addNotification("success","Successfully", "deleted \""+epname+"\" from Database")
           tohide.fadeOut()
        } else {
          addNotification("error", "Whooooopsy...", "There was an Error deleteing \""+epname+"\" from Database")
        }
        console.log(data)
     });
    });

     function runDivx() {
      plugin = document.getElementById('divx');
      if (plugin){
        plugin.Open(window.location.origin+plugin.attributes.src.textContent);
      }
    }
    $('.stream').click(function(){
      epname = $(this).parent().attr("ep-name")
      tohide = $(this).parent()

      args = {
        'type' : 'series',
        'synoindex': $(this).parent().attr("syno-id")
      }

     $.post("/stream", args, function(data){
        Shadowbox.open({
          content:    data,
          player:     "html",
          title:      epname,
          height:     580,
          width:      740,
          options : { onFinish : runDivx } 
        });
     });
    });


  </script>
  <!-- end scripts -->


</body>
</html>


	