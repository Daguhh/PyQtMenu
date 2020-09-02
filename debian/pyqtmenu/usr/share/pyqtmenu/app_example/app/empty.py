#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
"""

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication

class Example(QWidget):
    
    def __init__(self):
        super(QWidget, self).__init__()

        self.setWindowTitle('Useless app')    
        self.initUI()
        
    def initUI(self):               
        
        btn = QPushButton('Quit', self)
        btn.clicked.connect(QApplication.instance().quit)
        btn.resize(btn.sizeHint())
        
        self.setGeometry(300, 300, 250, 150)
        self.show()
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
