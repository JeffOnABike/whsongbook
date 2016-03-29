import re

# sample input
string_sample_chords = """
c1 a:m f c2 g
c1 a:m f c2 g \break
"""

list_sample_chords = ["c1", "a:m", "f", "c2", "g", "c1", "a:m", "f", "c2", "g"]

sample_lyrics = """
[]Love of mine some day []you will die
But I'll be []close behind. I'll follow []you into the []dark,
No []blinding light or tunnels to []gates of white
Just our hands []clasped so tight, waiting []for the hint of a []spark.
"""

def match_chords_with_lyrics(chords, lyrics):
    """Match a set of chords with the text of lyrics"""

    output = ""

    for l in lyrics.splitlines():
        newline = ""
        for x in l.split("["):
            if "]" in x:
                newsection = "[%s%s" % (chords.pop(0), x)
            else:
                newsection = x
            newline += newsection
        output += newline + "\n"

    return output

print(match_chords_with_lyrics(list_sample_chords, sample_lyrics))
