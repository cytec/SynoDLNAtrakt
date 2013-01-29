%include incl_top title=title, topmenu=topmenu
%from synodlnatrakt import config
     
  <div role="main">
	<div class="container">
    <div class="row">
      <div class="span12">
        
        <form id="myForm" method="POST" class="form-horizontal well" >
          <div class="page-header">
            <h1>Settings <small>Adjust your settings for SynoDLNAtrakt</small></h1>
            <div class="alert alert-info">
              <strong>Attention!</strong> Some changes may require a restart to work.
            </div>
          </div>

          <div class="tabbable tabs-left">
            <ul class="nav nav-tabs">
              <li class="active"><a href="#basic" data-toggle="tab">Basic</a></li>
              <li><a href="#webserver" data-toggle="tab">Webserver</a></li>
              <li><a href="#advanced" data-toggle="tab">Advanced</a></li>
            </ul>
            <div class="tab-content">

              <div class="tab-pane active" id="basic">
                <fieldset>
                  <legend>Basic Config</legend>
      
                  <div class="control-group">
                    <label class="control-label" for="moviedir">Movie directorys</label>
                    <div class="controls">
                      <input type="text" class="span8" id="moviedir" name="moviedir" placeholder="{{','.join(config.moviedir)}}">
                      <span class="help-block">Absoulte path to your main movies dir (seperated by ",")</span>
                    </div>
                  </div>

                  <div class="control-group">
                    <label class="control-label" for="seriesdir">Series directorys</label>
                    <div class="controls">
                      <input type="text" class="span8" id="seriesdir" name="seriesdir" placeholder="{{','.join(config.seriesdir)}}">
                      <span class="help-block">Absoulte path to your main series dir (seperated by ",")</span>
                    </div>
                  </div>

                  <div class="control-group">
                    <label class="control-label" for="trakt_user">Trakt.tv username</label>
                    <div class="controls">
                      <input type="text" id="trakt_user" name="trakt_user" placeholder="{{config.trakt_user}}">
                      <span class="help-block">your trakt.tv username</span>
                    </div>
                  </div>

                  <div class="control-group">
                    <label class="control-label" for="trakt_pass">Trakt.tv password</label>
                    <div class="controls">
                      <input type="password" id="trakt_pass" name="trakt_pass" placeholder="{{config.trakt_pass}}">
                      <span class="help-block">your trakt.tv password</span>
                    </div>
                  </div>

                  <div class="control-group">
                    <label class="control-label" for="min_progress">Minimal Progress</label>
                    <div class="controls">
                      <input type="text" id="min_progress" name="min_progress" placeholder="{{config.min_progress}}">
                      <span class="help-block">Minimal progress that must be watched before scrobbeling to trakt</span>
                    </div>
                  </div>
                   
                  <div class="form-actions">
                    <button type="submit" class="btn btn-primary">Save changes</button>
                    <button type="button" class="btn cancel">Cancel</button>
                  </div>
                </fieldset>
              </div>



              <div class="tab-pane" id="webserver">
                <fieldset>
                  <legend>Webserver Config <small>This Settings require a restart</small></legend>
      
                  <div class="control-group">
                    <label class="control-label" for="port">Port</label>
                    <div class="controls">
                      <input type="text" id="port" name="port" placeholder="{{config.port}}">
                      <span class="help-block">Port on which the webserver listens for incomeinc connections</span>
                    </div>
                  </div>

                  <div class="control-group">
                    <label class="control-label" for="username">Username</label>
                    <div class="controls">
                      <input type="text" id="username" name="username" placeholder="{{config.username}}">
                      <span class="help-block">The name you want to use to protect the webinterface</span>
                    </div>
                  </div>

                  <div class="control-group">
                    <label class="control-label" for="password">Password</label>
                    <div class="controls">
                      <input type="password" id="password" name="password" placeholder="{{config.password}}">
                      <span class="help-block">The password you want to use to protect the webinterface</span>
                    </div>
                  </div>

                  <div class="control-group">
                    <div class="controls">
                      <label class="checkbox">
                        %if config.hide_watched:
                          <input name="hide_watched" type="checkbox" checked> Hide watched episodes
                        %else:
                          <input name="hide_watched" type="checkbox"> Hide watched episodes
                        %end if
                        <span class="help-block">hide watched episodes instead of showing a "watched" overlay</span>
                      </label>
                    </div>
                  </div>

                  
           
                  <div class="form-actions">
                    <button type="submit" class="btn btn-primary">Save changes</button>
                    <button type="button" class="btn cancel">Cancel</button>
                  </div>
                </fieldset>
              </div>



              <div class="tab-pane" id="advanced">

                <fieldset>
                  <legend>Advanced Config</legend>
      
                  <div class="control-group">
                    <label class="control-label" for="language">Language</label>
                    <div class="controls">
                      <input type="text" id="language" name="language" placeholder="{{config.language}}">
                      <span class="help-block">ISO language code for tvdb and tmdb api requests</span>
                    </div>
                  </div>

                  <div class="control-group">
                    <label class="control-label" for="interval">Scan Intervall</label>
                    <div class="controls">
                      <input type="text" id="interval" name="interval" placeholder="{{config.interval}}">
                      <span class="help-block">Interval to run the scan for played media in minutes</span>
                    </div>
                  </div>

                  <div class="control-group">
                    <label class="control-label" for="page_limit">Entrys per page</label>
                    <div class="controls">
                      <input type="text" id="page_limit" name="page_limit" placeholder="{{config.page_limit}}">
                      <span class="help-block">how many items should be shown per page</span>
                    </div>
                  </div>
      
                  <div class="control-group">
                    <div class="controls">
                      <label class="checkbox">
                        %if config.try_guessing:
                          <input name="try_guessing" type="checkbox" checked> Try Guessing
                        %else:
                          <input name="try_guessing" type="checkbox"> Try Guessing
                        %end if
                        <span class="help-block">try to guess infos from filename if no nfo file is found</span>
                      </label>
                    </div>
                  </div>

                  <div class="control-group">
                    <div class="controls">
                      <label class="checkbox">
                        %if config.delete_logs:
                          <input name="delete_logs" type="checkbox" checked> delete logs
                        %else:
                          <input name="delete_logs" type="checkbox"> delete logs
                        %end if
                        <span class="help-block">deleting logfiles after scrobbled the found results to trakt</span>
                      </label>
                    </div>
                  </div>

                  <div class="control-group">
                    <div class="controls">
                      <label class="checkbox">
                        %if config.absolute_ep_anime:
                          <input name="absolute_ep_anime" type="checkbox" checked> Use absolute EP for Animes
                        %else:
                          <input name="absolute_ep_anime" type="checkbox"> Use absolute EP for Animes
                        %end if
                        <span class="help-block">use absolte episode numbers for animes</span>
                      </label>
                    </div>
                  </div>

                  <div class="control-group">
                    <div class="controls">
                      <label class="checkbox">
                        %if config.logtoconsole:
                          <input name="logtoconsole" type="checkbox" checked> log to console
                        %else:
                          <input name="logtoconsole" type="checkbox"> log to console
                        %end if
                        <span class="help-block">print the output to console, too (for debbuging)</span>
                      </label>
                    </div>
                  </div>

                  <div class="control-group">
                    <div class="controls">
                      <label class="checkbox">
                        %if config.debugmode:
                          <input name="debugmode" type="checkbox" checked> Debugmode
                        %else:
                          <input name="debugmode" type="checkbox"> Debugmode
                        %end if
                        <span class="help-block">activate debug mode logging</span>
                      </label>
                    </div>
                  </div>

                  <div class="control-group">
                    <div class="controls">
                      <label class="checkbox">
                        %if config.watched_flags:
                          <input name="watched_flags" type="checkbox" checked> Watched Flags
                        %else:
                          <input name="watched_flags" type="checkbox"> Watched Flags
                        %end if
                        <span class="help-block">Watched Flags for YAMJ/Popcorn Hour</span>
                      </label>
                    </div>
                  </div>

                  <div class="control-group">
                    <div class="controls">
                      <label class="checkbox">
                        %if config.add_to_list:
                          <input id="add_to_list" name="add_to_list" type="checkbox" checked> Add Movies to trakt.tv list
                        %else:
                          <input id="add_to_list" name="add_to_list" type="checkbox"> Add Movies to trakt.tv list
                        %end if
                        <span class="help-block">Add Movies to trakt.tv list on import</span>
                      </label>
                    </div>
                  </div>

                  %if config.add_to_list:
                  <div id="list_name" class="control-group">
                  %else:
                  <div id="list_name" class="control-group hidden">
                  %end if
                    <label class="control-label" for="list_name">List Name</label>
                    <div class="controls">
                      <input type="text" id="list_name" name="list_name" placeholder="{{config.list_name}}">
                      <span class="help-block">Name of the List you want to add the movies to (default: watchlist)</span>
                    </div>
                  </div>
                  

                  <div class="form-actions">
                    <button type="submit" class="btn btn-primary">Save changes</button>
                    <button type="button" class="btn cancel">Cancel</button>
                  </div>
                </fieldset>
              </div>
            </div>
          </div>

          
          

         
        </form>
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

  
    $('button[type="submit"]').click( function(event) {
      event.preventDefault()
      args = $('#myForm').serialize()

      $.post("/save/config", args, function(data) {})

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

    $('#add_to_list').click( function(){
      $('#list_name').toggleClass("hidden")
    })

  </script>
  <!-- end scripts -->


</body>
</html>


	