import urllib, urllib2
import json
from shove import Shove

cache = Shove('file://spoetry.filecache') 

def search(query):
    items = {'q': query}
    url = 'http://ws.spotify.com/search/1/track.json'
    url = url + '?' + urllib.urlencode(items)
    print "get http, " + url
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    tracks = json.load(response)['tracks']
    trackresults = []
    for track in tracks:
        trackresult = {"trackhref": track['href'], \
                "trackname": track['name'], \
                "albumname": track['album']['name'], \
                "albumhref": track['album']['href']}
        if track['artists']:
            trackresult["artistname"] = track['artists'][0]['name']
            trackresult["artisthref"] = track['artists'][0].get('href')
            
        trackresults.append(trackresult)
    
    return trackresults
    
def poemToPlaylist(poem, maxNgram):
    lines = poem.split('\n')
    results = []
    for line in lines:
        parts = line.split()
        results.append(searchForLargestNgrams(parts, maxNgram))
    return results
    
  
def searchForLargestNgrams(parts, maxN):
    if not parts:
        return []
    n = min(maxN, len(parts))
    while n > 0:
        diff = len(parts) - n
        for start in range(diff + 1):
            end = start + n
            ngram = parts[start:end]
            result = searchExactNgram(ngram)
            if result:
                results = searchForLargestNgrams(parts[:start], maxN) + [result] + searchForLargestNgrams(parts[end:], maxN)
                return results
        n = n - 1
    query = " ".join(parts).lower().strip()
    return [{"query": query, "track": None}]

def searchExactNgram(ngram):
    query = " ".join(ngram)
    query = query.lower().strip()
    
    cachekey = 'searchExactNgram:1:' + query
    if cachekey in cache:
        print "get cache hit, " + cachekey
        return cache[cachekey]
    print "get cache miss, " + cachekey
    
    tracks = search('"' + query + '"')
    result = None
    for track in tracks:
        if track['trackname'].lower().strip() == query:
            result = {"query":query, "track": track}
                
    cache[cachekey] = result
    return result

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

