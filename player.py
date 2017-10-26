import vlc
import threading
import time
from multiprocessing import Queue
__author__ = 'Jan'


class Player:
    def __init__(self):

        self.playing = False
        self.mediaList = vlc.MediaList()
        self.player = vlc.MediaPlayer()
        self.list_player = vlc.MediaListPlayer()
        self.list_player.set_media_list(self.mediaList)
        self.list_player.set_media_player(self.player)
        self.level = 80
        self.volume_interval = 5
        self.pipe = self.monitor()

    def clearList(self):
        self.mediaList = vlc.MediaList()
        self.player = vlc.MediaPlayer()
        self.set_volume(self.level)
        self.list_player = vlc.MediaListPlayer()
        self.list_player.set_media_list(self.mediaList)
        self.list_player.set_media_player(self.player)

    def add_song(self, song_path):
        song = vlc.Media(song_path)
        self.mediaList.add_media(song)

    def play(self):
        self.playing = True
        self.list_player.play()

    def pause(self):
        self.list_player.pause()
        self.playing = False

    def stop(self):
        self.list_player.stop()
        self.playing = False

    def next(self):
        self.list_player.next()


    def get_volume(self):
        return self.player.audio_get_volume()

    def set_volume(self, level):
        self.player.audio_set_volume(level)

    def set_volume_interval(self, interval):
        self.volume_interval = interval

    def increase_volume(self):
        self.level += self.volume_interval
        self.set_volume(self.level)

    def decrease_volume(self):
        self.level -= self.volume_interval
        self.set_volume(self.level)

    def _check(self):
        current_song = self.player.get_media()
        while True:
            time.sleep(1)
            if self.player.get_media() != current_song:
                self.pipe.put("1")
                current_song = self.player.get_media()

    def monitor(self):
        thread = threading.Thread(target=self._check, daemon=True,)
        thread.start()
        return Queue()


if __name__ == "__main__":
    a = Player()
    print("made object")
    a.add_song("music/Aqualung.mp3")
    print("added a song")
    a.add_song("music/12 Shimi.mp3")
    print("added another")
    a.next()
    print(a.pipe.get(timeout=3))


