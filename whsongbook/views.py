from . import app
from flask import render_template
from os import listdir
import ast


@app.route("/")
def home():
    return render_template("song_fixed.html")

@app.route("/songs")
def songs():
    """
    List all songs in the production folder
    """

    songs_dir = "songs/production/"
    return str(listdir(songs_dir))

@app.route("/songs/<title>")
def song(title):
    # Test with "http://0.0.0.0:8080/songs/i_will_follow_you_into_the_dark-death_cab_for_cutie"

    songs_dir = "songs/production/"
    full_title = songs_dir + title + ".song"
    sections = []
    metadata = {}
    cur = None

    with open(full_title, "r") as f:
        text = f.read()

    # Parse file
    for line in text.splitlines():
        # strip initial white space
        line = line.rstrip()
        # ignore blank lines
        if not line: continue

        # identify line type statements (ie "chorus:")
        if line == line.lstrip():
            cur = []
            sections.append((line.strip(":"), cur))

        # work with all remaining lines (content)
        else:
            line = line.strip()
            # separate chords from lyrics
            if "[" in line and "genres = " not in line:
                chord_sections = []
                for section in line.split("["):
                    if "]" in section:
                        chord, lyric = section.split("]")
                        chord_sections.append((chord, lyric))
                line = chord_sections
            cur.append(line)

    # convert header section to dictionary
    if sections[0][0] == "header":
        for line in sections.pop(0)[1]:
            key, value = line.split('=', 1)
            metadata[key] = ast.literal_eval(value.strip())

    return render_template("song.html",
                           title=metadata['title'],
                           artist=metadata['artist'],
                           sections=sections
    )
    # return render_template("song.html")

