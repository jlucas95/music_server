from http.server import HTTPServer, BaseHTTPRequestHandler
import collection_reader as cr
from player import Player
import json.encoder as json
from urllib.request import unquote

__author__ = 'Jan'

ADRESS = ''
PORT = 80

collection = cr.MusicCollection(cr.map_songs(cr.rootfolder))
print("collection built")

music = Player()


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/artists":
            self.send_artists()
        elif self.path.startswith("/albums"):
            self.send_albums()
        elif self.path.startswith("/songs"):
            self.send_songs()
        elif self.path == "/":
            self.standard_response()
        elif self.path.startswith("/css"):
            path = self.path[1:len(self.path)]
            with open(path) as file:
                data = file.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/css")
                self.end_headers()
                self.wfile.write(data.encode())
        elif self.path.startswith("/font"):
            path = self.path[1:len(self.path)]
            if path.endswith("?"):
                path = path [0:len(path)-1]
            try:
                with open(path, "rb") as file:
                    data = file.read()
                    self.send_response(200)
                    self.wfile.write(data)
            except OSError:
                self.send_error(404, "File not found")
        elif self.path.startswith("/favicon.ico"):
            self.send_response(200)
            with open("favicon.ico", "rb") as icon:
                self.end_headers()
                self.wfile.write(icon.read())

        else:
            print('could not find')
            self.send_error(404, "File not found")

    put_dict = {
        "rebuild": collection.rebuild,
        "play": lambda self: self.resume_song,

    }

    def do_PUT(self):
        # TODO rewrite elifs to function dictionary
        if self.path == "/rebuild":
            collection.rebuild()
        elif self.path == "/play":
            self.resume_song()
        elif self.path.startswith("/play"):
            self.play_song()
        elif self.path.startswith("/add"):
            self.add_song()
        elif self.path == "/pause":
            self.pause_song()
        elif self.path == "/stop":
            self.stop_song()
        elif self.path == "/next":
            self.next_song()
        elif self.path == "/volume/down":
            self.decrease_volume()
        elif self.path == "/volume/up":
            self.increase_volume()
        self.end()

    def standard_response(self):
        with open("page.html") as page:
            data = page.read()
            self.send_response(200)
            self.wfile.write(data.encode())

    def send_artists(self):
        data = [x.name for x in collection.artists]
        encoder = json.JSONEncoder()
        data = encoder.encode(data)
        self.wfile.write(data.encode())

    def send_albums(self):
        # Path will be something like albums/artist
        seperated_path = self.path.split('/')
        artist = unquote(seperated_path[len(seperated_path) - 1])
        artist = collection.get_artist(artist)
        albums = [x.name for x in artist.albums]
        encoder = json.JSONEncoder()
        albums = encoder.encode(albums)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(albums.encode())

    def send_songs(self):
        # Path will be something like songs/artist/album
        separated_path = self.path.split('/')
        # Get artist
        artist = unquote(separated_path[len(separated_path) - 2])
        artist = collection.get_artist(artist)
        # Get album
        album = unquote(separated_path[len(separated_path) - 1])
        album = artist.find_album(album)
        # get all the songs
        songs = [x.name for x in album.songs]
        # Encode the list into JSON
        encoder = json.JSONEncoder()
        songs = encoder.encode(songs)
        # Send the songs
        self.send_response(200)
        self.end_headers()
        self.wfile.write(songs.encode())

    def play_song(self):
        # Get information from the path
        path = self.path.split("/")
        artist = unquote(path[2])
        album = unquote(path[3])
        song = unquote(path[4])
        # Get the corresponding objects
        artist = collection.get_artist(artist)
        album = artist.find_album(album)
        song = album.find_song(song)
        # stop current music
        music.stop()
        # Clear the song queue
        music.clearList()
        # Add the song to the queue
        music.add_song(song.path)

    def add_song(self):
        # Get stuff out of the URL
        path = self.path.split("/")
        artist = unquote(path[2])
        album = unquote(path[3])
        song = unquote(path[4])
        # Get the corresponding objects
        artist = collection.get_artist(artist)
        album = artist.find_album(album)
        song = album.find_song(song)
        # Add the song to the queue
        music.add_song(song.path)

    def stop_song(self):
        music.stop()

    def pause_song(self):
        music.pause()

    def resume_song(self):
        music.play()

    def next_song(self):
        music.next()

    def end(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'1')

    def decrease_volume(self):
        music.decrease_volume()

    def increase_volume(self):
        music.increase_volume()


if __name__ == "__main__":
    print("starting server")
    server = HTTPServer((ADRESS, PORT), handler)
    server.serve_forever()
