import glob
import eyed3
import re
import os

# this will look for any mp3 files in the current folder which are named
# "artist / title" as their tagged title and fix this so the title
# is correct, the track artist is set correctly, and the album artist
# is marked as Various Artists, also setting the compilation flag
files = glob.glob('./*.mp3')
for file in files:
  audiof = eyed3.load(file)
  long_title = audiof.tag.title
  m = re.search('(.*) / (.*)', long_title)
  if m:
    artist = m.group(1)
    title = m.group(2)
    audiof.tag.artist = artist
    audiof.tag.title = title
    audiof.tag.album_artist = u"Various Artists"
    audiof.tag.setTextFrame(u"TCMP", u"1")
    audiof.tag.save()
    title_for_file = title.translate({ord(c): None for c in '?<>:*|'})
    os.rename(file, file[:4] + " - " + title_for_file + ".mp3")
