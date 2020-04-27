#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Project desciption
"""

__author__ = "Daguhh"
__copyright__ = "Copyright 2020, The Daguhh Project"
__credits__ = ["Daguhh"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Daguhh"
__email__ = "daguhh@daguhh.fr"
__status__ = "Production"

import sys
import os
from itertools import product

from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QSpacerItem,
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
from PyQt5.QtGui import QPixmap, QIcon, QStaticText

from parse_desktop_file import get_app_from_desktop # parse_desktop

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
        #grid = QGridLayout()
        self.setLayout(self.layout)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.resize(300,200)

        # Create first tab
        app_list = get_app_from_desktop()


        category_tab_dct = {}
        for i, app in enumerate(app_list):
            category = app['category']
            if not category in category_tab_dct.keys():
                new_tab = QWidget()
                new_tab.layout = QGridLayout(self)
                category_tab_dct[app['category']] = new_tab
                self.tabs.addTab(new_tab, app['category'])
            btn = AppLauncherBtn(category_tab_dct[category].layout, app, (1,i))

        #self.tab1.setLayout(self.tab1.layout)
        for tab in category_tab_dct.values():
            tab.setLayout(tab.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

class AppLauncherBtn(QWidget):

    def __init__(self, parent_tab, app, pos):

        super(QWidget, self).__init__()

        layout = QVBoxLayout(self)
        #layout.SetFixedSize = 120, 100
        self.setFixedSize(120,180)

        name = app['Name'] # 'qrcopy'
        icon = app['Icon'] # 'qrcode.png'
        tooltip = app['Comment'] #'generate a qr code'

        btn = QPushButton('')
        btn.setIcon(QIcon(QPixmap(icon)))
        btn.setIconSize(QSize(100, 100))
        layout.addWidget(btn)
        btn.setToolTip(tooltip)
        btn.clicked.connect(app['Exec'])

        txt = QLabel(name)
        txt.setAlignment(Qt.AlignHCenter)
        layout.addWidget(txt)

        self.setLayout(layout)

        parent_tab.addWidget(self, *pos)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

