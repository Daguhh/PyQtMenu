#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Project desciption

@Author = Daguhh
"""

import sys
import os
from itertools import product, count
import sip
import subprocess

from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QFont #QStaticText, QColor,
from PyQt5.QtCore import QThreadPool, QRunnable, pyqtSlot
from PyQt5.QtWidgets import (
    #QInputDialog,
    QDialog,
    #QLineEdit,
    #QSpacerItem,
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
    #QTextEdit,
    #QDesktopWidget,
    QSizePolicy,
    QGraphicsOpacityEffect,
    #QListWidgetItem,
    QFrame,
    QCheckBox,
)

from .parse_desktop_file import get_app_from_desktop, parse_desktop_lang
from .qss import APP_BUTTON_QSS, APP_LABEL_QSS, APP_LAUNCHER_QSS
from .layout_manager.layout_manager_tab import LayoutMgr
from .dialogs import AskMultipleValues


class MainWindow(QMainWindow):

    # bigpicture = True
    instance = None

    def __init__(self):
        super().__init__()
        self.title = "PyQtMenu"
        self.setWindowTitle(self.title)
        self.isSplit = False
        #        self.setStyleSheet("""
        # """)
        # self.setMouseTracking(True)
        MainWindow.instance = self

        self.initUI()

    def initUI(self):

        ######## Status bar ###########
        self.statusBar()

        ######## Menubar ############
        exitAct = QAction(text="&Exit", parent=self)
        exitAct.setShortcut("Ctrl+Q")
        exitAct.setStatusTip("Exit application")
        exitAct.triggered.connect(QApplication.quit)

        resizeiconAct = QAction(text="&Resize Icons", parent=self)
        resizeiconAct.triggered.connect(self.resize_icons)

        self.reducemodAct = QAction("Masquer", self, checkable=True)
        self.reducemodAct.setStatusTip(
            "Réduit le menu au lancement d'une application"
        )
        self.reducemodAct.setChecked(True)

        menubar = self.menuBar()

        fileMenu = menubar.addMenu("&Fichier")
        fileMenu.addAction(exitAct)

        EditMenu = menubar.addMenu("&Edition")
        EditMenu.addAction(resizeiconAct)
        EditMenu.addAction(self.reducemodAct)

        ######## control panel ############
        window = QWidget()
        self.setCentralWidget(window)

        reduceBtn = QPushButton("M")
        reduceBtn.setFixedSize(100, 100)
        reduceBtn.setToolTip("Réduire le menu")
        reduceBtn.setFont(QFont("Times", 80))
        reduceBtn.clicked.connect(MainWindow.reduce_mainwindow)

#        splitBtn = QPushButton("Split")
#        splitBtn.setToolTip("place les fenêtres côte à cote à la verticale")
#        splitBtn.clicked.connect(self.toogle_layout)
#
#        twopanelBtn = QPushButton("2 panel")
#        twopanelBtn.setToolTip("dispose les fenêtes sous forme de deux panneaux")

        self.twopanelCb = QCheckBox("Vue à deux panneaux")
        self.twopanelCb.setToolTip(
            "Disposer les fenêtres en deux panneaux séparées verticalement"
        )
        self.twopanelCb.setChecked(False)
        self.twopanelCb.stateChanged.connect(self.toogle_layout)

        self.reduceCb = QCheckBox("Réduire le menu")
        self.reduceCb.setToolTip(
            "Réduire le menu au lancement d'une application"
        )
        self.reduceCb.setChecked(True)
        #self.reduceCb.stateChanged.connect(self.)

        hbox = QHBoxLayout()
        hbox.addWidget(reduceBtn)
        hbox.addWidget(self.twopanelCb)
        hbox.addWidget(self.reduceCb)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        window.setLayout(vbox)

        ########### Tabs launchers ####################
        # create tab
        self.table_widget = TabsContainer(parent=self)
        self.layout_mgr = LayoutMgr()
        self.table_widget.addtabmodule(self.layout_mgr, "layout")

        self.twopanelCb.stateChanged.connect(self.layout_mgr.refresh)
        vbox.addWidget(self.table_widget)

        self.show()

    def toogle_layout(self):
        if self.isSplit:
            os.system("""i3-msg "layout tabbed" """)
        else:
            os.system("""i3-msg "layout splith" """)
        self.isSplit = not self.isSplit

    def get_size_value(self, *args):
        dialog = AskMultipleValues(*args)
        if dialog.exec_():
            vals = dialog.get_values()
        else:
            vals = dialog.cancel()
        return vals

    @classmethod
    def reduce_mainwindow(cls):
        if cls.instance.reduceCb.isChecked() == False:
            return
        dialog = ReduceModButton()
        MainWindow.instance.hide()
        if dialog.exec_():
            vals = dialog.accept()
            cls.instance.show()
        else:
            QApplication.quit()
        return

    def resize_icons(self):
        x, y, test = self.get_size_value("x", "y")
        x, y = int(x), int(y)
        if test:
            for launcher in AppLauncherBtn.instances.values():
                launcher.resize_icons(x, y)
            for tab in Tab.instances.values():
                tab.launcher_size = (x, y)
                tab.setMinimumWidth(int(x) + 20)


class ReduceModButton(QDialog):
    """ button that reopen main window """

    def __init__(self):

        super(QDialog, self).__init__()
        self.layout = QGridLayout(self)  # QVBoxLayout(self)

        reopen_button = QPushButton("M")
        reopen_button.setGeometry(0, 0, 100, 100)
        reopen_button.setStatusTip("Afficher le menu en plein écran")
        reopen_button.clicked.connect(self.accept)

        self.setGeometry(0, 0, 150, 150)

        dialog_size = self.geometry().getRect()
        desktop_size = QApplication.desktop().screenGeometry().getRect()

        *_, x, y = map(lambda x, y: y - x - 30, dialog_size, desktop_size)
        self.move(x, y)

        reopen_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        reopen_button.setStyleSheet("background-color:rgba(55,55,55,15);")
        reopen_button.setFont(QFont("Times", 48))

        self.layout.addWidget(reopen_button)
        op = QGraphicsOpacityEffect(self)
        op.setOpacity(0.5)  # 0 to 1 will cause the fade effect to kick in
        self.setGraphicsEffect(op)
        self.setAutoFillBackground(True)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)



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
        self.tabs.resize(600, 400)

        # get all apps
        app_list = get_app_from_desktop()

        # Create tabs and give them a name
        categories = set([app["category"] for app in app_list])
        for category in categories:
            tab = ScrollTab(category)
            name = category
            self.tabs.addTab(tab, name)

        # add module tab
        #self.addtabmodule()

        # Fill tabs with apps with launchers
        for app in app_list:
            category = app["category"]
            Tab.instances[category].addLauncher(app)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def addtabmodule(self, module, tab_name):

        # add a tab for layout management (i3module)
        #self.modules.append(module())
        self.tabs.addTab(module, tab_name)


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
        # self.shape = (3,5) # 3x3 squares
        self.width = 3
        self.max_launcher = 100  # useless?
        self.gen_position = self.genPos()

        self.launcher_size = (100, 100)

        self.setMinimumWidth((self.launcher_size[0] * 1.3))

    def addLauncher(self, app):
        """ create a button to launch app, store it as "button" key"""

        app["button"] = AppLauncherBtn(
            self.layout, app, next(self.gen_position), size=self.launcher_size
        )
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
        while i <= self.max_launcher:  # shape[0] * shape[1]:
            x = i // self.width
            y = i % self.width
            yield (x, y)
            i += 1

    def resizeEvent(self, event):
        """ Modify grid shape as window is resized """

        # button_size = (60, 70)

        # buttons_space_x = (button_size[0] + 10) * self.shape[0]
        tab_x = self.size().width()

        new_width = tab_x // self.launcher_size[0]
        if self.width != new_width:
            self.width = new_width
            self.refresh()

    def refresh(self):

        self.gen_position = self.genPos()

        for app in self.launcher_list:
            self.layout.removeItem(app["button"].layout)
        for app in self.launcher_list:
            x, y = next(self.gen_position)
            self.layout.addWidget(app["button"], x, y)

    def dragEnterEvent(self, e):
        """ A useless method """
        if e.mimeData().hasFormat("text/uri-list"):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        """ As desktop file is dropped on a tab, create a new launcher """
        import ipdb

        #        ipdb.set_trace()
        file_path = e.mimeData().urls()[0].path()  # split('//')[1:][0]
        app = parse_desktop_lang(file_path)
        file_name = file_path.split("/")[-1]
        os.system(f"cp {file_path} Apps/{self.category}/{file_name}")
        self.addLauncher(app)


class AppLauncherBtn(QFrame):
    instances = {}

    def __init__(self, parent_tab, app, pos, size):

        super(QFrame, self).__init__()

        self.layout = QVBoxLayout(self)
        self.size = size
        # layout.SetFixedSize = 120, 100
        self.icon_size = (int(size[0]), int(size[1]))
        self.setFixedSize(size[0] + 20, size[1] + 35)

        self.setStyleSheet(APP_LAUNCHER_QSS)

        name = app["Name"]  # 'qrcopy'
        icon = app["Icon"]  # 'qrcode.png'
        tooltip = app["Comment"]  #'generate a qr code'

        self.btn = QPushButton("")
        self.btn.setIcon(QIcon(QPixmap(icon)))
        self.btn.setIconSize(QSize(*self.icon_size))
        self.btn.setStyleSheet(APP_BUTTON_QSS)

        self.layout.addWidget(self.btn)
        self.btn.setToolTip(tooltip)

        self.threadpool = QThreadPool()
        # self.btn.clicked.connect(app['Exec'])
        self.app_command = app["Exec"]
        self.btn.clicked.connect(self.run_app)

        txt = QLabel(name)
        txt.setAlignment(Qt.AlignHCenter)
        txt.setStyleSheet(APP_LABEL_QSS)

        self.layout.addWidget(txt)

        self.setLayout(self.layout)

        parent_tab.addWidget(self, *pos)

        AppLauncherBtn.instances[name] = self

    def run_app(self):

        app_runner = AppRunner(self.app_command)
        self.threadpool.start(app_runner)
        MainWindow.reduce_mainwindow()

    def remove(self):
        self.layout.removeWidget(self.widget_name)
        sip.delete(self.widget_name)
        self.widget_name = None

    def resize_icons(self, size_x, size_y):
        self.setFixedSize(size_x + 20, size_y + 35)
        self.btn.setIconSize(QSize(size_x, size_y))


class AppRunner(QRunnable):
    """
    Run app in a thread
    """

    def __init__(self, app_command):

        super(AppRunner, self).__init__()
        self.command = app_command

    @pyqtSlot()
    def run(self):
        """
        Your code goes in this function
        """
        self.command()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
