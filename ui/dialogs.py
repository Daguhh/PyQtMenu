#!/usr/bin/env python3

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog,
    QPushButton,
    QLabel,
    QGridLayout,
    QLineEdit,
)


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
        try:
            if any([int(val) >= 1 for val in vals]):
                return (*vals, True)
            else:
                raise ValueError("Size must be >= 1")
        except ValueError as e:
            print(f"{e}\nwrong value for icon size")
            return 0, 0, False

    def cancel(self):
        return 0, 0, False

