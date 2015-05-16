# Search Spotify library and return the URI of the desired item
# The URI can be entered as a location in foobar2000

import sys
import spotipy
import pyperclip
import string

spotify = spotipy.Spotify()

# Choose advanced search type (track, album, playlist)
searchtype = str(raw_input("Please type track, album, or playlist: "))
            
# Generate search results
search = str(raw_input("Please enter search term: "))
results = spotify.search(q=search, type = searchtype, limit = 20)
items = results[searchtype+'s']['items']

# If there are multiple results, let user choose which URI to copy to clipboard
# Searches with one result automatically copies URI

print '\nResults:\n'
if len(items) > 1:
        for i, t in enumerate(items):
                name = filter(lambda x: x in string.printable, t['name'])
                print ' ',i, name
        n = int(input("Choose from provided list: "))
	album = items[n]
	text = album['uri']
elif len(items) == 1:
        album = items[0]
        text = album['uri']
else:
        print 'No results found'
        text = 'No results found'        

# Copy final result to clipboard
pyperclip.copy(text)

raw_input("URI copied to clipboard. Press enter to exit")
