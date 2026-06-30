#!/usr/bin/env python3
import mpv
import os
from player import Player

COMMERCIAL_DIR = 'library/commercials/'

# player = Player()
path = COMMERCIAL_DIR + '2000s_commercials_nostalgia.mp4'
print(os.path.exists(path))
player = mpv.MPV(vo='libmpv', input_vo_keyboard=True, log_handler=print, loglevel='error')
player.play(path)
player.wait_for_playback()
