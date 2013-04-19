%include incl_top title=title, topmenu=topmenu
%from synodlnatrakt import config, db
%from synodlnatrakt.timer import sched
%import datetime

%episodes = db.session.query(db.TVEpisodes)
%seriescount = db.session.query(db.TVShows).count()
%a = 100 * float(episodes.filter(db.TVEpisodes.scrobbled == 1).count())/float(episodes.count())
%movies = db.session.query(db.Movies)
%b = 100 * float(movies.filter(db.Movies.scrobbled ==1).count())/float(movies.count())


%episodes_watched = episodes.filter(db.TVEpisodes.scrobbled == 1).count()
%episodes_unwatched = int(episodes.count()) - int(episodes_watched)

  <div role="main">
	 <div class="container">
    <div class="row">
     <div class="span12">
        You have {{seriescount}} series with {{episodes.count()}} episodes <br />
        
        you watched {{episodes.filter(db.TVEpisodes.scrobbled == 1).count()}} Episodes which are {{a}}%<br />
        you have {{movies.count()}} movies<br />
        you watched {{movies.filter(db.Movies.scrobbled ==1).count()}} movies which are {{b}}%<br />
        you rated {{movies.filter(db.Movies.rating != 0).count()}} movies<br />

        %for x in sched._pending_jobs:
          {{sched._pending_jobs[x][0].name}} {{sched._pending_jobs[x][0].trigger.run_date}}
        %end for

        <div class="row statistics" style="text-align:center">
          <div class="span6">
            <h4>Episode Stats</h4>
            <div class="row">
              <div id="series" class="span6" style="min-height:400px">
              </div>
            </div>
          </div>

          <div class="span6">
          <h4>Most Episodes by show</h4>
          <div class="row">
              <div id="sseries" class="span6" style="min-height:400px">
              </div>
            </div>
        </div>


        <div class="row statistics" style="text-align:center">
          <div class="span6">
            <h4>Movie Stats</h4>
            <div class="row">
              <div id="movies" class="span6" style="min-height:400px">
              </div>
            </div>
          </div>

          <div class="span6">
          <h4>Movie Rating Stats</h4>
          <div class="row">
              <div id="rating" class="span6" style="min-height:400px">
              </div>
            </div>
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
  <script language="javascript" type="text/javascript" src="/static/js/jquery.flot.js"></script>
    <script language="javascript" type="text/javascript" src="/static/js/jquery.flot.pie.js"></script>

  <script type="text/javascript">

  
    $('button[type="submit"]').click( function(event) {
      event.preventDefault()
      args = $('#myForm').serialize()

      $.post("/save/config", args, function(data) {
        if (data["status"] == "success") {
          successNotification("Yeah...","settings saved")
        } else {
          errorNotification("Whooopsy...","something went wrong")
        }
      })

    })

    function clearForm(form) {
  // iterate over all of the inputs for the form
  // element that was passed in
  $(':input', form).each(function() {
    var type = this.type;
    var tag = this.tagName.toLowerCase(); // normalize case
    // it's ok to reset the value attr of text inputs,
    // password inputs, and textareas
    if (type == 'text' || type == 'password' || tag == 'textarea')
      this.value = "";
    // checkboxes and radios need to have their checked state cleared
    // but should *not* have their 'value' changed
    else if (type == 'checkbox' || type == 'radio')
      this.checked = false;
    // select elements need to have their 'selectedIndex' property set to -1
    // (this works for both single and multiple select elements)
    else if (tag == 'select')
      this.selectedIndex = -1;
  });
};

    $('button.cancel').click( function(){
      clearForm($(this).parent().parent())
    })

    var sdata = [
      { label: "watched",  data: {{episodes_watched}}, color: "#85bc26"},
      { label: "unseen",  data: {{episodes_unwatched}}, color: "#bc2626"},
    ];

    var mdata = [
      { label: "watched",  data: {{movies.filter(db.Movies.scrobbled ==1).count()}}, color: "#85bc26"},
      { label: "unseen",  data: {{movies.count()- movies.filter(db.Movies.scrobbled ==1).count()}}, color: "#bc2626"},
    ];

    var rdata = [
      { label: "10",  data: {{movies.filter(db.Movies.rating ==10).count()}}},
      { label: "9",  data: {{movies.filter(db.Movies.rating ==9).count()}}},
      { label: "8",  data: {{movies.filter(db.Movies.rating ==8).count()}}},
      { label: "7",  data: {{movies.filter(db.Movies.rating ==7).count()}}},
      { label: "6",  data: {{movies.filter(db.Movies.rating ==6).count()}}},
      { label: "5",  data: {{movies.filter(db.Movies.rating ==5).count()}}},
      { label: "4",  data: {{movies.filter(db.Movies.rating ==4).count()}}},
      { label: "3",  data: {{movies.filter(db.Movies.rating ==3).count()}}},
      { label: "2",  data: {{movies.filter(db.Movies.rating ==2).count()}}},
      { label: "1",  data: {{movies.filter(db.Movies.rating ==1).count()}}},
      { label: "unrated",  data: {{movies.filter(db.Movies.rating ==0).count()}}},
    ];

    var ssdata = [
      %a = db.session.query(db.TVShows).all()

      %for x in a:
        { label: "{{x.name}}", data:{{db.session.query(db.TVEpisodes).filter(db.TVEpisodes.show_id == x.tvdb_id).count()}}},
        %end for
    ];

    $.plot($("#series"), sdata,
    {
      series: {
          pie: { 
              innerRadius: 0.5,
              show: true
          }
      },
      legend: {
            show: false
      },
      grid: {
            hoverable: true,
      }

    });

    $.plot($("#sseries"), ssdata,
    {
      series: {
          pie: { 
              innerRadius: 0.5,
              show: true
          }
      },
      legend: {
            show: false
      },
      grid: {
            hoverable: true,
      }

    });

    $.plot($("#movies"), mdata,
    {
      series: {
          pie: { 
              innerRadius: 0.5,
              show: true
          }
      },
      legend: {
            show: false
      },
      grid: {
            hoverable: true,
      }

    });

    $.plot($("#rating"), rdata,
    {
      series: {
          pie: { 
              innerRadius: 0.5,
              show: true
          }
      },
      legend: {
            show: false
      },
      grid: {
            hoverable: true,
      }

    });


     


  </script>
  <!-- end scripts -->


</body>
</html>


	