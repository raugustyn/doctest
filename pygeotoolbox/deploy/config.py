#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"


import datetime
from fileprocessors import PythonProcessFileProcessor, SQL_FileProcessor


class Config:
    skipedDirectories = [".git", '.idea']
    skippedExtensions = [".log"]
    BUILD_NUMBER = 1
    data = {
        ".pyc": None,
        ".log": None,
        ".qgs~": None,
        ".py": PythonProcessFileProcessor,
        ".sql": SQL_FileProcessor
    }
    authors = {
        "radek.augustyn@email.cz" : {
            "Author": "Ing.Radek Augustýn",
            "E-mail": "radek.augustyn@email.cz",
            "Web":    "http://raugustyn.github.io/",
            "Copyright": "(c) Radek Augustýn, " + str(datetime.datetime.today().year)
        },
        "radek.augustyn@vugtk.cz": {
            "Author": "Ing.Radek Augustýn",
            "E-mail": "radek.augustyn@vugtk.cz",
            "Web": "http://www.vugtk.cz/",
            "Copyright": "(c) VUGTK, v.v.i. " + str(datetime.datetime.today().year)
        }
    }