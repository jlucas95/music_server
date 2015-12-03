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
        title = self.file.get('title')[0]

        if title is None:
            title = "unknown song"
        self.name = title

class Album:
    def __init__(self, name):
        self.songs = []
        self.name = name

    def __contains__(self, item):
        for song in self.songs:
            if song.name == item:
                return True
        return False

    def find_song(self, song_name):
        for song in self.songs:
            if song.name == song_name:
                return song

class Artist:
    def __init__(self, name):
        self.name = name
        self.albums = []

    def __contains__(self, item):
        for album in self.albums:
            if album.name == item:
                return True
        return False

    def find_album(self, album_name):
        for album in self.albums:
            if album.name == album_name:
                return album






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

            album = song.file.get("album")
            if type(album) is list:
                album = album[0]
            elif album is None:
                album = "unknown album"

            if artist in collection:
                artist = collection.get_artist(artist)
                if album in artist:
                    album = artist.find_album(album)
                else:
                    album = Album(album)
                    artist.albums.append(album)
                album.songs.append(song)
            else:
                artist = Artist(artist)
                if album in artist:
                    album = artist.find_album(album)
                else:
                    album = Album(album)
                    artist.albums.append(album)
                album.songs.append(song)
                collection.artists.append(artist)
        self.sort()

    def sort(self):
        self.artists.sort(key=lambda item: item.name)
        for artist in self.artists:
            artist.albums.sort(key=lambda album: album.name)
            for album in artist.albums:
                album.songs.sort(key=lambda song: song.name)

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



