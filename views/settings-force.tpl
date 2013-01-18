%include incl_top title=title, topmenu=topmenu
%from synodlnatrakt import config
  

   
  <div role="main">
	<div class="container">
    <div class="row">
      <div class="span12">
        <div class="span6 offset3">
          <div class="well">
            <p><i class="btn btn-inverse icon-wrench"> Toggle Advanced Settings</i></p>

          <p><button id="sync" class="btn btn-large btn-block" type="button">Force trakt.tv sync</button></p>
          <p><button id="scrobble" class="btn btn-large btn-block" type="button">Force Scrobble</button></p>
          <div class="advanced" style="display:none">
            <form>
              <fieldset>
                <legend>Advanced Import settings</legend>
                <label>Process Folder</label>
                <select name="folder">
                  <option value=""></option>
                  %for folder in config.moviedir:
                     <option value="{{folder}}">{{folder}}</option>
                  %end for
                  %for folder in config.seriesdir:
                     <option value="{{folder}}">{{folder}}</option>
                  %end for
                </select>
                <span class="help-block">enter folder path to process here..</span>
                <label>Entrys</label>
                <input type="text" name="max_entrys" placeholder="20">
                <span class="help-block">load the last x entrys (enter 0 for all)</span>
                <label class="radio">
                  <input type="radio" name="mediatype" id="mediatype2" value="series" >
                  Process all Series Folders
                </label>
                <label class="radio">
                  <input type="radio" name="mediatype" id="mediatype2" value="movies">
                  Process all Movie Folders
                </label>
              </fieldset>
            </form>
          </div>
          <p><button id="import" class="btn btn-large btn-block" type="button">Force Import</button></p>
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

    $('button').click(function(){
      btn = $(this)
      btnid = $(this).attr('id')

      if ($(this).hasClass("use-advanced")) {
        args = $('form').serialize()
        console.log(args)
      } else {
        args = {}
      }

      what = $(this).text()
      url = "/settings/force/" + btnid
      //show this notification only for 1 sec...
      showNotification("Running", what + " please whait",1000)
      $.post(url, args, function(data){
        console.log(data)
        if (data["status"] == "success") {
          //successNotification("Success", data["message"])
          addNotification("message", "Yeah", data["message"])
        } else {
          addNotification("error", "Whooooopsy...", "Something went wrong...")
        }
        console.log(data)
      })
    })


    $('.icon-wrench').click(function(){
      $('.advanced').slideToggle()
      $('#import').toggleClass('use-advanced')
    })


  </script>
  <!-- end scripts -->


</body>
</html>


	