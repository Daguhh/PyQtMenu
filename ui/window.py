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
    QInputDialog,
    QDialog,
    QLineEdit,
    QSpacerItem,
    QMainWindow,
    QScrollArea,
    QWidget,
    QTabWidget,
    QHBoxLayout,
    QVBoxLayout,
    QAction,
    QLabel,
    QApplication,
    QPushButton,
    QGridLayout,
    QTextEdit
)
from PyQt5.QtGui import QPixmap, QIcon, QStaticText

from .parse_desktop_file import get_app_from_desktop, parse_desktop_lang

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

        resizeiconAct = QAction(text='&Resize Icons', parent=self)
        resizeiconAct.triggered.connect(self.resize_icons)
        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        fileMenu.addAction(resizeiconAct)

        # create tab
        self.table_widget = TabsContainer(parent=self)
        self.setCentralWidget(self.table_widget)

        self.show()

    def get_size_value(self, *args):
        dialog = AskMultipleValues(*args)
        #dialog.exec_()
        if dialog.exec_():
            vals = dialog.get_values()
        else:
            vals = dialog.cancel()
        return vals

    def resize_icons(self):
        x, y, test = self.get_size_value('x','y')
        x, y = int(x), int(y)
        if test:
            for launcher in AppLauncherBtn.instances.values():
                launcher.resize_icons(x, y)
            for tab in Tab.instances.values():
                tab.setMinimumWidth(int(x)+20)

class AskMultipleValues(QDialog):

    def __init__(self, *args, **kwargs):
        super(QDialog, self).__init__()
        self.layout = QGridLayout(self) #QVBoxLayout(self)
        self.textEdits = []
        for i, item in enumerate(args):
            text = QLabel(item)
            textEdit = QLineEdit()
            self.textEdits.append(textEdit)
            self.layout.addWidget(text, i, 0)
            self.layout.addWidget(textEdit, i, 1, 1, 2)

        ok_btn = QPushButton("Ok")
        ok_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)

        self.layout.addWidget(cancel_btn, i+1, 1)
        self.layout.addWidget(ok_btn, i+1, 2)

    def get_values(self):
        vals = []
        for textEdit in self.textEdits:
            vals.append(textEdit.text())

        return *vals, True

    def cancel(self):
        return 0, 0, False


class TabsContainer(QWidget):
    """
    A container (Qwidget) to hold all category tabs
    at call it loops over desktop files, create new category tab,
    and fill them with launcher for apps
    """

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
            tab = ScrollTab(category)
            name = category
            self.tabs.addTab(tab, name)

        # Fill tabs with apps with launchers
        for app in app_list:
            category = app['category']
            Tab.instances[category].addLauncher(app)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

class ScrollTab(QScrollArea):
    """
    Make tab vertically scrollable
    """

    def __init__(self, category):

        super(QScrollArea, self).__init__()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.widget = Tab(category)
        self.setWidget(self.widget)

class Tab(QWidget):
    """
    A tab for each category,
    support .desktop files dropEvent
    laucnhers are display on a grid that reshapes on window resizeEvent
    """
    instances = {}

    def __init__(self, category):
        """ Create an empty tab """
        super(QWidget, self).__init__()

        self.setAcceptDrops(True)

        # max launcher in 1 Tab

        # keep track of all created categories
        self.category = category
        Tab.instances[category] = self

        # keep track of launchers
        self.launcher_list = []

        # Init gris, its shape and a generator to fill it
        self.layout = QGridLayout(self)
        #self.shape = (3,5) # 3x3 squares
        self.width = 3
        self.max_launcher = 12
        self.gen_position = self.genPos()

        self.launcher_size = (100,100)

        self.setMinimumWidth((self.launcher_size[0]*1.3))

    def addLauncher(self, app):
        """ create a button to launch app, store it as "button" key"""

        app['button'] = AppLauncherBtn(self.layout,
                                       app,
                                       next(self.gen_position),
                                       size = self.launcher_size)
        self.launcher_list += [app]



    def genPos(self):
        """
        Create a generator that return positions,
        line by line, to fill a 2-dimensions grid
        args:
            shape(tuple) : (x,y) dimensions of the array to fill
        return:
            generator
        """

        i = 0
        print('==================')
        print(self.category)
        while i <= self.max_launcher: #shape[0] * shape[1]:
            print(i)
            #print(shape)
            x = i//self.width
            y = i%self.width
            print(x, y)
            yield (x, y)
            i += 1

    def resizeEvent(self, event):
        """ Modify grid shape as window is resized """

        #button_size = (60, 70)

        #buttons_space_x = (button_size[0] + 10) * self.shape[0]
        tab_x = self.size().width()

        new_width = tab_x // self.launcher_size[0]
        if self.width != new_width:
            self.width = new_width
            self.refresh()

    def refresh(self):

        self.gen_position = self.genPos()

        for app in self.launcher_list:
            self.layout.removeItem(app['button'].layout)
        for app in self.launcher_list:
            x, y = next(self.gen_position)
            self.layout.addWidget(app['button'], x, y)

    def dragEnterEvent(self, e):
        """ A useless method """
        print('drag')
        if e.mimeData().hasFormat("text/uri-list"):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        """ As desktop file is dropped on a tab, create a new launcher """
        file_path = e.mimeData().text().split('//')[1:][0]
        app = parse_desktop_lang(file_path)
        file_name = file_path.split('/')[-1]
        os.system(f'cp {file_path} Apps/{self.category}/{file_name}')
        self.addLauncher(app)


class AppLauncherBtn(QWidget):
    instances = {}

    def __init__(self, parent_tab, app, pos, size):

        super(QWidget, self).__init__()

        self.layout = QVBoxLayout(self)
        self.size = size
        #layout.SetFixedSize = 120, 100
        self.icon_size = (int(size[0]), int(size[1]))
        self.setFixedSize(size[0]+20, size[1]+35)


        name = app['Name'] # 'qrcopy'
        icon = app['Icon'] # 'qrcode.png'
        tooltip = app['Comment'] #'generate a qr code'

        self.btn = QPushButton('')
        self.btn.setIcon(QIcon(QPixmap(icon)))
        self.btn.setIconSize(QSize(*self.icon_size))
        self.layout.addWidget(self.btn)
        self.btn.setToolTip(tooltip)
        self.btn.clicked.connect(app['Exec'])

        txt = QLabel(name)
        txt.setAlignment(Qt.AlignHCenter)
        self.layout.addWidget(txt)

        self.setLayout(self.layout)

        parent_tab.addWidget(self, *pos)

        AppLauncherBtn.instances[name] = self

    def remove(self):
        self.layout.removeWidget(self.widget_name)
        sip.delete(self.widget_name)
        self.widget_name = None

    def resize_icons(self, size_x, size_y):
        self.setFixedSize(size_x+20, size_y+35)
        self.btn.setIconSize(QSize(size_x, size_y))

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

