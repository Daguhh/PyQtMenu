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
    QGraphicsOpacityEffect,
    QListWidgetItem,
    QFrame,
)
from PyQt5.QtGui import QPixmap, QIcon, QStaticText, QColor, QFont
from PyQt5.QtCore import QThreadPool, QRunnable, pyqtSlot

from .parse_desktop_file import get_app_from_desktop, parse_desktop_lang
from .layout_manager import Ui_LayoutManagerWidget


class MainWindow(QMainWindow):

    # bigpicture = True
    instance = None

    def __init__(self):
        super().__init__()
        self.title = "PyQtMenu"
        self.setWindowTitle(self.title)
        self.isSplit = False
#        self.setStyleSheet("""
#""")
        #self.setMouseTracking(True)
        MainWindow.instance = self

        self.initUI()

    def initUI(self):

        ######## Menubar ############
        exitAct = QAction(text="&Exit", parent=self)
        exitAct.setShortcut("Ctrl+Q")
        exitAct.setStatusTip("Exit application")
        exitAct.triggered.connect(QApplication.quit)

        resizeiconAct = QAction(text="&Resize Icons", parent=self)
        resizeiconAct.triggered.connect(self.resize_icons)
        self.statusBar()

        self.reducemodAct = QAction("Masquer", self, checkable=True)
        self.reducemodAct.setStatusTip("Cache le menu au lancement d'une application")
        self.reducemodAct.setChecked(True)
        #    reducemodAct.triggered.connect(MainWindow.toggle_bigpicture)

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

        splitBtn = QPushButton("Split")
        splitBtn.setToolTip("place les fenêtres côte à cote à la verticale")
        splitBtn.clicked.connect(self.toogle_layout)

        twopanelBtn = QPushButton("2 panel")
        twopanelBtn.setToolTip("dispose les fenêtes sous forme de deux panneaux")

        hbox = QHBoxLayout()
        hbox.addWidget(reduceBtn)
        hbox.addWidget(splitBtn)
        hbox.addWidget(twopanelBtn)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        window.setLayout(vbox)

        ########### Tabs launchers ####################
        # create tab
        self.table_widget = TabsContainer(parent=self)
        twopanelBtn.clicked.connect(self.table_widget.layout_mgr.refresh)
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
        if cls.instance.reducemodAct.isChecked() == False:
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


class AskMultipleValues(QDialog):
    """ Dialog to resize icon """

    def __init__(self, *args, **kwargs):

        super(QDialog, self).__init__()
        self.layout = QGridLayout(self)  # QVBoxLayout(self)
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

        self.layout.addWidget(cancel_btn, i + 1, 1)
        self.layout.addWidget(ok_btn, i + 1, 2)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.accept()
        elif e.key() == Qt.Key_Escape:
            self.close()

    def get_values(self):
        vals = []
        for textEdit in self.textEdits:
            vals.append(textEdit.text())
        try :
            if any([int(val) >= 1 for val in vals]):
                return (*vals, True)
            else :
                raise ValueError("Size must be >= 1")
        except ValueError as e:
            print(f"{e}\nwrong value for icon size")
            return 0, 0, False

    def cancel(self):
        return 0, 0, False


class LayoutMgr(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = Ui_LayoutManagerWidget()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)

        # list list
        self.l_Qlist = self.ui.leftlistWidget
        self.r_Qlist = self.ui.rightlistWidget
        self.l_list = []
        self.r_list = []

        self.connect_list()

    def refresh(self):

        self.l_Qlist.clear()
        self.r_Qlist.clear()
        self.l_list = []
        self.r_list = []

        self.list_windows()

    def list_windows(self):

        # get window list and their id
        #cmd = r"wmctrl -lx | sed -r 's/^(\w*).*?\.(\w*).*/\1,\2/'"
        cmd = r"wmctrl -lx | sed -r 's/^(\w*)[^.]*\.(\w*).*/\1,\2/'"
        out = subprocess.check_output(cmd, shell=True, text=True)
        self.w_list = [
            {"name": w_name, "id": X11_id}
            for X11_id, w_name in [line.split(",") for line in out.split("\n")][:-1]
        ]

        # Mark all windows (see i3wm doc for mark)
        alph = "ABCDEFGHIJKLMNOPQRSTU"
        for mark, w in zip(alph, self.w_list):
            w["mark"] = mark
            i3_cmd = f"[id={w['id']}] mark {mark}"
            cmd = f'i3-msg "{i3_cmd}"'
            subprocess.check_output(cmd, shell=True)

        # create list of window for right and left container
        self.l_list = self.w_list[:]  # put all window on the left
        self.r_list = []
        for i, w in enumerate(self.l_list):
            if w["mark"] == "A":  # put window with mark A in right list
                self.r_list.append(self.l_list.pop(i))

        # move first window to the right and make a tabbed container
        cmd = '''i3-msg "[con_mark="A"] move right"'''
        for i in range(len(self.l_list)+1):
            output = subprocess.check_output(cmd, shell=True)
        self.maketabbedcontainer(mark='A')

        # show list item in QtListWidget
        self.l_Qlist.addItems([w["name"] for w in self.l_list])
        self.r_Qlist.addItems([w["name"] for w in self.r_list])

    def connect_list(self):

        self.ui.moveleftBtn.clicked.connect(self.moveleft)
        self.ui.moverightBtn.clicked.connect(self.moveright)

    def maketabbedcontainer(self, mark):

        os.system(f"""i3-msg "[con_mark="{mark}"] split horizontal" """)
        os.system(f"""i3-msg "[con_mark="{mark}"] focus, layout tabbed" """)

    def swap_list(self, sQl, eQl, sl, el):

        # sawp Qlist
        l_item = sQl.takeItem(0)
        while True:
            r_item = eQl.takeItem(0)
            if r_item == None :
                break
            sQl.addItem(r_item)
        eQl.addItem(l_item)

        #swap list
        self.l_list, self.r_list = self.r_list[:], self.l_list[:]


    def moveright(self):

        self.move(sQl=self.l_Qlist,
                  eQl=self.r_Qlist,
                  sl=self.l_list,
                  el=self.r_list,
                  direction='right')

    def moveleft(self):

        self.move(sQl=self.r_Qlist,
                  eQl=self.l_Qlist,
                  sl=self.r_list,
                  el=self.l_list,
                  direction='left')

    def move(self, sQl, eQl, sl, el, direction):

        # get selected window
        i = sQl.currentRow()

        # if only one window left : swap containers
        if len(sl) == 1:
            mark = sl[0]['mark']
            cmd = f'''i3-msg "[con_mark="{mark}"] move {direction}"'''
            for i in range(len(el)+1):
                subprocess.check_output(cmd, shell=True)

            self.swap_list(sQl, eQl, sl, el)
            self.maketabbedcontainer(mark)

        else:
            w = sl[i]
            # update list
            el.append(sl.pop(i))

            # update Qt list
            item = self.l_Qlist.takeItem(i)
            eQl.addItem(item)

            # move next to top list window (i3wm mark)
            list_head_l_mark = el[0]["mark"]
            cmd = f'''i3-msg "[id={w['id']}] move to mark "{list_head_l_mark}""'''
            subprocess.check_output(cmd, shell=True)

#    def moveleft(self):
#
#        # get selected window
#        i = self.r_Qlist.currentRow()
#        w = self.r_list[i]
#
#        # update list
#        self.l_list.append(self.r_list.pop(i))
#
#        # update Qt list
#        item = self.r_Qlist.takeItem(i)
#        self.l_Qlist.addItem(item)
#
#        # move next to top list window (i3wm mark)
#        list_head_r_mark = self.l_list[0]["mark"]
#        cmd = f'''i3-msg "[id={w['id']}] move to mark "{list_head_r_mark}""'''
#        subprocess.check_output(cmd, shell=True)


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
        self.addtabmodule()

        # Fill tabs with apps with launchers
        for app in app_list:
            category = app["category"]
            Tab.instances[category].addLauncher(app)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def addtabmodule(self):

        # add a tab for layout management (i3module)
        self.layout_mgr = LayoutMgr()
        name = "layout"
        self.tabs.addTab(self.layout_mgr, name)


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

        self.setStyleSheet("""
            QFrame:hover {
                border: 2px solid green;
                border-radius: 4px;
                padding: 2px;
            }
            QFrame:pressed {
                border: 50px solid green;
                border-radius: 44px;
                padding: 2px;
            }
        """)

        name = app["Name"]  # 'qrcopy'
        icon = app["Icon"]  # 'qrcode.png'
        tooltip = app["Comment"]  #'generate a qr code'

        self.btn = QPushButton("")
        self.btn.setIcon(QIcon(QPixmap(icon)))
        self.btn.setIconSize(QSize(*self.icon_size))
        self.btn.setStyleSheet("""
            QPushButton {
                border: None;
            }
            QPushButton:pressed {
                border: 50px solid white;
                border-radius: 60px;
                padding: 4px;
            }
        """)
        #25px solid #6593cf;
        #        border-radius: 2px;
        #        //margin: 20px;
        #        padding: 20px
        #"    }
        #""")
#        QWidget {
#            border: 20px solid black;
#            border-radius: 10px;
#            background-color: rgb(255, 255, 255);
#            }
#        """)
        self.layout.addWidget(self.btn)
        self.btn.setToolTip(tooltip)

        self.threadpool = QThreadPool()
        # self.btn.clicked.connect(app['Exec'])
        self.app_command = app["Exec"]
        self.btn.clicked.connect(self.run_app)

        txt = QLabel(name)
        txt.setAlignment(Qt.AlignHCenter)
        txt.setStyleSheet("""
            QLabel {
                border : None;
                }
        """)
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
