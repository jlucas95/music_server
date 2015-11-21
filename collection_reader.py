import os
import mutagen.mp3 as mp3
import mutagen.mp4 as mp4
__author__ = 'Jan'

rootfolder = "music"


class Song:
    def __init__(self, path, extension):
        self.extension = extension
        self.path = path
        if extension == ".mp3":
            self.file = mp3.EasyMP3(path)
        elif extension == '.m4a':
            self.file = mp4.MP4(path)
        title = self.file.get('title')[0]

        if title is None:
            title = "unknown song"
        self.name = title


class Artist:
    def __init__(self, name):
        self.name = name
        self.songs = []

    def find_song(self, song_name):
        for song in self.songs:
            if song.name == song_name:
                return song


class MusicCollection:
    def __contains__(self, item):
        for artist in self.artists:
            if artist.name == item:
                return True
        return False

    def get_artist(self, name):
        for artist in self.artists:
            if artist.name == name:
                return artist

    def __init__(self, songs):
        self.artists = []
        self.build(songs)


    def build(self, songs):
        collection = self
        for song in songs:
            artist = song.file.get("artist")[0]
            artist = artist[0:1].capitalize() + artist[1:len(artist)]
            if artist in collection:
                artist = collection.get_artist(artist)
                artist.songs.append(song)
            else:
                artist = Artist(artist)
                artist.songs.append(song)
                collection.artists.append(artist)

    def rebuild(self):
        self.build(map_songs(rootfolder))

def map_songs(path):
    songs = []
    items = os.listdir(path)
    for item in items:
        extension = item[len(item) - 4:]
        if os.path.isdir(path+"/"+item):
            songs += map_songs(path+"/"+item)
        elif extension == ".mp3":
            songs.append(Song(path+"/" + item, extension))
    return songs



