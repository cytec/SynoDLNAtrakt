#SynoDLNAtrakt

###Version 2.0

This is Version 2.0 of SynoDLNAtrakt.

Some new stuff:

* Webfrontend
* Semi MediaCenter (lists all Episodes/Movies in the DLNA index)
* deamon support
* different sort options (lastseen/unseen/unrated)
* option to rate movies/episodes
* option to scrobble/mark as seen manually
* option to delete entrys from databse/synoindex/HDD
* trakt 2 way sync (syncs seen status/rating for movies/episodes from and to trakt)

some screenshots can be viewed here [BETA Screenshots](http://imgur.com/a/Y4bO1)

#SPK Installation (recommendet)

just add http://cytec.us/spk/ to your Packagemanager Sources and install SynoDLNAtrakt.


#Source Installation

1.	Make sure you have ipkg installed on your Diskstation [How to install ipkg](http://forum.synology.com/wiki/index.php/Overview_on_modifying_the_Synology_Server,_bootstrap,_ipkg_etc#Installing_compiled.2Fbinary_programs_using_ipkg)
2.	install python2.6
3.	install git
4.	git clone //URLHERE//
5.	change to the SynoDLNAtrakt directory
6.	change the config file if needed
7.	start SynoDLNAtrakt (python SynoDLNAtrakt.py start)

now you can access SynoDLNAtrakt through your browser: http://YOURIP:1337
