#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
small desktop file parser
"""

import os
import glob
import re
from itertools import product
import hashlib
import json


from config import (
    ICON_PATHS, ICON_SIZES, CONFIG,
    CONFIG_PATH, APP_SAVE_FILE, ICON_DEFAULT,
    DESKTOP_FILES_PATH,
)


def get_app_for_folder():
    pass

def hash_file(file):
    """hash .desktop file to watch for any change"""

    hasher = hashlib.md5()
    with open(file, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def get_app_from_desktop():
    """
    get all app dict and store them in a list
    """

    # Try load previous session
    app_config_file = APP_SAVE_FILE
    try:
        with open(app_config_file) as json_data_file:
            saved_app = json.load(json_data_file)
    except FileNotFoundError as e:
        saved_app = {}

    app_list = []
    app_dct = {}

    # parse .desktop file if it's new
    path_desktop = f"{DESKTOP_FILES_PATH}/*/*.desktop"
    for file in glob.iglob(path_desktop):

        hex_hash = hash_file(file)

        # if new launcher : parse .desktop
        if not hex_hash in list(saved_app.keys()):

            app = parse_desktop_lang(file)
            category = file.split('/')[-2]
            app['category'] = category
            app['Icon']  = icon2paths(app['Icon']).copy()

        # else load from json conf
        else:
            app = saved_app[hex_hash]

        app_list += [app]
        app_dct[hex_hash] = app

    # Save session
    with open(app_config_file, "w") as outfile:
        json.dump(app_dct, outfile)

    # python function is not serializable so had to be done after loadin json
    for app in app_list:
        app['Exec'] = txt2fct(app['Exec'])

    return app_list

def txt2fct(command_path):
    """ transform path of a command into a python function """

    def exec():
        os.system(command_path)
    return exec

def icon2paths(icon_name):
    """
    return icon path from icon_name :
        - if icon_name is path to icon, do nothing
        - if not look for icon in file system
    """
    icon_path = {theme:ICON_DEFAULT for theme in CONFIG['Themes']}
    if not icon_name:
        pass
    elif os.path.isfile(icon_name):
        for theme in CONFIG['Themes']:
            icon_path[theme] = icon_name
    else:
        for theme in CONFIG['Themes']:
            theme_paths = CONFIG['Themes'][theme].replace(' ','').split(',')
            for t, s, p in product(theme_paths, ICON_SIZES, ICON_PATHS):
                icon_tmp = glob.glob(f'{p}/{t}/{s}x{s}/*/{icon_name}.*')
                if icon_tmp:
                    icon_path[theme] = icon_tmp[0]
                    break
    return icon_path

def create_pattern(entry, lang=None):
    """Return a pattern to parse either or not translated entry in .desktop"""

    if lang != None:
        pattern = re.compile(f'^{entry}\[{lang}\]=.*')
    else:
        pattern = re.compile(f'^{entry}=.*')
    return pattern

def find_in_file(file, pattern):
    """return a matched pattern in a file"""

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

    entry_names_lang = ['Name', 'Comment']
    entry_names = ['Exec', 'Icon']

    app = {}
    for name in entry_names_lang:
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




