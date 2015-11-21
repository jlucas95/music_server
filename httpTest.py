from http.server import HTTPServer, BaseHTTPRequestHandler
import collection_reader as cr
from player import Player
import json.encoder as json
from urllib.request import unquote
__author__ = 'Jan'

ADRESS = '127.0.0.1'
PORT = 80

collection = cr.MusicCollection(cr.map_songs(cr.rootfolder))
print("collection built")

music = Player()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/artists":
            self.send_artists()
        elif self.path.startswith("/songs"):
            self.send_songs()
        elif self.path == "/":
            self.standardResponse()
        elif self.path.startswith("/css"):
            path = self.path[1:len(self.path)]
            with open(path) as file:
                data = file.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/css")
                self.end_headers()
                self.wfile.write(data.encode())
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
            self.send_response(200)
            global collection
            collection= collection.rebuild()
        elif self.path == "/play":
                self.resume_song()
        elif self.path.startswith("/play"):
            path = self.path.split("/")
            artist = unquote(path[2])
            song = unquote(path[3])
            self.play_song(artist, song)
        elif self.path.startswith("/add"):
            path = self.path.split("/")
            artist = unquote(path[2])
            song = unquote(path[3])
            self.add_song(artist, song)
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
        self.end_request()

    def standardResponse(self):
        with open("page.html") as page:
            data = page.read()
            self.send_response(200)
            self.wfile.write(data.encode())

    def send_artists(self):
        self.send_response(200)
        data = [x.name for x in collection.artists]
        encoder = json.JSONEncoder()
        data = encoder.encode(data)
        self.wfile.write(data.encode())

    def send_songs(self):
        seperated_path = self.path.split('/')
        artist = unquote(seperated_path[len(seperated_path)-1])
        artist = collection.get_artist(artist)
        songs = [x.name for x in artist.songs]
        encoder = json.JSONEncoder()
        songs = encoder.encode(songs)
        self.send_response(200)
        self.wfile.write(songs.encode())

    def play_song(self, artist, song):
        artist = collection.get_artist(artist)
        song = artist.find_song(song)
        music.stop()
        music.clearList()
        music.add_song(song.path)

    def add_song(self, artist, song):
        artist = collection.get_artist(artist)
        song = artist.find_song(song)
        music.add_song(song.path)

    def stop_song(self):
        music.stop()

    def pause_song(self):
        music.pause()

    def resume_song(self):
        music.play()

    def next_song(self):
        music.next()

    def end_request(self):
        self.send_response(200)
        self.wfile.write(b'1')

    def decrease_volume(self):
        music.decrease_volume()

    def increase_volume(self):
        music.increase_volume()

if __name__ == "__main__":
    print("starting server")
    server = HTTPServer((ADRESS, PORT), handler)
    server.serve_forever()