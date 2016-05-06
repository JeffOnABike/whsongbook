from pprint import pprint
import ast

text = """
header:
    title = "I Will Follow You Into the Dark"
    artist = "Death Cab for Cutie"
    capo = 5
    year = 2005
    genre = ["indie"]

instrumental:
    <chorus chords>

verse:
    [c]Love of mine some day [a:m]you will die
    But I'll be [f]close behind. I'll follow [c]you into the [g]dark,]
    No [c]blinding light or tunnels to [a:m]gates of white]
    Just our hands [f]clasped so tight, waiting [c]for the hint of a [g]spark.

chorus:
    If [a:m]Heaven and Hell de[c]cide that they [f]both are satisf[c]ied [g]
    Ill[a:m]uminate the [c]"no"s on their [g]vacancy [g]signs
    If [a:m]there's no one be[c]side you when your [e]soul em[a:m]barks [g]
    Then [f]I'll follow [f:m]you into the dark [c] [c]

verse:
    In Catholic school as vicious as Roman rule
    I got my knuckles bruised by a lady in black
    And I held my tongue as she told me
    "Son, fear is the heart of love." So I never went back

chorus

verse:
    You and me have seen everything to see
    From Bangkok to Calgary, and the soles of your shoes
    Are all worn down. The time for sleep is now.
    It's nothing to cry about, 'cause we'll hold each other soon

bridge:
    In the [a:m]blackest of [f]rooms [f] [f]

chorus

chorus:
    and [f]I’ll follow [f:m]you into the [c]dark.
"""

sections = []
metadata = {}
cur = None
for line in text.splitlines():
    line = line.rstrip()
    if not line: continue
    if line == line.lstrip():
        cur = []
        sections.append((line.strip(":"), cur))
    else:
        cur.append(line.strip())

if sections[0][0] == "header":
    for line in sections.pop(0)[1]:
        key, value = line.split('=', 1)
        metadata[key] = ast.literal_eval(value.strip())

pprint(metadata)
pprint(sections)
