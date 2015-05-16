# Shows related artists for the given seed artist
# Adapted to let the user choose from list of artists if search returns multiple artists

import spotipy
import sys
import pprint
import string
import pyperclip

# Checks for specified artist in command line
if len(sys.argv) > 1:
    artist_name = sys.argv[1]
else:
    artist_name = str(raw_input("No artist indicated. Enter artist: "))

spotify = spotipy.Spotify()

# Search for artist(s)
result = spotify.search(q='artist:' + artist_name, type='artist')
artists = result['artists']['items']

# If multiple artists, let user choose from list
# Searches with one result are automatically chosen
if len(artists) > 0:
    for i, t in enumerate(artists):
        name = filter(lambda x: x in string.printable, t['name'])
        print ' ', i, name
    if len(artists) == 1:
        n = 0
    else:
        n = int(input("Please choose artist: "))
else:
    print 'No results found'
    
# Generate list of related artists
try:
    name = artists[n]['name']
    uri = artists[n]['uri']

    related = spotify.artist_related_artists(uri)
    print 'Related artists for', name
    for i, artist in enumerate(related['artists']):
        print '  ', i, artist['name']
except:
    print "usage show_related.py [artist-name]"

m = int(input("Choose artist to explore further: "))
searchtype = str(raw_input("Please type track or album: "))
country = u'US'

artist_id = related['artists'][m]['id']

# Find songs or albums for chosen artist
if searchtype == 'album':
        results = spotify.artist_albums(artist_id)
        items = results['items']
elif searchtype == 'track':
        results = spotify.artist_top_tracks(artist_id)
        items = results['tracks']

# If there are multiple results, let user choose which URI to copy to clipboard.
# Searches with one result automatically copies URI.
print '\nResults:\n'
if len(items) > 0:
        for i, t in enumerate(items):
                name = filter(lambda x: x in string.printable, t['name'])
                album_type = ''
                if searchtype == 'album':
                        if t['album_type'] != 'album':
                                album_type = ' - '+t['album_type']
                if country in t['available_markets']:
                        print ' ',i, name, album_type, '\n','     ', t['uri'], '\n'
        if len(items) == 1:
                n = 0
        else:
                n = int(input("Choose from provided list: "))
	item = items[n]
	text = item['uri']
else:
        print 'No results found'
        text = 'No results found'
        
# Copy final result to clipboard
pyperclip.copy(text)


raw_input("URI copied to clipboard. Press enter to exit.")
