import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import socket
import struct
import threading
import time
import random
import os, time, sys
from evaluate import evaluate
from receive_process import MulticastReceiveProcess


class filedialogdemo(QWidget):

    def __init__(self, parent=None):
        super(filedialogdemo, self).__init__(parent)
        layout = QVBoxLayout()

        self.btn = QPushButton()
        self.btn.clicked.connect(self.loadFile)
        self.btn.setText("从文件中获取照片")
        layout.addWidget(self.btn)

        self.label = QLabel()
        layout.addWidget(self.label)

        self.btn_2 = QPushButton()
        self.btn_2.clicked.connect(self.load_text)
        self.btn_2.setText("加载电脑文本文件")
        layout.addWidget(self.btn_2)

        self.content = QTextEdit()
        layout.addWidget(self.content)
        self.setWindowTitle("测试")

        self.setLayout(layout)

    def loadFile(self):
        multicast_receive_process = MulticastReceiveProcess()
        multicast_receive_process.run()
        # print("load--file")
        # fname, _ = QFileDialog.getOpenFileName(self, '选择图片', 'c:\\', 'Image files(*.jpg *.gif *.png)')
        # self.label.setPixmap(QPixmap(fname))

    def load_text(self, txt):
        pipe_name = 'pipe_test'
        if not os.path.exists(pipe_name):
            os.mkfifo(pipe_name)
            
        print("xxx1")
        pipein = open(pipe_name, os.O_RDONLY | os.O_NONBLOCK)
        print("xxx2")
        while True:
            line = pipein.readlines()
            print("reading", line)
            self.content.setText(line)
        '''
        print("load--text")
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setFilter(QDir.Files)
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            f = open(filenames[0], 'r')
            with f:
                data = f.read()
                self.content.setText(data)
        '''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fileload = filedialogdemo()
    fileload.show()
    sys.exit(app.exec_())

