#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"

import os
import pygeotoolbox.sharedtools.log as log
from pygeotoolbox.sharedtools import extractFileName, changeFileExtension
from pygeotoolbox.sharedtools import Container
from base import *
from glyph import Glyph


class SVGFontReader:
    def __init__(self, svgFileName, charsToBeLoaded = None):
        self.name = changeFileExtension(extractFileName(svgFileName), "")

        self.glyphs = {}
        self.defaults = Container({
            "width" : 556,
            "height" : None,
            "x" : None,
            "y" : None
        })

        log.openSection("Reading glyphs from %s" % svgFileName, log.DEBUG)
        svgData = open(svgFileName, "r").read().replace('\n', '')

        self.letters = u""
        startPos = 0
        while startPos < len(svgData):
            startPos = svgData.find('<glyph', startPos)
            if startPos >=  0:
                endPos = svgData.find("/>", startPos) + 2
                if endPos >= 0:
                    tag = svgData[startPos:endPos]
                    glyph = Glyph(tag, self)

                    if isinstance(glyph.unicode, list):
                        unicodes = glyph.unicode
                    else:
                        unicodes = [glyph.unicode]
                    for unicode in unicodes:
                        if not charsToBeLoaded or unicode in charsToBeLoaded:
                            self.letters += unicode
                            self.glyphs[unicode] = glyph
                    startPos = endPos
                else:
                    log.error("Unclosed glyph tag at %d" % startPos)
                    break
            else:
                break

        self.letters = "".join(sorted(self.letters))

        if charsToBeLoaded and len(charsToBeLoaded) <> len(self.glyphs.keys()):
            log.openSection("Not all characters found!", log.WARNING)
            log.warning("%d characters to be loaded, %d found" % (len(charsToBeLoaded), len(self.glyphs.keys())))

            log.closeSection(level=log.WARNING)
        log.closeSection("%d glyphs found" % len(self.glyphs.keys()), level=log.DEBUG)


def readTestFonts():
    import os

    fonts = []
    for fontName in ['ArialMT.svg', 'Helvetica-Regular.svg']:
        log.openSection("Loading font %s into database..." % fontName)
        font = SVGFontReader(os.path.dirname(__file__) + os.sep + fontName, addCharaters(getLowerASCII(), u'ěščřžýáíéúůĚŠČŘŽÝÁÍÉÚŮ'))
        fonts.append(font)
        log.info("'%s':%d glyphs readed." % (fontName, len(font.glyphs.keys())))
        log.info("[%s]" % font.letters)
        log.closeSection()

    return fonts


if __name__ == "__main__":
    readTestFonts()
