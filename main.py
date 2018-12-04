import sys, pytube
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                                QLineEdit, QHBoxLayout, QVBoxLayout, QComboBox)
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import pyqtSlot, QThread


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

        #loading gif
        self.status_txt = QLabel()
        movie = QMovie("C:/Users/cgarc/Desktop/cst205/205git/cst205FinalProject/ajax-loader.gif")
        self.status_txt.setMovie(movie)
        movie.start()
        self.status_txt.setHidden(True)
        hbox1.layout().addWidget(self.status_txt)

        self.loading_label =  QLabel()
        self.loading_label.setText("Loading")
        self.loading_label.setHidden(True)
        hbox1.layout().addWidget(self.loading_label)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def getVideo(self):
        self.pytubeCallThread = pytubeCallThread(self.yt_url.text())
        self.status_txt.setHidden(False)
        self.loading_label.setHidden(False)
        self.pytubeCallThread.start()
        self.pytubeCallThread.finished.connect(self.hideLoading)
    def hideLoading(self):
        self.status_txt.setHidden(True)
        self.loading_label.setHidden(True)

class pytubeCallThread(QThread):

    def __init__(self, url):
        QThread.__init__(self)
        self.url = url

    def __del__(self):
        self.wait()

    def run(self):
        self.yt = pytube.YouTube(self.url)
        print('Video')
        self.videos = self.yt.streams.all()
        for x in self.videos:
            print(x)
        print('Audio')
        #get only audio 
        self.audio = self.yt.streams.filter(only_audio=True).all()
        for x in self.audio:
            print(x)

app = QApplication(sys.argv)
main = MyWindow()
main.show()
sys.exit(app.exec_())
