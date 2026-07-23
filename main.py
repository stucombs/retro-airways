#! /usr/bin/env python3
"""
A simple Media Player using MPV and Pyside6
"""
import glob
import locale
import mpv as mpv
import os
import random
import sys
import subprocess

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

SHOWS_DIR='library/shows/'
COMMERCIAL_DIR='library/commercials/'
MUSIC_VIDEO_DIR='library/music_videos'

class RetroPlayer(QMainWindow):
    def __init__(self, parent=None):
        return
        # super().__init__(parent)
        # self.setWindowTitle("Retro MTV Player")
        # self.createWindow()
        # self.show()
        # self.initPlayer() 

    def initPlayer(self):
        wid = int(self.container.winId())
        print(f"Window ID: {wid}")
        print(f"Container visible: {self.container.isVisible()}")
        self.player = mpv.MPV(
            wid=str(wid),
            input_default_bindings=True,
            input_vo_keyboard=True,
            osc=True,
            hwdec='no',
            force_window=True,
            log_handler=print,
            loglevel="debug"
        )

    def createWindow(self):
        """Set up the user interface"""
        self.container = QWidget(self)
        self.setCentralWidget(self.container)
        self.container.setAttribute(Qt.WA_DontCreateNativeAncestors)
        self.container.setAttribute(Qt.WA_NativeWindow)

        self.container.setFocusPolicy(Qt.StrongFocus)
        self.container.setFocus()

    def play(self, path):
        if os.path.exists(path):
            self.player.play(path)
        else:
            print(f'Path does not exists {path}')
        

    """
        Temp subprocess route for running MPV until figure out mpv working on mac
    """
    def play_file(self, path):
        subprocess.run([
            'mpv',
            '--really-quiet',
            path
        ])

class Scheduler():
    def __init__(self):
        self.schedule = None

    def listDirNoHidden(self, path):
        return glob.glob(os.path.join(path, '*'))

    def getRandomShow(self):
        """Selects a random show from library/shows"""
        show = random.choice(self.listDirNoHidden(SHOWS_DIR))
        season = random.choice(self.listDirNoHidden(show))
        episode = random.choice(self.listDirNoHidden(season))

        return episode
    
    def getRandomCommercial(self):
        return random.choice(self.listDirNoHidden(COMMERCIAL_DIR))

    def getShowSeasonEpisode(self, showPath):
        fileName = showPath.replace('library/shows/', '')
        fileName = fileName.split('/')

        show = fileName[0]
        
        episode = fileName[-1]
        episode = episode.replace('.mp4', '')

        return show, episode

    def getCommercialName(self, commPath):
        commPath = commPath.split('/')
        commPath = commPath[-1]

        return commPath.replace('.mp4', '')
    
    def runChannel(self, player):
        """
            Run channel
            player: RetroPlayer
        """

        while True:
            episode = self.getRandomShow()
            showName, episodeName = self.getShowSeasonEpisode(episode)
            print(f"Now Playing: {showName} {episodeName}")

            player.play_file(episode)

            for _ in range(3):
                commercial = self.getRandomCommercial()
                commercialName = self.getCommercialName(commercial)
                print(f"Taking a break with: {commercialName}")
                player.play_file(commercial)

if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # locale.setlocale(locale.LC_NUMERIC, "C")

    player = RetroPlayer()
    # player.resize(1280, 720)

    scheduler = Scheduler()
    scheduler.runChannel(player)

    # sys.exit(app.exec())
