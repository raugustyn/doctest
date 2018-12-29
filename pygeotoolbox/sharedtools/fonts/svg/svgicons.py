#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"


from pygeotoolbox.sharedtools.fonts.svg.svgfontreader import SVGFontReader
import pygeotoolbox.sharedtools.log as log
from pygeotoolbox.sharedtools import makeDirForFile

__readers = {}

def extractSVGIcon(svgFontFileName, glyphName, iconFileName=None):
    global __readers

    if not svgFontFileName in __readers:
        __readers[svgFontFileName] = SVGFontReader(svgFontFileName)

    reader = __readers[svgFontFileName]
    for glyphUnicode, glyph in reader.glyphs.iteritems():
        if glyphName == glyph.name:
            result = '<?xml version="1.0"?>\n<svg>\n\t%s\n</svg>' % glyph.glyphXMLContent.replace("glyph", "path")
            if iconFileName:
                makeDirForFile(iconFileName)
                open(iconFileName, "w").write(result)
                log.debug("Saving icon '%s' --> '%s'." % (glyphName, iconFileName))
            return result

    log.warning("extractSVGIcon('%s', '%s', '%s') - glyph [%s] not found." % (svgFontFileName, glyphName, str(iconFileName), glyphName))
    return ""


if __name__ == "__main__":
    extractSVGIcon("C:/ms4w/Apache/htdocs/Generalizace/MapGen/projects/zm/zm10/zm10fonts/zm10x1.svg", "105_kostel", "C:/ms4w/Apache/htdocs/Generalizace/MapGen/ms4w/Apache/htdocs/mgFiddle/Maps/zm10/105_kostel.svg")
