"""
Views

This module defines the endpoints of the Flask app.
"""

from random import choice
from collections import defaultdict
from flask import render_template, redirect
from . import app, songs_data, artists_data


@app.route("/")
def home():
    """
    Display the home page.
    """

    return render_template("index.html")


@app.route("/about")
def about():
    """
    Display the about page.
    """

    return render_template("about.html")


@app.route("/random")
def random():
    """
    Display a randomly selected song page.
    """

    selection = choice(songs_data)
    artist_underscore = selection.metadata["artist"].replace(" ", "_")
    title_underscore = selection.metadata["title"].replace(" ", "_")
    return redirect("/browse/%s/%s" % (artist_underscore, title_underscore))


@app.route("/browse")
def browse():
    """
    Display a list of links to all songs.
    """

    songs = []
    for song in songs_data:
        cur = defaultdict(list)
        cur["artist"] = song.metadata["artist"]
        cur["title"] = song.metadata["title"]
        cur["artist_link"] = "/browse/%s" % (cur["artist"].replace(" ", "_"))
        cur["song_link"] = "%s/%s" % (cur["artist_link"], cur["title"].replace(
            " ", "_"))
        songs.append(cur)

    return render_template(
        "browse.html", songs=sorted(
            songs, key=lambda song: song["title"]))


@app.route("/browse/<artist_underscore>/<title_underscore>")
def song(artist_underscore, title_underscore):
    """
    Display a specific song transcription.
    """

    artist = artist_underscore.replace("_", " ")
    title = title_underscore.replace("_", " ")

    # test for urls to songs that do not exist
    try:
        selection = next(song for song in songs_data
                         if song.metadata["title"] == title and song.metadata[
                             "artist"] == artist)
        artist_link = "/browse/%s" % (artist.replace(" ", "_"))
    except StopIteration:
        return redirect("/browse")

    return render_template(
        "song.html",
        filename=selection.filename,
        title=title,
        artist=artist,
        metadata=selection.metadata,
        artist_link=artist_link,
        sections=selection.content)


@app.route("/browse/<artist_underscore>")
def artist(artist_underscore):
    """
    Display a page for each artist, with a list of links to their songs.
    """

    artist = artist_underscore.replace("_", " ")

    # test for urls to artists that do not exist
    if artist not in artists_data.keys():
        return redirect("/browse")
    else:
        songs = []
        for song in artists_data[artist]:
            cur = defaultdict(list)
            cur["title"] = song
            cur["link"] = "/browse/%s/%s" % (artist_underscore, song.replace(
                " ", "_"))
            songs.append(cur)

        return render_template("artist.html", artist=artist, songs=songs)


@app.route("/songs_list")
def songs_list():
    ret = ""
    for song in songs_data:
        ret += str(song.metadata)
    return str(ret)
