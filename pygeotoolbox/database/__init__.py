#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"
"""
Database package implements simple database binder for geodatabase access. It is primary developed implementing PostGIS database wrapper,
open for another databases as well.
"""

import pygeotoolbox.sharedtools.config as config
from sqltemplating import SQLCommands
from base import *

__databases = {}

if config.database.type.lower() == "postgis":
    from postgis import Database
else:
    from base import DatabaseTemplate as Database


connection = database = Database()


def databaseByName(name):
    """Returns database with a given name. If it doesn't exist yet, creates and returns new instance.

    :param str name: database name
    :return: database with a given name
    """
    global __databases

    if not name in __databases:
        if config.database.name == name:
            database.connection  # do connect
            __databases[name] = database
        else:
            __databases[name] = Database()
            savedDBName = config.database.name
            config.database.name = name
            __databases[name].connection # do connect
            config.database.name = savedDBName

    return __databases[name]
