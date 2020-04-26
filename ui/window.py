#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
maid by Daguhh
on 04/2020
Main description
"""

import sys
import os

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QTabWidget,
    QHBoxLayout,
    QVBoxLayout,
    QAction,
    QLabel,
    QApplication,
    QPushButton,
    QLabel,
    QGridLayout,
    QTextEdit
)
from PyQt5.QtGui import QPixmap, QIcon



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "DaguhhMenu"
        self.setWindowTitle(self.title)

        self.initUI()

    def initUI(self):

        exitAct = QAction(text='&Exit', parent=self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(QApplication.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        # tab
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()

class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,200)

        # Add tabs
        self.tabs.addTab(self.tab1,"Tab 1")
        self.tabs.addTab(self.tab2,"Tab 2")

        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.btn = QPushButton('')
        self.btn.setIcon(QIcon(QPixmap("qrcode.png")))
# adjust width and height to fit the size of button.
        self.btn.setIconSize(QSize(100, 100))
# set zero border.
        #self.btn.setStyleSheet('QPushButton{border: 0px solid;}')
        #self.pushButton1 = QPushButton(QIcon("qrcode.png"),"PyQt5 button",self)
        self.tab1.layout.addWidget(self.btn)
        self.tab1.setLayout(self.tab1.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)

        self.setLayout(self.layout)

#    @pyqtSlot()
#    def on_click(self):
#        print("\n")
#        for currentQTableWidgetItem in self.tableWidget.selectedItems():
#            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

