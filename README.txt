Spoetry attempts to auto generate spotify playlists from poetry.

It searches the spotify metadata api using phrases up to a maximum of 4 terms,
decreasing the number of terms until it finds a match, repeatin with the remaining 
terms to find the next track, until there are no more terms.

Unfortunately there doesn't seem to be a documented way of querying over track title only,
so many matches will partly match in the album or artist name.

It uses Shove to do on disk caching of results. 
It's not going to be fast, and the cached items never timeout, but it will stop 
pointless network access. It will currently grow the cache until the server runs out of diskspace. 
Using a shared memcache with a 1 week timeout would be better.

It is currently running at:
http://188.40.147.70:8000/spoetry/

Requires:
  python 2.6
  django 1.2
  Shove 0.2.1
  
To start the server change to the src/spoetry directory and run:
  python manage.py runserver
  
