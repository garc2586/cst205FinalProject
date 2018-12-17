import sys, pytube
import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                                QLineEdit, QHBoxLayout, QVBoxLayout, QComboBox,
                                    QInputDialog, QFileDialog)
from PyQt5.QtGui import QMovie, QIcon
from PyQt5.QtCore import pyqtSlot, QThread


#used for filters
filters = [ "Choose Filter: default", "sepia", "negative", "grayscale", "flip video"]
class MyWindow(QWidget):
    def __init__(self):

        super().__init__()

        #vertical box layout
        vbox = QVBoxLayout()

        #horizontal box layouts
        hbox1 = QHBoxLayout()
        hbox_loading = QHBoxLayout()

        #url input
        self.label1 = QLabel('Enter url: ')
        self.yt_url = QLineEdit()
        hbox1.addWidget(self.label1)
        hbox1.addWidget(self.yt_url)

        #search button
        self.button = QPushButton('Search', self)
        hbox1.addWidget(self.button)

        #drop down box
        self.dropDown = QComboBox(self)
        hbox_loading.addWidget(self.dropDown)
        self.dropDown.setHidden(True)

        #filter box
        self.filter_box = QComboBox()
        self.filter_box.addItems(filters)
        self.filter_box.setHidden(True)
        hbox_loading.addWidget(self.filter_box)

        #save as Button
        self.button1 = QPushButton('Save as', self)
        hbox_loading.addWidget(self.button1)
        self.button1.setHidden(True)

        #call save function when save button clicked
        self.button1.clicked.connect(self.save)
        #call function to get video info when search button pressed
        self.button.clicked.connect(self.getVideo)

        #loading gif
        self.status_txt = QLabel()
        movie = QMovie("/cst205FinalProject/ajax-loader.gif")
        self.status_txt.setMovie(movie)
        movie.start()
        self.status_txt.setHidden(True)
        hbox_loading.addWidget(self.status_txt)
        #loading label in case loading gif doesent load
        self.loading_label =  QLabel()
        self.loading_label.setText("Loading")
        self.loading_label.setHidden(True)
        hbox_loading.addWidget(self.loading_label)

        #add vertical layouts to horisontal layout
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox_loading)

        #define UI layout and window size
        self.setLayout(vbox)
        self.title = 'Audio/Video Downloader'
        self.left = 300
        self.top = 300
        self.width = 500
        self.height = 300
        self.initUI()

    #starts up the UI
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    #called when the search button is pressed
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
        self.pytubeCallThread.finished.connect(self.hideLoadingGif)


    def hideLoadingGif(self):
        self.status_txt.setHidden(True)
        self.loading_label.setHidden(True)
        self.button1.setHidden(False)

    def finishedLoading(self, videos_list = ''):
        self.videos_list = videos_list
        self.itags = []
        print('Finished loading')

        for x in videos_list:
            if x.type == 'video':
                self.dropDown.addItem(f'{x.type}: {x.subtype}\tresolution: {x.resolution}')
            else:
                self.dropDown.addItem(f'{x.type} bitrate: {x.abr}')
            self.itags.append(x.itag)
        self.dropDown.setHidden(False)
        self.filter_box.setHidden(False)

        for x in videos_list:
            print(x)

    #fucntion when we want to save a file
        print('current index: '+ str(self.dropDown.currentIndex()))
        print('current size of itags'+str(len(self.itags)))
    def save(self):
        newSaveWindow = SaveWindow(self.dropDown.currentIndex(), self.videos_list)
        newSaveWindow.show()
        
class pytubeCallThread(QThread):
    #signal that emits when the videos list are obtained
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

#window that opens to let users choose save location
class SaveWindow(QWidget):

    def __init__(self, pytube_index, videos_list):
        self.pytube_index = pytube_index
        self.videos_list = videos_list
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.saveFileDialog()
        self.show()

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Save Location","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

        print(self.pytube_index)
        #splits file location and name by / so that the program can separate save path and file name
        split_fileName = fileName.split('/')
        #last_word is the name of the file
        last_word = split_fileName[-1]
        #out path is the path where the file will be saved
        out_path = fileName[0: len(fileName) - len(last_word)]
        #temp: to check if this worked
        print(f"...{out_path}...")
        print(f"...{last_word}...")
        #using pytube download function to define output path and filename
        self.videos_list[self.pytube_index].download(output_path = out_path, filename = last_word)

app = QApplication(sys.argv)
main = MyWindow()
main.show()
sys.exit(app.exec_())
