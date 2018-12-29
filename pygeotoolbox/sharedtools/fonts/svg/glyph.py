#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"


from shapely.wkt import loads
from base import *
from pathshape import PathShape


class Glyph:
    """Implements letter glyph outline.
    """
    PATH_STROKE_LENGTH = 30


    def __init__(self, glyphXMLContent, glyphs):
        """Parses glyphXMLContent, default values takes from glyphs parameter.

        :param glyphXMLContent: Glyph XML content.
        :param glyphs:
        """
        self.glyphXMLContent = glyphXMLContent
        self.name = extractParam(glyphXMLContent, "glyph-name")
        unicode = extractParam(glyphXMLContent, "unicode")
        if unicode.startswith("&#x"):
            unicodes = unicode.split(";")
            chars = []
            for unicode in unicodes:
                if unicode:
                    unicodeValue = int(unicode[3:], 16)
                    char = unichr(unicodeValue)
                    chars.append(char)
            if len(chars) == 1:
                unicode = chars[0]
            else:
                unicode = chars
        self.unicode = unicode
        self.width = int(extractParam(glyphXMLContent, "horiz-adv-x", glyphs.defaults.width))
        self.shapes = []
        d = extractParam(glyphXMLContent, "d")
        if d:
            if d[len(d) - 1:] == "z":
                d = d[:len(d) - 1]

            shapeDefs = d.split("z")
            for shapeDef in shapeDefs:
                shape = PathShape(shapeDef, Glyph.PATH_STROKE_LENGTH)
                self.shapes.append(shape)


    @property
    def wkt(self):
        """Returns Well Known Text representation of the glyph.

        :return:  Well Known Text representation of the glyph.
        """
        if len(self.shapes) == 0:
            return ""
        elif len(self.shapes) == 1:
            return self.shapes[0].wkt
        else:
            return "MULTIPOLYGON(\n%s\n)" % (",\n".join(map(lambda shape: "\t" + shape.wkt.replace("Polygon", ""), self.shapes)))


    @property
    def shape(self):
        """Returns shapely shape representation of the glyph.

        :return:  shapely shape representation of the glyph.
        """
        wkt = self.wkt
        if wkt:
            try:
                result = loads(self.wkt)
                return result
            except:
                return None