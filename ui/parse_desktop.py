#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
small desktop file parser
"""

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










