import sys, pytube
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                                QLineEdit, QHBoxLayout, QVBoxLayout, QComboBox,
                                    QInputDialog, QFileDialog)
from PyQt5.QtGui import QMovie, QIcon
from PyQt5.QtCore import pyqtSlot, QThread


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

        #save as Button
        self.button1 = QPushButton('Save as', self)
        hbox1.addWidget(self.button1)

        self.button1.clicked.connect(self.save)
        #call function to get video info when search button pressed
        self.button.clicked.connect(self.getVideo)

        #drop down box
        self.dropDown = QComboBox(self)
        hbox_loading.addWidget(self.dropDown)
        self.dropDown.setHidden(True)

        #loading gif
        self.status_txt = QLabel()
        movie = QMovie("C:/Users/cgarc/Desktop/cst205/205git/cst205FinalProject/ajax-loader.gif")
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
        self.pytubeCallThread.finished.connect(self.finishedLoading)

    def finishedLoading(self, videos_list = ''):
        self.status_txt.setHidden(True)
        self.loading_label.setHidden(True)
        print('Finished loading')
        for x in videos_list:
            if x.type == 'video':
                self.dropDown.addItem(f'{x.type}: {x.subtype}\tresolution: {x.resolution}')
            else:
                self.dropDown.addItem(f'{x.type} bitrate: {x.abr}')
        self.dropDown.setHidden(False)

        for x in videos_list:
            print(x)

    def save(self):
        self.App()

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

class App(QWidget):

    def __init__(self):
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

        self.openFileNameDialog()
        self.openFileNamesDialog()
        self.saveFileDialog()

        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

app = QApplication(sys.argv)
main = MyWindow()
main.show()
sys.exit(app.exec_())