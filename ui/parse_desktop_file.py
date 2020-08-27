#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
small desktop file parser
"""

import os
import glob
import re
from itertools import product

from config import ICON_PATHS, ICON_THEME, ICON_SIZES, ICON_DEFAULT


def get_app_for_folder():
    pass


def get_app_from_desktop():
    """
    get all app dict and store them in a list
    """

    app_list = []

    path_desktop = "Apps/*/*.desktop"
    for file in glob.iglob(path_desktop):
        app = parse_desktop_lang(file)

        category = file.split('/')[-2]
        app['category'] = category

        app_list += [app]

    return app_list

def txt2fct(command_path):
    """ transform path of a command into a python function """

    def exec():
        os.system(command_path)
    return exec

def icon2path(icon_name):
    """
    return icon path from icon_name :
        - if icon_name is path to icon, do nothing
        - if not look for icon in file system
    """
    icon_path = ICON_DEFAULT
    if not icon_name:
        pass
    elif os.path.isfile(icon_name):
        icon_path = icon_name
    else:
        t = ICON_THEME
        for s, p in product(ICON_SIZES, ICON_PATHS):
            icon_tmp = glob.glob(f'{p}/{t}/{s}x{s}/*/{icon_name}.*')
            if icon_tmp:
                icon_path = icon_tmp[0]
                break
    return icon_path

            #icon = glob.glob(f'/usr/share/icons/hicolor/128x128/*/{icon}.*')[0]

    return icon

def create_pattern(entry, lang=None):
    if lang != None:
        pattern = re.compile(f'^{entry}\[{lang}\]=.*')
    else:
        pattern = re.compile(f'^{entry}=.*')
    return pattern

def find_in_file(file, pattern):
    match = None
    with open(file) as f:
        for line in f:
            temp = pattern.match(line)
            if temp != None:
                match = temp.string.replace("\n", "").split('=')[-1]
                break
    return match

def parse_desktop_lang(file_name, lang='fr'):
    """
    parse_desktop("fichier.desktop") => dict

    args:
        str : desktop file following freedesktop guidelines
    return:
        dict : parsed desktop file into dict
    """

    entry_names_tr = ['Name', 'Comment']
    entry_names = ['Exec', 'Icon']

    app = {}
    for name in entry_names_tr:
        pattern = create_pattern(name, lang)
        match = find_in_file(file_name, pattern)

        if match == None:
            pattern = create_pattern(name)
            match = find_in_file(file_name, pattern)

        app[name] = match

    for name in entry_names:
        pattern = create_pattern(name)
        match = find_in_file(file_name, pattern)

        app[name] = match


    app['Exec'] = txt2fct(app['Exec'])
    app['Icon'] = icon2path(app['Icon'])
    return app

def parse_desktop(file_name):
    """
    parse_desktop("fichier.desktop") => dict

    args:
        str : desktop file following freedesktop guidelines
    return:
        dict : parsed desktop file into dict
    """

    entries = ['Name', 'Comment', 'Exec', 'Icon']

    Name = re.match(f'Name\[{lang}\]')
    app = {}
    with open(file_name, 'r') as file:
        next(file) # forget first line
        for line in file:
            k, v = [l.strip() for l in line.split('=')]
            app[k] = v

    app['Exec'] = txt2fct(app['Exec'])
    return app


if __name__ == "__main__":
    app = parse_desktop("qrcode.desktop")
    for k,v in app.items():
        pass
    app_list = get_app_from_desktop()




