import sys, pytube
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                                QLineEdit, QHBoxLayout, QVBoxLayout, QComboBox)
from PyQt5.QtCore import pyqtSlot


class MyWindow(QWidget):
    def __init__(self):

        super().__init__()

        hbox1 = QHBoxLayout()
        self.label1 = QLabel('Enter url: ')
        self.yt_url = QLineEdit()

        hbox1.addWidget(self.label1)
        hbox1.addWidget(self.yt_url)

        self.button = QPushButton('Search', self)
        hbox1.addWidget(self.button)

        #call function to get video info
        self.button.clicked.connect(self.getVideo)

        self.setLayout(hbox1)
        self.title = 'Audio/Video Downloader'
        self.left = 300
        self.top = 300
        self.width = 500
        self.height = 300
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def getVideo(self):
        self.yt = pytube.YouTube(self.yt_url.text())
        print('Video')
        self.videos = self.yt.streams.all()
        for x in self.videos:
            print(x)
        print('Audio')
        #to get only audio use
        self.audio = self.yt.streams.filter(only_audio=True).all()
        for x in self.audio:
            print(x)

app = QApplication(sys.argv)
main = MyWindow()
main.show()
sys.exit(app.exec_())
