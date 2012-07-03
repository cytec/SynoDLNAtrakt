This is still in alpha/beta state.

SynoDLNAtrakt is a trakt.tv plugin for Synology DiskStations. If your running the default Synology MediaServer and watching stuff over UPNP or DLNA directly on your Device but want to keep your trakt.tv account up to date, this is the right thing for you.

In order to make this work you must have your MediaServer running in Debug mode (see wiki for screenshot)

How it works:
SynoDLNAtrakt scans a access.log which is provided by lighthttpd which runs the Synologys native MediaServer. Sadly this log is only available in Debug mode.

The access.log contains which file was served and when. more exactly a 5 digit number with an file extension and the time it was requested.

this 5 digit number is the id from Synologys Mediaindex Database.

So SynoDLNAtrakt extracts this number and queries the Mediaindex Database for its Path.

the path is checked for containing your Series/Movies home dir and decides based on this if its a movie or a series.

If you used a Mediacenter to maintain your Series/Movies you may already have some nfo files for those files, SynoDLNAtrakt checks for existing files first before connecting to tvdb/tmdb to get some infos based on the filenames

then it scribbles all that stuff to your trakt.tv account, updates his database and clears the log (optionally)