#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
small desktop file parser
"""

import os
import glob

def get_app_from_desktop():
    """
    get all app dict and store them in a list
    """

    app_list = []

    path_desktop = "/home/david/Programmation/Projets/PythonMenu/MyMenu/ui/*.desktop"
    for file in glob.iglob(path_desktop):
        app = parse_desktop(file)
        app['Exec'] = txt2fct(app['Exec'])
        app_list += [app]

    return app_list

def txt2fct(command_path):
    """ transform path of a command into a python function """

    def exec():
        os.system(command_path)
    return exec


def parse_desktop(file_name):
    """
    parse_desktop("fichier.desktop") => dict

    args:
        str : desktop file following freedesktop guidelines
    return:
        dict : parsed desktop file into dict
    """

    app = {}
    with open(file_name, 'r') as file:
        next(file) # forget first line
        for line in file:
            k, v = [l.strip() for l in line.split('=')]
            app[k] = v

    return app


if __name__ == "__main__":
    app = parse_desktop("qrcode.desktop")
    #print(app)
    for k,v in app.items():
        print(k,v)

    print('=================')
    app_list = get_app_from_desktop()
    print(app_list)
    print('=================')
    print(app_list[0])










