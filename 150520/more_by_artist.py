# Find more songs or albums by a chosen artist
# Now filters out results not available in specified country
# User can choose to view entire list of results as text file
# Use with command line ""C:\Python27\Lib\more_by_artist.py" "$ascii(%artist%)""

import sys
import spotipy #third-party module
import pyperclip #third-party module
import string

spotify = spotipy.Spotify()
display = "URI(s) copied to clipboard. Press enter to exit"

# Specified country
country = u'US'

# args = [path, artist], taken from command line
if len(sys.argv) > 1:
    artist_name = sys.argv[1]
else:
    artist_name = str(raw_input("Enter artist name: "))

#If multiple artists are found, list them and have user choose one
results1 = spotify.search(q='artist:' + artist_name, type = 'artist')
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

# Choose advanced search type (track or album)
valid_types = ['track', 'album']
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

print 'Finding ' + searchtype + 's by ' + artist

# Find songs or albums for chosen artist
if searchtype == 'album':
        results = spotify.artist_albums(artist_id, country = str(country))
        items = results['items']
elif searchtype == 'track':
        results = spotify.artist_top_tracks(artist_id, country = str(country))
        items = results['tracks']

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
        album = ''
        release_date = ''
        if searchtype == 'album':
                get_artist = spotify.album(t['id'])
                release_date = ' ('+get_artist['release_date'][0:4]+') '
                if t['album_type'] != 'album':
                        album_type = ' - '+t['album_type']
                line1 = ' '+str(i)+' '+name+album_type+release_date
        else:
                album = filter(lambda x: x in string.printable, ' from '+'"'+t['album']['name'])
                line1 = shorten(' '+str(i)+' '+name+album)+'"'
        line2 = '\n      '+t['uri']+'\n'
        return line1+line2

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
        # Copy final result to clipboard/Open list as text file
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
        print 'No results found'
        text = 'No results found'
        display = 'Press enter to exit'

raw_input(display)
