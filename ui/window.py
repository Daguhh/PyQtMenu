#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Project desciption

@Author = Daguhh
"""

import sys
import os
from itertools import product
import sip

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

from parse_desktop_file import get_app_from_desktop, parse_desktop

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "PyQtMenu"
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

        # create tab
        self.table_widget = TabsContainer(parent=self)
        self.setCentralWidget(self.table_widget)

        self.show()


class TabsContainer(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.resize(600,400)

        # get all apps
        app_list = get_app_from_desktop()

        # Create tabs and give them a name
        categories = set([app['category'] for app in app_list])
        for category in categories:
            tab = Tab(category)
            name = category
            self.tabs.addTab(tab, name)

        # Fill tabs with apps with launchers
        for app in app_list:
            category = app['category']
            Tab.instances[category].addLauncher(app)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class Tab(QWidget):
    instances = {}

    def __init__(self, category):
        super(QWidget, self).__init__()
        self.setAcceptDrops(True)

        self.category = category
        self.layout = QGridLayout(self)
        Tab.instances[category] = self
        self.launcher_list = []
        self.shape = (3,3)
        self.gen_position = self.genPos()

    def addLauncher(self, app):
        app['button'] = AppLauncherBtn(self.layout, app, next(self.gen_position))
        self.launcher_list += [app]

    def genPos(self, shape=(3,3)):
        self.shape = shape
        i = 0
        while i < shape[0] * shape[1]:
            x = i//shape[0]
            y = i%shape[0]
            #print(f'position : {x},{y}')
            yield (x, y)
            i += 1

    def resizeEvent(self, event):

        button_size = (120,180)

        buttons_space_x = (button_size[0] + 10) * self.shape[0]
        tab_x = self.size().width()

        x = tab_x // (button_size[0] + 10)
        y = self.shape[1]
        if self.shape != (x,y):
            self.gen_position = self.genPos((x, y))
            for app in self.launcher_list:
                self.layout.removeItem(app['button'].layout)
            for app in self.launcher_list:
                x, y = next(self.gen_position)
                self.layout.addWidget(app['button'], x, y)

    def dragEnterEvent(self, e):
        print('drag')
        if e.mimeData().hasFormat("text/uri-list"):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        file_path = e.mimeData().text().split('//')[1:][0]
        app = parse_desktop(file_path)
        file_name = file_path.split('/')[-1]
        os.system(f'cp {file_path} Apps/{self.category}/{file_name}')
        self.addLauncher(app)


class AppLauncherBtn(QWidget):

    def __init__(self, parent_tab, app, pos):

        super(QWidget, self).__init__()

        self.layout = QVBoxLayout(self)
        #layout.SetFixedSize = 120, 100
        self.setFixedSize(120,180)

        name = app['Name'] # 'qrcopy'
        icon = app['Icon'] # 'qrcode.png'
        tooltip = app['Comment'] #'generate a qr code'

        btn = QPushButton('')
        btn.setIcon(QIcon(QPixmap(icon)))
        btn.setIconSize(QSize(100, 100))
        self.layout.addWidget(btn)
        btn.setToolTip(tooltip)
        btn.clicked.connect(app['Exec'])

        txt = QLabel(name)
        txt.setAlignment(Qt.AlignHCenter)
        self.layout.addWidget(txt)

        self.setLayout(self.layout)

        parent_tab.addWidget(self, *pos)

    def remove(self):
        self.layout.removeWidget(self.widget_name)
        sip.delete(self.widget_name)
        self.widget_name = None

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

