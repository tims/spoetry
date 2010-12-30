import urllib, urllib2
import json
from shove import Shove

cache = Shove('file://spoetry.filecache') 

def search(query):
    cachekey = 'search:2:' + query
    if query in cache:
        return cache[cachekey]
    
    items = {'q': query}
    url = 'http://ws.spotify.com/search/1/track.json'
    url = url + '?' + urllib.urlencode(items)
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
    cache[cachekey] = trackresults
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
    n = maxN
    numsearches = 0
    while n > 0:
        ngram = parts[:n]
        query = " ".join(ngram)
        query = query.lower().strip()
        tracks = search('"' + query + '"');
        numsearches = numsearches + 1
        for track in tracks:
            if track['trackname'].lower().strip() == query:
                return [{"query":query, "track": track, 'numsearches': numsearches}] \
                     + searchForLargestNgrams(parts[n:], maxN)
        n = n - 1
    query = " ".join(parts).lower().strip()
    return [{"query": query, "track": None, 'numsearches': numsearches}]

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

