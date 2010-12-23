Spoetry attempts to auto generate spotify playlists from poetry.

It search the spotify metadata api using phrases up to a maximum of 4 terms,
decreasing the number of terms until it finds a match, repeatin with the remaining 
terms to find the next track, until there are no more terms.

Unfortunately there doesn't seem to be a documented way of querying over track title only,
so many matches will partly match in the album or artist name.

There is currently no caching at all. It should really store results in a local
memcache (or on disks cache) with a 1 week timeout.

It is currently running at:
http://188.40.147.70:8000/spoetry/

Requires:
  python 2.6
  django 1.2
  
To start the server change to the src/spoetry directory and run:
  python manage.py runserver
  
