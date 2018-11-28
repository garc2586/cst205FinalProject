import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                                QLineEdit, QHBoxLayout, QVBoxLayout, QComboBox)
from PyQt5.QtCore import pyqtSlot


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        hbox1 = QHBoxLayout()
        self.label1 = QLabel('Enter url: ')
        self.line_edit = QLineEdit()

        hbox1.addWidget(self.label1)
        hbox1.addWidget(self.line_edit)

        self.button = QPushButton('Search', self)
        hbox1.addWidget(self.button)

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

app = QApplication(sys.argv)
main = MyWindow()
main.show()
sys.exit(app.exec_())
