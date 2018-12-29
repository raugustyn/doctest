#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"


import pygeotoolbox.sharedtools.log as log
from base import getFontTableName


class Font:
    def __init__(self, name):
        self.name = name



    @property
    def glyphs(self):
        if not hasattr(self, "__glyphs"):
            from fonts import fonts
            from shapely.wkb import loads
            from glyph import Glyph

            self.__glyphs = {}
            for glyphRow in fonts.sql.getGlyphs(getFontTableName(self.name)):
                name, unicodeCode, geomWKB = glyphRow
                geom = loads(geomWKB, hex=True)
                self.__glyphs[name] = Glyph(name, unicodeCode, geom)

        return self.__glyphs

    def __iter__(self):
        return self.glyphs.values().__iter__()


    def textToSQL(self, x, y, text):
        from shapely.affinity import translate

        sql = ""
        dx = x
        for char in unicode(text, "utf-8"):
            if not char in self.glyphs:
                char = char.encode("hex")
            if char in self.glyphs:
                glyph = self.glyphs[char]
                shape = glyph.shape
                if shape:
                    shape = translate(shape, dx, y)
                    minx, miny, maxx, maxy = shape.bounds
                    dx += 1.2 * (maxx - minx)
                    sql += "insert into temp.glyphs(name, geom) values('%s', st_geometryfromtext('%s', 5514));\n" % (
                    glyph.name, shape.wkt)
        return sql


    @property
    def letters(self):
        result = u""
        for char in self.glyphs.keys():
            result += char

        return "".join(sorted(result))


    def saveToDatabase(self):
        from pygeotoolbox.sharedtools.fonts.fonts import fonts
        from shapely.affinity import translate
        from pygeotoolbox.database import database

        fonts.schemaNeeded()
        id, tableName = fonts.getFontInfo(self.name)
        fonts.sql.createFontTable(tableName)

        sql = ""
        dx = 0
        for key, glyph in self.glyphs.iteritems():
            shape = glyph.shape
            if shape:
                shape = translate(shape, dx, 0)
                minx, miny, maxx, maxy = shape.bounds
                dx += 1.2*(maxx - minx)
                sql += "insert into mg_fonts.%s(unicode, name, geom) values('%s', ''%s', st_geometryfromtext('%s', 5514));\n" % (tableName, key.encode('hex'), glyph.name, shape.wkt)
            else:
                log.warning("Letter '%s' has no glyph" % key)

        fonts.schemaNeeded()
        database.execute(sql)


    def readFromSVG(self, svgReaderOrSVGFileName, saveToDatabase=True):
        from svg.svgfontreader import SVGFontReader

        if isinstance(svgReaderOrSVGFileName, SVGFontReader):
            svgFontReader = svgReaderOrSVGFileName
        else:
            svgFontReader = SVGFontReader(svgReaderOrSVGFileName, charsToBeLoaded = None)
        self.glyphs = svgFontReader.glyphs
        self.name = svgFontReader.name
        if saveToDatabase:
            self.saveToDatabase()


if __name__ == "__main__":
    from svg.svgfontreader import readTestFonts

    log.openSection("Reading svg fonts...")
    fonts = readTestFonts()
    log.closeSection()

    log.openSection("Saving fonts to database...")
    for svgFont in readTestFonts():
        log.info(svgFont.name)
        font = Font("")
        font.readFromSVG(svgFont)
        log.closeSection()
    log.closeSection()


# @TODO Některé základní znaky se načtou, ale nemají glyph
# @TODO Sloupce unicode a letters se nenaplňují
# @TODO Potřeba vytvořit algoritmus pro sestavení textu podél křivky či čáry, s volbou text originu, případných offsetů atd.

