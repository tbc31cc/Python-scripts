# Find more songs or albums by a chosen artist
# Now filters out results not available in specified country
# Must use with command line ""C:\Python27\Lib\more_by_artist.py" "$ascii(%artist%)""

import sys
import spotipy #third-party module
import pyperclip #third-party module
import string

spotify = spotipy.Spotify()

#Choose advanced search type (track or album)
searchtype = str(raw_input("Please type track or album: "))
country = u'US'

# args = [path, artist], taken from command line
args = sys.argv

#If multiple artists are found, list them and have user choose one
results1 = spotify.search(q='artist:' + args[1], type = 'artist')
artists = results1['artists']['items']
if len(artists) > 0:
        for i, t in enumerate(artists):
                name = filter(lambda x: x in string.printable, t['name'])
                print ' ', i, name
        if len(artists) == 1:
                n = 0
        else:
                n = int(input("Please choose artist: "))
        choice = artists[n]
        artist = choice['name']
        artist_id = choice['id']
else:
        print 'No results found'

print 'Finding more ' + searchtype + ' s by ' + artist

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

raw_input("URI copied to clipboard. Press enter to exit")
