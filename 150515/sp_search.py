# Search Spotify library and return the URI of the desired item
# The URI can be entered as a location in foobar2000
# Now filters out results not available in specified country (US)
# Displays artist and album type (if applicable) for each result
# The lines for retrieving the artists for albums is convoluted because artists don't appear
#     to be linked directly to albums, but the tracks instead.  The current solution retrieves the
#     first track of each album and prints the artist for the retrieved track.

import sys
import spotipy
import pyperclip
import string

spotify = spotipy.Spotify()

# Choose advanced search type (track, album, playlist)
searchtype = str(raw_input("Please type track, album, or playlist: "))
country = u'US'
            
# Generate search results
search = str(raw_input("Please enter search term: "))
results = spotify.search(q=search, type = searchtype, limit = 30)
items = results[searchtype+'s']['items']

# If there are multiple results, let user choose which URI to copy to clipboard
# Searches with one result automatically copies URI
print '\nResults:\n'
if len(items) > 0:
        for i, t in enumerate(items):
                name = filter(lambda x: x in string.printable, t['name'])
                album_type = ''
                artist = ''
                if searchtype == 'album':
                        get_tracks = spotify.album_tracks(t['id'])
                        track = get_tracks['items'][0]
                        artist = '      '+track['artists'][0]['name']+'\n'
                        if t['album_type'] != 'album':
                                album_type = ' - '+t['album_type']
                elif searchtype == 'track':
                        artist = '      '+t['artists'][0]['name']+'\n'
                if searchtype == 'playlist':
                        print ' ', i, name, '\n', '     ', t['uri'], '\n'
                else:
                        if country in t['available_markets']:
                                print ' ',i, name, album_type, '\n',artist,'     ', t['uri'], '\n'
        if len(items) == 1:
                n = 0
        else:
                n = int(input("Choose from provided list: "))
	album = items[n]
	text = album['uri']
else:
        print 'No results found\n'
        text = 'No results found'        

# Copy final result to clipboard
pyperclip.copy(text)

raw_input("URI copied to clipboard. Press enter to exit")
