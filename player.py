import mpv

class Player:
    def __init__(self):
        self.player = mpv.MPV()

    def play(self, video):
        self.player.play(video)
        self.player.wait_until_playing()
