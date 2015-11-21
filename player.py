import vlc
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

    def clearList(self):
        self.mediaList = vlc.MediaList()
        self.player = vlc.MediaPlayer()
        self.list_player = vlc.MediaListPlayer()
        self.list_player.set_media_list(self.mediaList)
        self.list_player.set_media_player(self.player)

    def add_song(self, song_path):
        song = vlc.Media(song_path)
        self.mediaList.add_media(song)
        if self.mediaList.count() == 1:
            self.play()

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







