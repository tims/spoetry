import urllib, urllib2
import json
from shove import Shove

cache = Shove('file://spoetry.filecache') 

def search(query):
    cachekey = 'search:'+query
    if query in cache:
        return cache[cachekey]
    
    items = {'q': query}
    url = 'http://ws.spotify.com/search/1/track.json'
    url = url + '?' + urllib.urlencode(items)
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    tracks = json.load(response)['tracks']
    trackresult = None
    if tracks:
        track = tracks[0]
        trackresult = {"trackhref": track['href'], \
                "trackname": track['name'], \
                "albumname": track['album']['name'], \
                "albumhref": track['album']['href'], \
                "artistname" : track['artists'][0]['name'], \
                "artisthref" : track['artists'][0]['href']}
    cache[cachekey] = trackresult
    return trackresult
    
def searchForLargestNgrams(parts, maxN):
    if not parts:
        return []    
    n = maxN
    numsearches = 0
    while n > 0:
        ngram = parts[:n]
        query = " ".join(ngram)
        track = search(query);
        numsearches = numsearches + 1
        if track:
            return [{"query":query, "track": track, 'numsearches': numsearches}] \
                 + searchForLargestNgrams(parts[n:], maxN)
        else:
            n = n - 1
    return [None]

# Useful for testing.
if __name__ == '__main__':
    import sys
    print "Enter a query and press enter:"
    query = sys.stdin.readline()
    print "Querying..."
    results = searchForLargestNgrams(query.split(), 4)
    print "Tracks:"
    for result in results:
        print result

