#!/usr/bin/env python3

import os
HOME = os.getenv("HOME")

CONFIG_PATH = f"{HOME}/.config/pyqtmenu/"
APP_SAVE_FILE = "app_save.json"

ICON_PATHS = [f'{HOME}/.local/share/icons', '/usr/share/icons/']
ICON_THEME = ['hicolor', 'oxygen/base']
ICON_SIZES = [512, 310, 256, 192, 150, 128, 96, 72, 64, 48, 44, 42, 36, 32, 24, 22, 16, 8]
ICON_DEFAULT = "/Apps_example/EmptyApp/empty.png"

MENU_NAME = "pyqtmenu"
MENU_TITLE = "PyQtMenu"

I3_RIGHT = "right"
I3_LEFT = "left"
