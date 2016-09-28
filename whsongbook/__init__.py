"""
Init for WH Songbook

When the application is started, parse and load the songs to memory.
"""

import os
import re
import logging
import pprint
from collections import defaultdict
from flask import Flask

logging.basicConfig(filename="errors.log", level=logging.ERROR)
app = Flask(__name__)
failing_songs = []

from . import parse, display

# Load songs
songs_data = [parse.parse_file(file) for file in os.listdir("songs/production/")]
# Log whie debugging
# logging.debug("Songs Data:\n")
# logging.debug(pprint.pformat(songs_data))

# Load JSON
# songs_data_json = [song.get_json() for song in songs_data]
# logging.debug("Songs JSON:\n")
# logging.debug(pprint.pformat(songs_data_json))


# Die if any songs fail to parse
if failing_songs:
    import sys
    sys.exit(1)

# Build list of artists and their songs
artists_data = defaultdict(list)
for s in songs_data:
    artists_data[s.metadata["artist"]].append(s.metadata["title"])
# Log whie debugging
logging.debug("Artists_Data:\n")
logging.debug(pprint.pformat(artists_data))

from . import views

def check_type(data):
    return isinstance(data, list)

app.jinja_env.globals.update(
    check_type = check_type,
    display_lyrics = display.display_lyrics,
    display_chord = display.display_chord,
    display_section_name = display.display_section_name,
    connect_arabic = display.connect_arabic,
    display_genres = display.display_genres
)

