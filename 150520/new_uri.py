# Sometimes Spotify stores multiple entries for an album or track, or you may accidentally add an album/track that isn't available in your country
# If you choose a bad URI with the original search, use this to load a new entry that hopefully works
# Now filters out results that are not available in specified country (US) (new method)
# Program now asks user to re-enter searchtype in the case of an invalid entry
# User can choose to open entire list of results as a text file
# Use with command line ""C:\Python27\Lib\new_uri.py" "$ascii(%artist%)" "$ascii(%album%)" "$ascii(%title%)""

import sys
import spotipy #third-party module
import pyperclip #third-party module
import string

spotify = spotipy.Spotify()
display = "URI(s) copied to clipboard. Press enter to exit"

# Specified country
country = u'US'

# args = [path, artist, album, track], taken from command line
if len(sys.argv) > 1:
        artist_name = sys.argv[1]
else:
        artist_name = str(raw_input('Enter artist name: '))

# Choose advanced search type (track or album)
valid_types = ['track','album']
def get_valid_type():
        i = str(raw_input("Please type track or album: "))
        if i in valid_types:
                return i
        else:
                return None
while True:
        searchtype = get_valid_type()
        if searchtype:
                break

if searchtype == 'album':
        if len(sys.argv) > 2:
                item = sys.argv[2]
        else:
                item = str(raw_input('Enter album title: '))
elif searchtype == 'track':
        if len(sys.argv) > 3:
                item = sys.argv[3]
        else:
                item = str(raw_input('Enter track title: '))
        
print 'Finding URI for ' + searchtype +': ' + '"'+item+'"' + ' by ' + artist_name

# Generate search results
results = spotify.search(q="artist:"+artist_name+' '+searchtype+':'+item, type = searchtype, limit = 20)
items = results[searchtype+'s']['items']

# Filter out results not available in specified country
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

# Function for generating list of results
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

# If there are multiple results, let user choose which URI to copy to clipboard.
# Searches with one result automatically copies URI.
print '\nResults:\n'
if len(items) > 0:
        for i, t in enumerate(items):
                print print_info(i,t)
        if len(items) == 1:
                n = 0
        else:
                n = int(input("Choose from provided list. Enter -1 to choose all items "))
        # Copy final result to clipboard/Open full list as text file
        if n == -1:
                text = ''
                for i, t in enumerate(items):
                        text = text + '\n' + print_info(i,t)
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
