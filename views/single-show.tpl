%include incl_top title=title, topmenu=topmenu

%from synodlnatrakt import config

    <div class="row banner-top" style="background-image: url(/cache/fanart/{{show.tvdb_id}}.jpg)">
      <h1>{{show.name}}</h1>
    </div>
  <div role="main">
	<div class="container">
    <div class="row">
      <div class="span12">
        <ul class="unstyled pull-right inline">
          <li class="edit"><i class="icon-pencil"></i></li>
        </ul>
        
      </div>
      <div class="span12" style="display: none;" id="edit">
        <b>Name:</b> {{show.name}}<br />
        <b>TVDBID:</b> {{show.tvdb_id}}<br />
        <b>Location:</b> {{show.location}}<br />
        <b>Anime:</b> {{bool(show.is_anime)}}<br />
        <!-- <form id="addShowForm">
          <fieldset>
            <legend>Edit</legend>
            <label>Series Name</label>
            <input type="text" id="nameToSearch" name="name" placeholder="Search TVDB" value="{{show.name}}">
            <span class="help-block">Enter a new Series name to search on tvdb</span>
            <input type="button" id="searchName" value="Search" class="btn"></input>
          </fieldset>

            <div id="searchResults">
            </div>
            <button type="button" id="submit" value="Submit" class="btn btn-success hidden">Submit</button>
         
        </form> -->
      </div>
    </div>
    <div class="row">
      <div id="star" class="pull-right">asdas</div>
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
      
    

        <tr season="{{entry.season}}" episode="{{entry.episode}}" ep-name="{{entry.name}}" syno-id="{{entry.synoindex}}" rating="{{entry.rating}}" rel="popover" data-placement="top" data-content="{{entry.description}}" data-original-title="{{entry.name}}" data-trigger="hover">
          <td class="episode">{{entry.episode}}</td>
          %if entry.is_anime and entry.abs_ep:
            <td class="name hidden-phone" rel="popover" data-placement="top" data-content="{{entry.description}}" data-original-title="{{entry.name}}">{{entry.abs_ep}} : {{entry.name}}</td>
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
    <script src="/static/js/jquery.raty.min.js"></script>   

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

    $('tr').hover(function(){
      $(this).popover("toggle")
    })

    $('.edit').click(function(){
      $('#edit').slideToggle()
    })

    var synoindex
    var element
    var season
    var episode

    $('tr').click(function(){
      console.log($(this).attr("syno-id"))
      synoindex = $(this).attr("syno-id")
      showPopover($(this).attr("rating"))
      element = $(this)
      season = $(this).attr("season")
      episode = $(this).attr("episode")
    })

    //implement episode rating here!
    function updateRating(score){
      //alert(score)
      if (score == null) {
        score = 0
      }

      args = {
        'type': 'series',
        'synoindex': synoindex,
        'score': score
      }

      scorevals = {
        0: "no rating",
        1: "weak sause :(",
        2: "Terrible",
        3: "Bad",
        4: "Poor",
        5: "Meh",
        6: "Fair",
        7: "Good",
        8: "Great",
        9: "Superb",
        10: "Totally Ninja!"
      }

      $.post("/rate", args, function(data){
        console.log(data)
        if (data["status"] == "success") {
          addNotification("success", "{{show.name}}", season+"x"+episode+" reated: \"" +scorevals[score]+"\"")
          element.attr("rating", score)
        } else {
          addNotification("error", "Unable", "to update rating")
        }
      });    

    }


    function showPopover(myscore) {
      $('#star').raty({
        cancel: true,
        size: 30,
        number: 10,
        path: "/static/img/",
        starOn  : 'star-on-big.png',
        starOff  : 'star-off-big.png',
        cancelOff : 'cancel-off-big.png',
        cancelOn  : 'cancel-on-big.png',
        hints: ["weak sauce :(","Terrible","Bad","Poor","Meh","Fair","Good","Great","Superb","Totally Ninja!"],
        score: myscore,
        click: function(score, evt) {
          updateRating(score);
        }
      })
    }
    

  </script>
  <!-- end scripts -->


</body>
</html>


	