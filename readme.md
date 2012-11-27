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


#Installation

1.	Make sure you have ipkg installed on your Diskstation [How to install ipkg](http://forum.synology.com/wiki/index.php/Overview_on_modifying_the_Synology_Server,_bootstrap,_ipkg_etc#Installing_compiled.2Fbinary_programs_using_ipkg)
2.	install python2.6
3.	install py26-psycopg2
4.	install git
5.	git clone //URLHERE//
6.	change to the SynoDLNAtrakt directory
7.	change the config file if needed
8.	start SynoDLNAtrakt (python SynoDLNAtrakt.py)

now you can access SynoDLNAtrakt through your browser: http://YOURIP:1337

###Optional
if you like to run SynoDLNAtrakt as a daemon you can do this by useing a screen session:

First make sure you have installed "screen" over ipkg successfully, than simply start SynoDLNAtrakt like this

    screen -dmS synodlnatrakt sh -c 'python SynoDLNAtrakt.py

to reattach to that screen session you can simply type in:

	screen -r synodlnatrakt

and close your ssh window if your done (the screen session will continue running)

to kill the session get reattached and hit ctrl+c OR run

	screen -X -S synodlnatrakt kill