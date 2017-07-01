from mutagen.mp3 import MP3
import vlc
import time
import os


class MediaPlayer(object):
    def __init__(self):
        self.instance = None
        self.player = None

    def create_vlc_connection(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

    def set_media(self, filename):
        media = self.instance.media_new(filename)
        self.player.set_media(media)

    def get_song_length(self, filename):
        audio = MP3(filename)
        return int(audio.info.length) + 3

    def play(self):
        self.create_vlc_connection()
        os.chdir('./media')
        for filename in os.listdir('.'):
            self.set_media(filename)
            song_length = self.get_song_length(filename)
            self.player.play()
            print "Playing %s for %s secs" % (filename, song_length)
            time.sleep(song_length)
