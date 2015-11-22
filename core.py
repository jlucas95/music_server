import collection_reader as cr
import player
__author__ = 'Jan'
import os

print(os.getcwd())

music = player.Player()


song = cr.Song('music/02 Free Will Sacrifice.mp3')
music.add_song(song.path)
print("playing")
music.play()
input()