<!doctype html>
<!-- paulirish.com/2008/conditional-stylesheets-vs-css-hacks-answer-neither/ -->
<!--[if lt IE 7]> <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang="de"> <![endif]-->
<!--[if IE 7]>    <html class="no-js lt-ie9 lt-ie8" lang="de"> <![endif]-->
<!--[if IE 8]>    <html class="no-js lt-ie9" lang="de"> <![endif]-->
<!-- Consider adding a manifest.appcache: h5bp.com/d/Offline -->
<!--[if gt IE 8]><!--> <html class="no-js" lang="de"> <!--<![endif]-->
<head>
  <meta charset="utf-8">

  <!-- Use the .htaccess and remove these lines to avoid edge case issues.
       More info: h5bp.com/i/378 -->
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

  <title></title>
  <meta name="description" content="">

  <!-- Mobile viewport optimized: h5bp.com/viewport -->
  <meta name="viewport" content="width=device-width">

  <!-- Place favicon.ico and apple-touch-icon.png in the root directory: mathiasbynens.be/notes/touch-icons -->
  <link rel="stylesheet" href="/static/css/bootstrap.min.css">
  <link rel="stylesheet" href="/static/css/bootstrap-responsive.min.css">
  <link rel="stylesheet" href="/static/css/style.css">

  %import os
  %html5video = ["mp4","m4v","mov"]
  %videoext = os.path.splitext(path)[1].replace(".","")

</head>
<body>
<div id="streamwrapper" style="width: 640px; margin: auto">

  %if videoext in html5video:
    <a href="/watch/{{path}}">IPHONE VIDEO</a>
    <video id="my_video_1" class="video-js vjs-default-skin" controls autoplay
  preload="auto" width="640" height="480" poster="/static/cache/fanart/{{cover}}.jpg"
  data-setup="{}">
  <source src="/watch/{{path}}" type='video/mp4'>
  </video>


  %else:

    <object classid="clsid:67DABFBF-D0AB-41fa-9C46-CC0F21721616" width="640" height="480" codebase="http://go.divx.com/plugin/DivXBrowserPlugin.cab">
      <param name="custommode" value="none" />
      <param name="previewImage" value="/static/cache/fanart/{{cover}}.jpg" />
      <param name="autoPlay" value="false" />
      <param name="src" value="/watch/{{path}}" />

      <embed id="divx" type="video/divx" src="/watch/{{path}}" custommode="none" width="640" height="480" autoPlay="false"  previewImage="/static/cache/fanart/{{cover}}.jpg"  pluginspage="http://go.divx.com/plugin/download/">
      </embed>
    </object>
    <br />No video? <a href="http://www.divx.com/software/divx-plus/web-player" target="_blank">Download</a> the DivX Plus Web Player.
  %end if


</div>


</body>
</html>


