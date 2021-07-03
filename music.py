from os import environ, path, listdir
from mutagen.mp3 import MP3

# Get the music path
music_path = environ.get('MUSIC_PATH')

# Expand the path to resolve the tilde if there is one
music_path = path.expanduser(music_path)

def collect():
  # Get the directories from this path
  playlists = [d for d in listdir(music_path) if path.isdir(path.join(music_path, d))]
  
  for playlist in playlists:
    absolute_path = path.join(music_path, playlist)
    # Get all files that is an mp3
    musics = [m for m in listdir(absolute_path) if m.endswith('.mp3')]

    # Compute count
    yield f'youtube,playlist={playlist} count={len(musics)}'

    # Compute duration
    duration = 0
    for music in [path.join(absolute_path, m) for m in musics]:
      audio = MP3(music)
      duration += audio.info.length
    yield f'youtube,playlist={playlist} duration={duration}'
