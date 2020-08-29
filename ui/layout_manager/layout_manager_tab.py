#!/usr/bin/env python3

import subprocess
import os

from PyQt5.QtWidgets import (
    QDialog,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QListWidgetItem,
    QFrame,
)

from .layout_manager import Ui_LayoutManagerWidget

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
        # cmd = r"wmctrl -lx | sed -r 's/^(\w*).*?\.(\w*).*/\1,\2/'"
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
        for i in range(len(self.l_list) + 1):
            output = subprocess.check_output(cmd, shell=True)
        self.maketabbedcontainer(mark="A")

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
        s_item = sQl.takeItem(0)
        while True:
            e_item = eQl.takeItem(0)
            if e_item == None:
                break
            sQl.addItem(e_item)
        eQl.addItem(s_item)

        # swap list
        self.l_list, self.r_list = self.r_list[:], self.l_list[:]

    def moveright(self):

        self.move(
            sQl=self.l_Qlist,
            eQl=self.r_Qlist,
            sl=self.l_list,
            el=self.r_list,
            direction="right",
        )

    def moveleft(self):

        self.move(
            sQl=self.r_Qlist,
            eQl=self.l_Qlist,
            sl=self.r_list,
            el=self.l_list,
            direction="left",
        )

    def move(self, sQl, eQl, sl, el, direction):

        # get selected window
        i = sQl.currentRow()

        # if only one window left : swap containers
        if len(sl) == 1:
            mark = sl[0]["mark"]
            cmd = f'''i3-msg "[con_mark="{mark}"] move {direction}"'''
            for i in range(len(el) + 1):
                subprocess.check_output(cmd, shell=True)

            self.swap_list(sQl, eQl, sl, el)
            self.maketabbedcontainer(mark)

        else:
            w = sl[i]
            # update list
            el.append(sl.pop(i))

            # update Qt list
            item = sQl.takeItem(i)
            eQl.addItem(item)

            # move next to top list window (i3wm mark)
            list_head_l_mark = el[0]["mark"]
            cmd = f'''i3-msg "[id={w['id']}] move to mark "{list_head_l_mark}""'''
            subprocess.check_output(cmd, shell=True)

