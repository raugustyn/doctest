#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"


class Glyph:
    def __init__(self, name, unicodeCode, shapes):
        self.name = name
        self.unicodeCode = unicodeCode
        self.shapes = shapes