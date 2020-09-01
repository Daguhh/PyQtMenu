#!/usr/bin/env python3

import os
HOME = os.getenv("HOME")

CONFIG_PATH = f"{HOME}/.config/pyqtmenu/"
APP_SAVE_FILE = "app_save.json"

ICON_PATHS = [f'{HOME}/.local/share/icons', '/usr/share/icons']
ICON_THEMES = {
    'hicolor' : ['hicolor', 'oxygen/base', 'Moka', 'Faba'],
    'Moka' : ['Moka', 'oxygen/base', 'hicolor', 'Faba'],
    'Oxygen' : ['oxygen/base', 'hicolor'],
    'Faba' : ['Faba', 'hicolor'],
}
ICON_SIZES = [512, 310, 256, 192, 150, 128, 96, 72, 64, 48, 44, 42, 36, 32, 24, 22, 16, 8]
ICON_DEFAULT = "/Apps_example/EmptyApp/empty.png"
ICON_DEFAULT_DCT = {theme:ICON_DEFAULT for theme in ICON_THEMES.keys()}

MENU_NAME = "pyqtmenu"
MENU_TITLE = "PyQtMenu"

I3_RIGHT = "right"
I3_LEFT = "left"

DUAL_PANEL_ICON = b'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAIAAABvFaqvAAAACXBIWXMAAC4jAAAuIwF4pT92AAAAB3RJTUUH5AgdDg0xPexkygAAABl0RVh0Q29tbWVudABDcmVhdGVkIHdpdGggR0lNUFeBDhcAAAbjSURBVDgRAdgGJ/kBQEA7AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADMlM7MlM4AAAC119y119wAAAD7+Yn7+YkAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAUBAOwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAv7/EAAAAAAAAAAAAAAAAAAAAAAAAAAAAQUE8AAAAv7/EAAAAAAAAAAAAAAAAAAAAAAAAAAAAQUE8AAAAAAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABQEA7AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABCyhaH5OwuHQAAAABJRU5ErkJggg=='

REDUCE_ICON = b'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAA7EAAAOxAGVKw4bAAABOElEQVRIib2WsW6DMBCGf6MMHtNHSF8h3WCwX6UDEpGqRDxGpEap+kAeyh5lqaJGCs3GFkYPSO4EMjGxTSD9Nk62//u58wFhLFR4IBP9QYjMupjzyFhniwFAMDxHB4yF6lEwFirDwWIRI45fUZaXUQwYAlVV4Xj8QZouRxExBNbrd8xmz8jz090inEdNoQ2B6fQJm82Hl0iSxP0d9BE5HL47DxUia9q2U0Ap1cuJtwMpJaSUvZ04BeqiUEpBKQUhxCmy3+9uHmotchddIln25eWAMBYq1wyqKcsL0nSJPD81MdteziP/WVQUBc7nX8znL75bIETWnqbXJEl8sxUBIAjc+RH9e+D7qnT00axjvQdjMtHVhrDdfgIAVqu3Vvx/HIzBdeY1rZus4xtzMdiBq37k3t8W38b4A7no/T+ULYZFAAAAAElFTkSuQmCC'
