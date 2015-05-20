# Search Spotify library and return the URI of the desired item
# The URI can be entered as a location in foobar2000
# For removing items not available in chosen country, filters out actual items in list.
#     Previous method did not attempt to filter list and instead printed blank line when item was not available.
# User can choose to view entire list of results in text file
# Displays artist and album type (if applicable) for each result

import sys
import spotipy
import pyperclip
import string

spotify = spotipy.Spotify()
display = "URI(s) copied to clipboard. Press enter to exit"

# Specified country
country = u'US'

# Choose advanced search type (track, album, playlist)
valid_types = ['track', 'album', 'playlist']
def get_valid_type():
        i = str(raw_input("Please type track, album, or playlist: "))
        if i in valid_types:
                return i
        else:
                return None
while True:
        searchtype = get_valid_type()
        if searchtype:
                break
            
# Generate search results
search = str(raw_input("Please enter search term: "))
results = spotify.search(q=search, type = searchtype, limit = 20)
items = results[searchtype+'s']['items']

# Filter out results not available in specified country
if searchtype != 'playlist':
        for i, t in enumerate(items):
                if country not in items[i]['available_markets']:
                        items[i] = []
        while [] in items:
                items.remove([])

# Shorten long strings
def shorten(string):
        if len(string) > 80:
                return string[0:80]+'...'
        else:
                return string

# Generate list of results
def print_info(i,t):
        name = filter(lambda x: x in string.printable, t['name'])
        album_type = ''
        artist = ''
        album = ''
        release_date = ''
        if searchtype == 'album':
                get_artist = spotify.album(t['id'])
                artist_name = get_artist['artists'][0]['name']
                release_date = ' ('+get_artist['release_date'][0:4]+') '
                artist = filter(lambda x: x in string.printable, '      '+artist_name)
                if items[i]['album_type'] != 'album':
                        album_type = ' - '+t['album_type']
                line1 = ' '+str(i)+' '+name+album_type+release_date
        elif searchtype == 'track':
                artist = filter(lambda x: x in string.printable, '      '+t['artists'][0]['name']+'\n')
                album = filter(lambda x: x in string.printable, ' from '+'"'+t['album']['name'])
                line1 = shorten(' '+str(i)+' '+name+album)+'"'
        else:
                line1 = ' '+str(i)+' '+name
        line2 = '\n'+artist
        line3 = '\n      '+t['uri']+'\n'
        return line1+line2+line3

# If there are multiple results, let user choose which URI to copy to clipboard
# Searches with one result automatically copies URI
print '\nResults:\n'
if len(items) > 0:
        for i, t in enumerate(items):
                print print_info(i,t)
        if len(items) == 1:
                n = 0
        else:
                n = int(input("Choose from provided list. Enter -1 to choose all items. "))
        # Copy final result to clipboard/Open list of results in text file
        if n == -1:
                text = ''
                for i, t in enumerate(items):
                        text = text + print_info(i,t)
                import subprocess as sp
                programName = 'notepad.exe'
                with open('output.txt', 'w') as text_file:
                        text_file.write(text)
                sp.Popen([programName,'output.txt'])
        else:
                text = items[n]['uri']
                pyperclip.copy(text)
else:
        print 'No results found\n'
        text = 'No results found'
        display = 'Press enter to exit'

raw_input(display)
