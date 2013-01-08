%include incl_top title=title, topmenu=topmenu

%from synodlnatrakt import config
  <div role="main">
	<div class="container movie-list">

<div class="btn-group" id="filter">
  <button class="btn">Name</button>
  <button class="btn">Rating</button>
  <button class="btn">Year</button>
</div>
    <div class="row">
      <ul id="movies" class="unstyled" style="padding: 0; margin: 0">
        %counter = 0
    %for entry in content:
    %counter = counter +1
%addclass = ""

%if entry.scrobbled and config.hide_watched: 
  %addclass = "hidden"
%elif entry.scrobbled:
  %addclass = "seen"
%end if

%if "lastseen" in title:
  %addclass = ""
%end if
  
    

      
         <li class="span2" style="height: 270px;" data-id="{{counter}}" data-type="movie" data-rating="{{entry.rating}}" data-name="{{entry.name}}" data-year="{{entry.year}}">
          <a class="media-element" style="padding:0" href="/movies/view/{{entry.synoindex}}">
            <img src="/cache/cover/{{entry.imdb_id}}.jpg" height="100%"/>
          </a>
        </li>
      
  
 
%end for
</ul>
</div>
	</div>
  </div>
  <footer>

  </footer>


  <!-- JavaScript at the bottom for fast page loading -->

  <!-- Grab Google CDN's jQuery, with a protocol relative URL; fall back to local if offline -->
  

  <!-- scripts concatenated and minified via build script -->
  <script src="/static/js/bootstrap.min.js"></script>
   <script src="/static/js/jquery.easing.js"></script>
  <script src="/static/js/plugins.js"></script>
  <script src="/static/js/script.js"></script>  
  <script type="text/javascript">
// Custom sorting plugin
(function($) {
  $.fn.sorted = function(customOptions) {
    var options = {
      reversed: false,
      by: function(a) { return a.text(); }
    };
    $.extend(options, customOptions);
    $data = $(this);
    arr = $data.get();
    arr.sort(function(a, b) {
      var valA = options.by($(a));
      var valB = options.by($(b));
      if (options.reversed) {
        return (valA < valB) ? 1 : (valA > valB) ? -1 : 0;        
      } else {    
        return (valA < valB) ? -1 : (valA > valB) ? 1 : 0;  
      }
    });
    return $(arr);
  };
})(jQuery);

// DOMContentLoaded
$(function() {

  // bind radiobuttons in the form
  var $filterType = $('#filter input[name="type"]');
  var $filterSort = $('#filter input[name="sort"]');

  // get the first collection
  var $applications = $('#movies');

  // clone applications to get a second collection
  var $data = $applications.clone();

  var $filteredData = $data.find('li');


  $('#filter button').click(function(){
    var $sortBy = $(this).text().toLowerCase()



    if ($sortBy == "rating") {
      var $sortedData = $filteredData.sorted({
        by: function(v) {
          //console.log($(v).attr("data-rating"))
          return parseFloat(($(v).attr("data-rating")));
        }, reversed: true,
      });
    }

    if ($sortBy == "name") {
      var $sortedData = $filteredData.sorted({
        by: function(v) {
          //console.log($(v).attr("data-rating"))
          return ($(v).attr("data-name").toLowerCase());
        }
      });
    }

    if ($sortBy == "year") {
      var $sortedData = $filteredData.sorted({
        by: function(v) {
          //console.log($(v).attr("data-rating"))
          return parseFloat(($(v).attr("data-year")));
        }, reversed: true,
      });
    }

    $applications.quicksand($sortedData, {
      duration: 800,
      easing: 'easeInOutQuad'
    });

  })



  // $filterType.add($filterSort).change(function(e) {
  //   // if ($($filterType+':checked').val() == 'all') {
  //   //   var $filteredData = $data.find('li');
  //   // } else {
  //   //   var $filteredData = $data.find('li[data-type=' + $($filterType+":checked").val() + ']');
  //   // }
    

  //   // if sorted by size
  //   if ($('#filter input[name="sort"]:checked').val() == "size") {
  //     var $sortedData = $filteredData.sorted({
  //       by: function(v) {
  //         //console.log($(v).attr("data-rating"))
  //         return parseFloat(($(v).attr("data-rating")));
  //       }, reversed: true,
  //     });
  //   } else {
  //     // if sorted by name
  //     var $sortedData = $filteredData.sorted({
  //       by: function(v) {
  //         //console.log($(v).attr("data-name").toLowerCase())
  //         return $(v).attr("data-name").toLowerCase();
  //       }
  //     });
  //   }   

  //   //console.log($sortedData)
  //   // finally, call quicksand
  //   $applications.quicksand($sortedData, {
  //     duration: 800,
  //     easing: 'easeInOutQuad'
  //   });

  // });

});
  </script>
  <!-- end scripts -->


</body>
</html>


	