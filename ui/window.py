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
    QTextEdit,
    QDesktopWidget,
    QSizePolicy,
    QGraphicsOpacityEffect
)
from PyQt5.QtGui import QPixmap, QIcon, QStaticText, QColor, QFont
from PyQt5.QtCore import QThreadPool, QRunnable, pyqtSlot

from .parse_desktop_file import get_app_from_desktop, parse_desktop_lang

class MainWindow(QMainWindow):

    #bigpicture = True
    instance = None

    def __init__(self):
        super().__init__()
        self.title = "PyQtMenu"
        self.setWindowTitle(self.title)
        #self.setStyleSheet("""
        #QWidget {
        #
        #    border: 20px solid black;
        #    border-radius: 10px;
        #    background-color: rgb(255, 255, 255);
        #    }
        #""")

        MainWindow.instance = self

        self.initUI()

    def initUI(self):

        ######## Menubar ############
        exitAct = QAction(text='&Exit', parent=self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(QApplication.quit)

        resizeiconAct = QAction(text='&Resize Icons', parent=self)
        resizeiconAct.triggered.connect(self.resize_icons)
        self.statusBar()

        self.reducemodAct = QAction('Masquer', self, checkable=True)
        self.reducemodAct.setStatusTip("Cache le menu au lancement d'une application")
        self.reducemodAct.setChecked(True)
    #    reducemodAct.triggered.connect(MainWindow.toggle_bigpicture)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Fichier')
        fileMenu.addAction(exitAct)
        EditMenu = menubar.addMenu('&Edition')
        EditMenu.addAction(resizeiconAct)
        EditMenu.addAction(self.reducemodAct)


        ######## control panel ############
        window = QWidget()
        self.setCentralWidget(window)

        reduceBtn = QPushButton("M")
        #reduceBtn.setGeometry(0, 0, 200, 200)
        reduceBtn.setFixedSize(100,100)
        reduceBtn.setToolTip("Réduire le menu")
        reduceBtn.setFont(QFont('Times', 80))
        reduceBtn.clicked.connect(MainWindow.reduce_mainwindow)
        cancelButton = QPushButton("Cancel")

        hbox = QHBoxLayout()
        #hbox.addStretch(1)
        hbox.addWidget(reduceBtn)
        hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
#        vbox.addStretch(1)
        vbox.addLayout(hbox)

        window.setLayout(vbox)

        ########### Tabs launchers ####################
        # create tab
        self.table_widget = TabsContainer(parent=self)
        vbox.addWidget(self.table_widget)
        #self.setCentralWidget(self.table_widget)



        self.show()

    def get_size_value(self, *args):
        dialog = AskMultipleValues(*args)
        #dialog.exec_()
        if dialog.exec_():
            vals = dialog.get_values()
        else:
            vals = dialog.cancel()
        return vals

#    @classmethod
#    def toggle_bigpicture(cls):
#        print('enable bigpiture')
#        cls.bigpicture = not cls.bigpicture

    @classmethod
    def reduce_mainwindow(cls):
        if cls.instance.reducemodAct.isChecked() == False:
            return
        dialog = ReduceModButton()
        MainWindow.instance.hide()
        #self.hide()
        if dialog.exec_():
            vals = dialog.accept()
            cls.instance.show()
        else:
            vals = dialog.cancel()
        return


    def resize_icons(self):
        x, y, test = self.get_size_value('x','y')
        x, y = int(x), int(y)
        if test:
            for launcher in AppLauncherBtn.instances.values():
                launcher.resize_icons(x, y)
            for tab in Tab.instances.values():
                tab.launcher_size = (x, y)
                tab.setMinimumWidth(int(x)+20)

class ReduceModButton(QDialog):
    """ button that reopen main window """

    def __init__(self):
        super(QDialog, self).__init__()
        self.layout = QGridLayout(self) #QVBoxLayout(self)
        reopen_button = QPushButton("M")
        reopen_button.setGeometry(0, 0, 100, 100)
        reopen_button.setStatusTip("Afficher le menu en plein écran")
        reopen_button.clicked.connect(self.accept)
        self.setGeometry(0,0,150,150)
        #bottomright_pos = QApplication.desktop().availableGeometry().bottomRight()
        dialog_size = self.geometry().getRect()
        desktop_size = QApplication.desktop().screenGeometry().getRect()
        *_ ,x, y = map(lambda x,y : y -x - 30, dialog_size, desktop_size)
        self.move(x,y)
        reopen_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        reopen_button.setStyleSheet("background-color:rgba(55,55,55,15);")#setPalette().setColo(QColor(0,0,0,20))
        reopen_button.setFont(QFont('Times', 48))
        #reopen_button.setPalette(

        #rightpoint = QDesktopWidget().availableGeometry().bottomRight()

        self.layout.addWidget(reopen_button)
#        self.setWindowOpacity(10)
        op=QGraphicsOpacityEffect(self)
        op.setOpacity(0.5) #0 to 1 will cause the fade effect to kick in
        self.setGraphicsEffect(op)
        self.setAutoFillBackground(True)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        #self.move(rightpoint)

class AskMultipleValues(QDialog):
    """ Dialog to resize icon """

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

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.accept()
        elif e.key() == Qt.Key_Escape:
            self.close()

    def get_values(self):
        vals = []
        for textEdit in self.textEdits:
            vals.append(textEdit.text())

        return (*vals, True)

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
        self.max_launcher = 100 # useless?
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
        while i <= self.max_launcher: #shape[0] * shape[1]:
            x = i//self.width
            y = i%self.width
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
        if e.mimeData().hasFormat("text/uri-list"):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        """ As desktop file is dropped on a tab, create a new launcher """
        import ipdb
#        ipdb.set_trace()
        file_path = e.mimeData().urls()[0].path() #split('//')[1:][0]
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

        self.threadpool = QThreadPool()
        #self.btn.clicked.connect(app['Exec'])
        self.app_command = app['Exec']
        self.btn.clicked.connect(self.run_app)

        txt = QLabel(name)
        txt.setAlignment(Qt.AlignHCenter)
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
        self.setFixedSize(size_x+20, size_y+35)
        self.btn.setIconSize(QSize(size_x, size_y))

class AppRunner(QRunnable):
    '''
    Run app in a thread
    '''

    def __init__(self, app_command):

        super(AppRunner, self).__init__()
        self.command = app_command

    @pyqtSlot()
    def run(self):
        '''
        Your code goes in this function
        '''
        print("Thread start")
        self.command()
        print("Thread complete")

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

