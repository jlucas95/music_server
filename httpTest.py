from http.server import HTTPServer, BaseHTTPRequestHandler
import collection_reader as cr
from player import Player
import json.encoder as json
from urllib.request import unquote
from cgi import parse_header, parse_multipart

__author__ = 'Jan'
ADRESS = ''
PORT = 8080

#TODO Disconnect pages from the handler. Maybe a module per page?
collection = cr.MusicCollection(cr.map_songs(cr.rootfolder))
print("collection built")

music = Player()


class handler(BaseHTTPRequestHandler):

    getDict = {
        "/artists": lambda self: self.send_artists(),
        "/albums": lambda self: self.send_albums(),
        "/songs": lambda self: self.send_songs(),
        "/": lambda self:  self.standard_response(),
        "/css": lambda self: self.send_css(),
        "/favicon.ico": lambda self: self.send_icon(),
        "/settings": lambda self: self.send_settings(),
        "/fonts": lambda self: self.send_etc(),
        "/js": lambda self: self.send_etc()
    }

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
            self.send_css()
        elif self.path.startswith("/favicon.ico"):
            self.send_icon()
        elif self.path.startswith("/settings"):
            self.send_settings()
        elif self.path.startswith("/fonts"):
            self.send_etc()
        elif self.path.startswith("/js"):
            self.send_etc()

    def do_POST(self):
        print('got post')

        if self.path.startswith("/settings"):
            self.song_upload()

    def do_PUT(self):
        if self.path == "/settings/rebuild":
            self.rebuild()
        elif self.path == "/play":
            self.resume_song()
        elif self.path.startswith("/songPlay"):
            self.play_song()
        elif self.path.startswith("/songAdd"):
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
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(data.encode())

    def send_css(self):
        path = self.path[1:len(self.path)]
        with open(path) as file:
            data = file.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/css")
            self.end_headers()
            self.wfile.write(data.encode())

    def send_icon(self):
        self.send_response(200)
        with open("favicon.ico", "rb") as icon:
            self.end_headers()
            self.wfile.write(icon.read())

    def send_settings(self):
        with open("settings.html") as file:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(file.read().encode())

    def send_etc(self):
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
        music.play()

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

    def song_upload(self):
        size = self.headers["Content-length"]
        self.send_response(200)
        self.wfile.write(b'0')
        postvars = self.parse_headers()
        song = postvars["song"][0]
        filename = postvars["filename"][0].decode('utf-8')
        file = open("music/"+ filename, mode='wb')

        file.write(song)
        file.close()
        self.rebuild()
        self.wfile.write(b'1')

    def parse_headers(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)
        else:
            postvars = {}
        return postvars

    @staticmethod
    def stop_song():
        music.stop()

    @staticmethod
    def pause_song():
        music.pause()

    @staticmethod
    def resume_song():
        music.play()

    @staticmethod
    def next_song():
        music.next()

    def end(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'1')

    @staticmethod
    def decrease_volume():
        music.decrease_volume()

    @staticmethod
    def increase_volume():
        music.increase_volume()

    def rebuild(self):
        collection.rebuild()

if __name__ == "__main__":
    print("starting server")
    server = HTTPServer((ADRESS, PORT), handler)
    server.serve_forever()
