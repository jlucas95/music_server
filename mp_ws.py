__author__ = 'Jan'
from wsgiref.simple_server import make_server
from ws4py.websocket import WebSocket
from ws4py.server.wsgirefserver import WSGIServer, WebSocketWSGIRequestHandler
from ws4py.server.wsgiutils import WebSocketWSGIApplication
from json import decoder, encoder
from player import Player
from threading import Thread

player = Player()
class Handler(WebSocket):
    def __init__(self):
        super(WebSocket, self).__init__()


    def send_song_update(self):

        self.send()

    def received_message(self, message):
        print(message)
        message = self.convert_input(message)
        self.handle(message)

    def convert_input(self, data):
        json_decoder = decoder.JSONDecoder()
        data = json_decoder.decode(str(data))
        return data

    def handle(self, message):
        if message["page"] == "music":
            command = message["command"]
            if command == "play":




if __name__ == "__main__":
    server = make_server('', 9000, server_class=WSGIServer,
                         handler_class=WebSocketWSGIRequestHandler,
                         app=WebSocketWSGIApplication(handler_cls=Handler))
    server.initialize_websockets_manager()
    server.serve_forever()
