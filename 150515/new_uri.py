# Sometimes Spotify stores multiple entries for an album or track, or may accidentally add an album/track that isn't available in your country
# If you choose a bad URI with the original search, use this to load a new entry that hopefully works
# Now filters out results that are not available specified country (US)
# Must use with command line ""C:\Python27\Lib\new_uri.py" "$ascii(%artist%)" "$ascii(%album%)" "$ascii(%title%)""

import sys
import spotipy #third-party module
import pyperclip #third-party module
import string

spotify = spotipy.Spotify()

# Choose advanced search type (track or album)
searchtype = str(raw_input("Please type track or album: "))

#Specified country
country = u'US'

# args = [path, artist, album, track], taken from command line
args = sys.argv

if searchtype == 'album':
        item = args[2]
elif searchtype == 'track':
        item = args[3]

print 'Finding URI for ' + searchtype +': ' + '"'+item+'"' + ' by ' + args[1]

# Generate search results
results = spotify.search(q="artist:"+args[1]+' '+searchtype+':'+item, type = searchtype, limit = 30)
items = results[searchtype+'s']['items']

# If there are multiple results, let user choose which URI to copy to clipboard.
# Searches with one result automatically copies URI.
print '\nResults:\n'
if len(items) > 0:
        for i, t in enumerate(items):
                name = filter(lambda x: x in string.printable, t['name'])
                album_type = ''
                artist = ''
                if searchtype == 'album':
                        if t['album_type'] != 'album':
                                album_type = ' - '+t['album_type']
                if country in t['available_markets']:
                        print ' ',i, t['uri'], '\n', '     ', album_type
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
