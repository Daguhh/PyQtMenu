#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import os
import sys
import glob

from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
    QTextEdit, QGridLayout, QApplication,
    QAction, QFileDialog, QPushButton, QComboBox, QScrollArea)



class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        path = QLabel('path')
        pathsearch = QPushButton("open",self)
        pathsearch.clicked.connect(self.showdialog)

        extension = QLabel('extension')
        pattern = QLabel('Pattern')
        self.pattern_txt = QLineEdit()
        self.pattern_txt.setReadOnly(True)
        file_list = QLabel('files')
        actualize_files = QPushButton('Actualiser',self)
        actualize_files.clicked.connect(self.get_file_list)

        self.choose_action = QComboBox(self)
        self.choose_action.addItem("delete metadata")
        self.choose_action.addItem("rename with -Title")
        run_action = QPushButton('run', self)
        run_action.clicked.connect(self.run)

        self.pathEdit = QLineEdit()
        self.pathEdit.textChanged.connect(self.update_pattern)
        self.extensionEdit = QLineEdit()
        self.extensionEdit.textChanged.connect(self.update_pattern)
        self.file_list_disp = QTextEdit()

        grid = QGridLayout()
        #grid.setSpacing(10)

        grid.addWidget(path, 0, 0)
        grid.addWidget(self.pathEdit, 0, 1)
        grid.addWidget(pathsearch, 0, 2)

        grid.addWidget(extension, 1, 0)
        grid.addWidget(self.extensionEdit, 1, 1, 1, 2)

        grid.addWidget(pattern, 2, 0)
        grid.addWidget(self.pattern_txt, 2, 1, 1, 2)

        grid.addWidget(file_list, 3, 0)
        grid.addWidget(actualize_files, 3, 1, 1, 2)
        grid.addWidget(self.file_list_disp, 4, 0, 1, 3)

        grid.addWidget(self.choose_action, 5, 0, 1, 2)
        grid.addWidget(run_action, 5,2)

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.show()

    def run(self):
        action = str(self.choose_action.currentText())
        print(f'action = {action}')
        path = self.path_to_proceed
        if action == "delete metadata":
            for file in self.files_to_proceed:
                print(file)
                os.system(f"exiftool -all= '{path}/{file}'")
        elif action == "rename with -Title":
            for file in self.files_to_proceed:
                print(file)
                os.system(f"exiftool '-filename<$title.%e' '{path}/{file}'")

    def showdialog(self):
        dir_name = QFileDialog.getExistingDirectory(self, 'Select dir', '/home')

        self.pathEdit.setText(dir_name)

    def update_pattern(self):
        path = self.pathEdit.text()
        extension = self.extensionEdit.text()

        self.pattern_txt.setText(f'{path}/*.{extension}')

    def get_file_list(self):
        path = self.pathEdit.text()
        extension = self.extensionEdit.text()

        pattern = f'{path}/*.{extension}'
        print(pattern)
        self.files_to_proceed = [l.split('/')[-1] for l in glob.iglob(pattern)]
        files= '\n'.join(self.files_to_proceed)
        print(files)
        self.path_to_proceed = path
        self.file_list_disp.setText(files)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
