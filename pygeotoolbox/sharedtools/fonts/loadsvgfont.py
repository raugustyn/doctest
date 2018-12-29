#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"


import pygeotoolbox.sharedtools.log as log
from svg.base import *
from svg.svgfontreader import SVGFontReader


def getCharactersInSQL(sql):
    from pygeotoolbox.database import database

    result = u""
    rows = database.executeSelectSQL(sql)
    for row in rows:
        result = addCharaters(result, row[0])

    return result


def mapLabelToGlyphs(font, label):
    result = []

    for char in label:
        result.append(font.glyphs[char])

    return result

CREATE_GLYPHSTABLE_SQL = """
create schema if not exists mg_fonts;
drop table if exists mg_fonts.glyphs;
create table mg_fonts.glyphs (
  id serial,
  name text,
  unicode_name text,
  geom Geometry(Geometry, 5514)
);
"""


if __name__ == "__main__":
    from pygeotoolbox.sharedtools import setupEncoding
    setupEncoding()

    # --svgFileName ArialMT.svg --sqlSelect "select name from osm_query.roads where name is not null group by name order by name;" --readASCII127 --buildLettersRowSQL

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--svgFileName", help="SVF Font file name")
    parser.add_argument("--sqlSelect", help="Sql select for needed chars")
    parser.add_argument("--readASCII127", help="Force enable reading ASCII Base characters", action="store_true")
    parser.add_argument("--buildLettersRowSQL", action="store_true")

    args = parser.parse_args()

    charsToBeLoaded = None
    # --sqlSelect "select name from osm_query.roads where name is not null group by name order by name;"
    if args.sqlSelect:
        log.info('Reading characters from sql "%s"' % args.sqlSelect)
        charsToBeLoaded = getCharactersInSQL(args.sqlSelect)
        log.info("charsToBeLoaded:[%s]" % charsToBeLoaded)

    # --readASCII127
    if charsToBeLoaded and args.readASCII127:
        log.info("Adding ASCII 127 characters...")
        charsToBeLoaded = addCharaters(charsToBeLoaded, getLowerASCII())
        log.info("charsToBeLoaded:[%s]" % charsToBeLoaded)

    charsToBeLoaded = addCharaters(charsToBeLoaded, getLongerASCII())

    #--svgFileName Helvetica-Regular.svg
    #--svgFileName ArialMT.svg
    font = SVGFontReader(args.svgFileName, charsToBeLoaded)

    sql = ""

    if args.buildLettersRowSQL:
        sql += CREATE_GLYPHSTABLE_SQL

        from shapely.affinity import translate

        dx = 0
        for glyph in font.glyphs.values() + mapLabelToGlyphs(font, "Ahoj ty troubelíne jeden!!!"):
            shape = glyph.shape
            if shape:
                shape = translate(shape, dx, 0)
                minx, miny, maxx, maxy = shape.bounds
                dx += 1.2*(maxx - minx)
                sql += "insert into mg_fonts.glyphs(name, unicode_name, geom) values('%s', '%s', st_geometryfromtext('%s', 5514));\n" % (glyph.name, str(glyph.unicode).replace("'", "''"), shape.wkt)

        for glyph in font.glyphs.values():
            if glyph.unicode:
                print hex(ord(glyph.unicode)), ord(glyph.unicode), glyph.unicode
            else:
                print glyph.name


        from pygeotoolbox.database import database
        database.execute(sql)

    if False:
        sql = "select name from osm_query.roads where name is not null group by name order by name;"
        from pygeotoolbox.database import database
        from pygeotoolbox.sharedtools import printEvery100rowsInLongLine
        rows = database.executeSelectSQL(sql)

        sql = "delete from mg_fonts.glyphs;\n"
        y = 500
        rowCount = 0
        for row in rows:
            printEvery100rowsInLongLine(rowCount)
            sql += font.textToSQL(0, y, row[0])
            y += 2000
            rowCount = rowCount + 1

    if sql:
        open("glyphs.sql", "w").write(sql)

