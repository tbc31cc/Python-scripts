# Sometimes Spotify stores multiple entries for an album or track
# If you choose a dead URI with the original search, use this to load a new entry that hopefully works
# Must use with command line ""C:\Python27\Lib\new_uri.py" "$ascii(%artist%)" "$ascii(%album%)" "$ascii(%title%)""

import sys
import spotipy #third-party module
import pyperclip #third-party module
import string

spotify = spotipy.Spotify()

# Choose advanced search type (track or album)
searchtype = str(raw_input("Please type track or album: "))

# args = [path, artist, album, track], taken from command line
args = sys.argv

if searchtype == 'album':
        item = args[2]
elif searchtype == 'track':
        item = args[3]

print 'Finding URI for ' + searchtype +': ' + '"'+item+'"' + ' by ' + args[1]

# Generate search results
results = spotify.search(q="artist:"+args[1]+' '+searchtype+':'+item, type = searchtype, limit = 20)
items = results[searchtype+'s']['items']

# If there are multiple results, let user choose which URI to copy to clipboard.
# Searches with one result automatically copies URI.
print '\nResults:\n'
if len(items) > 1:
        for i, t in enumerate(items):
                name = filter(lambda x: x in string.printable, t['name'])
                print ' ',i, name
                print '    ', t['uri']
        n = int(input("Choose from provided list: "))
	album = items[n]
	text = album['uri']
elif len(items) == 1:
        album = items[0]
        text = album['uri']
        name = filter(lambda x: x in string.printable, album['name'])
        print ' ', name
        print '    ', album['uri']
else:
        print 'No results found'
        text = 'No results found'
        
# Copy final result to clipboard
pyperclip.copy(text)

raw_input("URI copied to clipboard. Press enter to exit")
