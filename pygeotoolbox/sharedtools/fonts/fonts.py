#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"


from base import getFontTableName


class Fonts:
    FONTS_SCHEMA_CREATED = False
    SQL_COMMANDS = None


    def __init__(self):
        pass


    @property
    def fonts(self):
        if not hasattr(self, "__fonts"):
            from font import Font
            self.__fonts = {}
            for row in self.sql.getFontInfos():
                self.__fonts[row[0]] = Font(row[0])

        return self.__fonts


    def __iter__(self):
        return self.fonts.values().__iter__()


    def font(self, name):
        return self.fonts.get(name, None)


    @property
    def names(self):
        return self.fonts.keys()

    @property
    def sql(self):
        if not Fonts.SQL_COMMANDS:
            from database import SQLCommands

            Fonts.SQL_COMMANDS = SQLCommands(sqlFileName="fonts.sql", file=__file__)

        return Fonts.SQL_COMMANDS


    def schemaNeeded(self):
        """

        >>> f.schemaNeeded()

        """
        if not Fonts.FONTS_SCHEMA_CREATED:
            self.sql.prepareFontSchema()
            Fonts.FONTS_SCHEMA_CREATED = True


    def getFontInfo(self, fontName):
        row = self.sql.getFontInfo(fontName).fetchone()
        if row:
            return row
        else:
            self.sql.registerFont(fontName, getFontTableName(fontName))
            return self.getFontInfo(fontName)


    def registerFont(self, name):

        pass


    def loadFromSVG(self, svgFileName, charsToBeAdded=None):
        from font import Font

        font = Font(svgFileName, charsToBeAdded)
        font.saveToDatabase()


fonts = Fonts()


if __name__ == "__main__":
    if False:
        fonts.schemaNeeded()
        id, tableName = fonts.getFontInfo('ArialMT.svg')
        print id, tableName

    if True:
        for font in fonts:
            print "%s - %d glyphs" % (font.name, len(font.glyphs))