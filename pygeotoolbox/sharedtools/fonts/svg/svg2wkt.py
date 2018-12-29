#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"
# https://github.com/davidmcclure/svg-to-wkt/blob/master/svg-to-wkt.js

import math


PRECISION = 3
DENSITY = 1


def __round(val):
    """
    Round a number to the number of decimal places in `PRECISION`.

    :param {Number} val: The number to round.
    :return {Number}: The rounded value.
    """
    root = math.pow(10, PRECISION)
    return math.round(val * root) / root


def swapDelimeters(points):
    # "1,2 3,4 " = > "1 2,3 4"
    points = points.strip()
    points = points.replace(" ", "::")
    points = points.replace(",", " ")
    points = points.replace("::", ",")

    return points


def extractParam(tag, paramName):
    import urllib

    paramPrefix = '%s="' % paramName
    startPos = tag.find(paramPrefix) + len(paramPrefix)
    endPos = tag.find('"', startPos)

    return urllib.unquote(tag[startPos: endPos])


def polygon(points):
    """
    Construct a WKT polygon from SVG `points` attribute value.

    :param {String} points: <polygon> `points` attribute value.
    :return {String}: Generated WKT.

    :public
    """
    points = swapDelimeters(points).split(",")
    points.append(points[0])
    points = ",".join(points)

    return 'POLYGON((' + points + '))';


def polyline(points):
    """
    Construct a WKT linestrimg from SVG `points` attribute value.

    @param {String} points: <polyline> `points` attribute value.
    @return {String}: Generated WKT.

    @public
    """

    return 'LINESTRING(' + swapDelimeters(points) + ')';



def line(x1, y1, x2, y2):
    """
    Construct a WKT line from SVG start/end point coordinates.

    :param {Number} x1: Start X.
    :param {Number} y1: Start Y.
    :param {Number} x2: End X.
    :param {Number} y2: End Y.
    :return {String}: Generated WKT.

    :public
    """
    return 'LINESTRING(%f %f, %f %f)' % (x1, y1, x2, y2)



def rect(x, y, width, height):
    """
    Construct a WKT polygon from SVG rectangle origin and dimensions.

    :param {Number} x: Top left X.
    :param {Number} y: Top left Y.
    :param {Number} width: Rectangle width.
    :param {Number} height: Rectangle height.
    :return {String}: Generated WKT.

    :public
    """
    points = []
    for item in [
            (x, y),
            (x + width, y),
            (x + width, y + height),
            (x, y + height)
        ]:
        points.append("%f %f" % (item[0], item[1]))

    return polygon(",".join(points))


def path(d):
    print "PATH:('%s')" % d
    pass


def glyph(d):
    return path(d)


def convert(svg):

    elements = []

    def forEach(tagName, processor):
        startPos = 0
        while startPos < len(svg):
            startPos = svg.find('<' + tagName, startPos)
            if startPos >= 0:
                startPos += len(tagName)
                endPos = svg.find("/>", startPos) + 2
                tag = svg[startPos:endPos]
                #name = extractParam(tag, "glyph-name")
                #unicode = extractParam(tag, "unicode")
                #xOrigin = extractParam(tag, "horiz-adv-x")
                #print name, unicode, xOrigin
                processor(tag)
                startPos = endPos
            else:
                break

    forEach('polygon', lambda content:polygon(extractParam(content, "points")))
    forEach('polyline', lambda content:polyline(extractParam(content, "points")))
    forEach('line', lambda content:line(extractParam(content, "x1"), extractParam(content, "y1"), extractParam(content, "x2"), extractParam(content, "y2")))
    forEach('rect', lambda content:rect(extractParam(content, "x"), extractParam(content, "y"), extractParam(content, "width"), extractParam(content, "height")))
    forEach('path', lambda content:path(extractParam(content, "d")))
    forEach('glyph', lambda content:path(extractParam(content, "d")))

    if len(elements) == 1:
        return elements[0]
    else:
        return 'GEOMETRYCOLLECTION(' + ",".join(elements) + ')'


if __name__ == "__main__":

    #print polyline("1,2 3,4 ")
    #print polygon("1,2 3,4 ")
    #print line(10, 15, 34, 45)
    #print rect(10, 12, 35, 8)

    convert(open("Helvetica-Regular.svg", "r").read().replace('\n', ''))