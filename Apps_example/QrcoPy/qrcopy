#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

In this example, we dispay an image
on the window.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""

import sys
import os

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QApplication,
    QPushButton,
    QLabel,
    QGridLayout,
    QTextEdit
)
from PyQt5.QtGui import QPixmap
import qrcode
from PIL.ImageQt import ImageQt

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        grid = QGridLayout()

        textqr = QLabel('Enter text to convert')
        self.textboxqr = QTextEdit()
        grid.addWidget(textqr, 1, 6)
        grid.addWidget(self.textboxqr, 2, 6)

        pixmap = QPixmap(200,200)
        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        grid.addWidget(self.label, 0, 0, 5, 5)
        #grid.addItem(pixmap,1,0,4,4)

        btn = QPushButton('Generate', self)
        btn.setToolTip('Generate qr code from text')
        btn.clicked.connect(self.generate)
        grid.addWidget(btn,3,6)

        self.setLayout(grid)
        self.setGeometry(300, 300, 350, 200)
        self.setWindowTitle('Generate QRcodes')
        self.show()

    def generate(self):
        text = self.textboxqr.toPlainText()
        img = qrcode.make(text)
        qim = ImageQt(img)
        pixmap = QPixmap.fromImage(qim)
        self.label.setPixmap(pixmap)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
