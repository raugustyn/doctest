#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"


def getFontTableName(fontName):
    return "font_" + fontName.lower().replace(" ", "_").replace(".", "_").replace("-", "_")
