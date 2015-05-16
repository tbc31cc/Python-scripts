# Find more songs or albums by a chosen artist.
# Must use with command line ""C:\Python27\Lib\more_by_artist.py" "$ascii(%artist%)""

import sys
import spotipy #third-party module
import pyperclip #third-party module
import string

spotify = spotipy.Spotify()

# Choose advanced search type (track or album)
searchtype = str(raw_input("Please type track or album: "))

# args = [path, artist], taken from command line
args = sys.argv

print 'Finding more ' + searchtype+'s ' + 'by ' + args[1]

# Generate search results
results = spotify.search(q="artist:"+args[1], type = searchtype, limit = 20)
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
