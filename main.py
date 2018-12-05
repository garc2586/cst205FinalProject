import sys, pytube
from PyQt5 import QtCore
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
        #set up thread to get video and pass url
        self.pytubeCallThread = pytubeCallThread(self.yt_url.text())
        self.pytubeCallThread.videos_signal.connect(self.finishedLoading)
        #show loading gif and text
        self.status_txt.setHidden(False)
        self.loading_label.setHidden(False)

        #start thread
        self.pytubeCallThread.start()

        #hide loading gif/text when thread is done
        self.pytubeCallThread.finished.connect(self.finishedLoading)

    def finishedLoading(self, videos_list = ''):
        self.status_txt.setHidden(True)
        self.loading_label.setHidden(True)
        print('Finished loading')

        for x in videos_list:
            print(x)




class pytubeCallThread(QThread):

    videos_signal = QtCore.pyqtSignal(list)
    def __init__(self, url):
        QThread.__init__(self)
        self.url = url

    def __del__(self):
        self.wait()

    def run(self):
        self.yt = pytube.YouTube(self.url)
        print('Got the Videos')
        self.videos = self.yt.streams.all()

        #emit signal with video list
        self.videos_signal.emit(self.videos)

app = QApplication(sys.argv)
main = MyWindow()
main.show()
sys.exit(app.exec_())
