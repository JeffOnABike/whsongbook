import logging
import ast
import re

logging.basicConfig(filename="song_errors.log", level=logging.ERROR)

class Song:

    def __init__(self, filename, metadata, content):
        self.filename = filename
        self.metadata = metadata
        self.content = content

def check_chord(chord):
    """
    Check that chords are in the right format.
    """

    # allow anything in parentheses (eg "(x3)")
    if chord[:1] == "(":
        pass

    # allow empty strings (for lyrics with no chords)
    elif len(chord) == 0:
        pass

    # reject unparsable characters
    else:
        try:
            parsable = "[a-gsuim1-9:/\|]+"
            assert(re.fullmatch(parsable, chord) != None)
        except AssertionError:
            return False

    return True

def parse_header(header):
    """
    TODO: This function is unused and incomplete
    Parse header and check that metadata is in the right format
    """

    parsable = ["title", "artist", "genres", "year", "capo"]

    metadata = []
    for line in header:
        try:
            key, value = line.split('=', 1)
            metadata[key.strip()] = ast.literal_eval(value.strip())
        except ValueError:
            return (False, False)

    return metadata

def check_section(section):
    """
    Check that sections are recognizeable.
    """

    parsable = ["header", "verse", "chorus", "bridge", "instrumental", "notes"]

    try:
        assert(section[0] in parsable)
    except AssertionError:
        return False

    return True

def parse_file(filename):
    songs_dir = "songs/production/"
    full_title = songs_dir + filename
    sections = []
    metadata = {}
    cur = None

    with open(full_title, "r") as f:
        text = f.read()

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
                        chord, lyric = section.split("]", 1)
                        if " " in chord:
                            multi_chords = chord.split(" ")
                            for m in multi_chords:
                                chord_sections.append((m,""))
                        else:
                            chord_sections.append((chord, lyric))
                    elif section:
                        chord_sections.append(("", section))
                # throw error if chord not recognized
                for chord, lyric in chord_sections:
                    try:
                        assert(check_chord(chord) == True)
                    except AssertionError:
                        logging.error("Unparsable chord (%s) in file (%s)" % (chord, filename))
                line = chord_sections

            cur.append(line)

    # check sections
    for s in sections:
        try:
            assert(check_section(section) == True)
        except AssertionError:
            logging.error("Unrecognized section (%s) in file (%s)" % (chord, filename))

    # convert header section to dictionary
    if sections[0][0] == "header":
        ## attempting to switch to fuction "parse_header()"
        # header = sections.pop(0)[1]
        # metadata = parse_header(header)
        # if False in metadata:
        #     logging.error("Unparsable header line (%s) in file (%s)" % (line, filename))

        # the old way
        for line in sections.pop(0)[1]:
            key, value = line.split('=', 1)
            metadata[key.strip()] = ast.literal_eval(value.strip())

    # return str(sections)
    return Song(filename, metadata, sections)