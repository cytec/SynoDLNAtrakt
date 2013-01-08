%include incl_top title=title, topmenu=topmenu

    <div class="row banner-top" style="background-image: url(/cache/fanart/{{movie.imdb_id}}.jpg)">
      <h1>{{movie.name}}</h1>
    </div>
  <div role="main">
	<div class="movie container" synoindex="{{movie.synoindex}}">
    <div class="row">
      <div class="span12">
        <ul class="unstyled pull-right inline">
          <li class="stream"><i class="icon-play"></i></li>
          <li class="scrobble"><i class="icon-eye-open"></i></li>
          <li class="delete"><i class="icon-remove"></i></li>
          <li class="edit"><i class="icon-pencil"></i></li>
        </ul>
        
      </div>
      <div class="span12" style="display: none;" id="edit">
        <b>Synoindex:</b> {{movie.synoindex}}<br />
        <b>Path:</b> {{movie.path}}<br />
        <b>IMDB:</b> {{movie.imdb_id}}<br />
        <b>Duration:</b> {{movie.duration}}<br />
        <b>added:</b> {{movie.added}}<br />
        <b>lastseen:</b> {{movie.lastseen}}<br />
        <b>progress:</b> {{movie.progress}}%<br />
        <b>scrobbled:</b> {{movie.scrobbled}}<br />
        <b>rating:</b> {{movie.rating}}/10<br />
        <b>synoindex id:</b> {{movie.synoindex}}<br />
        <form id="addShowForm">
          <fieldset>
            <legend>Edit</legend>
            <label>Movie Name</label>
            <input type="text" id="nameToSearch" name="name" placeholder="Search TMDB" value="{{movie.name}}">
            <span class="help-block">Enter a new Movie name to search on tmdb</span>
            <input type="button" id="searchName" value="Search" class="btn"></input>
          </fieldset>

            <div id="searchResults">
            </div>
            <button type="button" id="submit" value="Submit" class="btn btn-success hidden">Submit</button>
         
        </form>
      </div>
    </div>
    <div class="row">
      <div class="span3 hidden-phone">
        <img src="/cache/cover/{{movie.imdb_id}}.jpg" />
      </div>
      <div class="span9">
        <div id="star" class="pull-right"></div>
        <h1 class="hidden-phone">{{movie.name}} ({{movie.year}})</h1>
        <p>{{movie.description}}</p>

        
    </div>
    <div class="span12">
      

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
  <script src="/static/js/jquery.raty.min.js"></script>   
  <script src="/static/js/notification.js"></script>
    <script src="/static/js/shadowbox.js"></script>  
  <script src="/static/js/script.js"></script>  
  <script type="text/javascript">

  Shadowbox.init({
    // let's skip the automatic setup because we don't have any
    // properly configured link elements on the page
    skipSetup: true
});
    $('.edit').click(function(){
      $('#edit').slideToggle()
    })

    function runDivx() {
      plugin = document.getElementById('divx');
      if (plugin){
        plugin.Open(window.location.origin+plugin.attributes.src.textContent);
      }
    }
    $('.stream').click(function(){
      

      args = {
        'type' : 'movie',
        'synoindex': {{movie.synoindex}}
      }

     $.post("/stream", args, function(data){
        //$('footer').html(data)
        Shadowbox.open({
          content:    data,
          player:     "html",
          title:      "{{movie.name}}",
          height:     580,
          width:      740,
          options : { onFinish : runDivx } 
        });

     // WinId = window.open('', 'newwin');
     //        WinId.document.open();
     //        WinId.document.write(data);
     //        WinId.document.close();
     });
    });

    $('.scrobble').click(function(){
      args = {
        'type' : 'movie',
        'path': '{{movie.path}}',
        'synoindex': '{{movie.synoindex}}'
      }

     $.post("/scrobble", args, function(data){
        if (data["status"] == "success") {
          addNotification("success","Successfully","marked \"{{movie.name}}\" as seen")
        } else {
          errorNotification("Oh Noes!", "There was an Error marking \"{{movie.name}}\" as seen")
        }
     });
    });

    $('.delete').click(function(){
      args = {
        'type' : 'movie',
        'path': '{{movie.path}}',
        'synoindex': '{{movie.synoindex}}'
      }

     $.post("/delete", args, function(data){
        if (data["status"] == "success") {

           successNotification("Successfully", "deleted \"{{movie.name}}\" from Database")
        } else {
          errorNotification("Oh Noes!", "There was an Error deleteing \"{{movie.name}}\" from Database")
        }
        console.log(data)
     });
    });

    $('#searchName').click(function(){
      var searchstring = $('#nameToSearch').val()
      searchstring = encodeURI(searchstring)
      //$('#searchResults').append('<fieldset>\n<legend>Search Results:</legend>\n');
      htmlstring = '<fieldset>\n<legend>Search Results:</legend>\n'
      $.post('/update/movie', {'name':searchstring}, function(data){
        //console.log(data.length)
        for (var i = 0; i < data.length; i++) { 
          //alert(data[i].name);

          html = '<label class="radio"><input type="radio" name="new_id" value="'+data[i].imdb_id+'" ><a href="'+data[i].url+'" target="_blank">'+data[i].name + ' ('+ data[i].released+')</a></label>'

          htmlstring += html
        }
        htmlstring += '</fieldset>\n'
      $('#searchResults').html(htmlstring)
      $('#submit').removeClass("hidden")
      }, "json")

    })

    $('#submit').click(function(){
      var imdb_id = $("input[name='new_id']:checked").val()
      var synoindex = '{{movie.synoindex}}'

      args = {
        'synoindex': synoindex,
        'imdb_id': imdb_id
      }

      $.post('/save/movie', args, function(data){
        if (data["status"] == "success") {
          successNotification(data["title"], data["message"])
        }
      })
    })

    function updateRating(score){
      //alert(score)
      if (score == null) {
        score = 0
      }
      synoindex = "{{movie.synoindex}}"

      args = {
        'type': 'movie',
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
          addNotification("success", "{{movie.name}}", "was reated: \"" +scorevals[score]+"\"")
        } else {
          addNotification("error", "Unable", "to update rating for \"{{movie.name}}\"")
        }
      });    

    }

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
    score: {{movie.rating}},
    click: function(score, evt) {
      updateRating(score);
    }
  })

  </script>
  <!-- end scripts -->


</body>
</html>


	