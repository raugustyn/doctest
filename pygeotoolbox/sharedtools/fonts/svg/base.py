#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"


def getLowerASCII():
    """Returns lower 127 characters from ASCII code table, starting from space (no control characters like CR, LF etc).

    :return: String Returns lower 127 characters from ASCII code table, starting from space (no control characters like CR, LF etc).

    >>> getLowerASCII()
    u' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f'
    """
    result = u""

    index = ord(' ')
    while index <= 127:
        result += chr(index)
        index = index + 1
    return result



def getLongerASCII():
    """Returns lower 255 characters from ASCII code table, starting from space (no control characters like CR, LF etc).

    :return: String Returns lower 127 characters from ASCII code table, starting from space (no control characters like CR, LF etc).

    >>> getLowerASCII()
    u' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f'
    """
    result = u""

    index = ord(' ')
    while index <= 255:
        result += chr(index)
        index = index + 1
    return result


def addCharaters(chars, charsToBeAdded):
    """Adds characters from charsToBeAdded param into chars param, if they are not there already. Result is sorted unicode string out.

    :param Unicode chars:
    :param Unicode charsToBeAdded:
    :return: Unicode sorted union of chars and charsToBeAdded parameters.

    >>> addCharaters('A', 'CDEF')
    u'ACDEF'

    """
    result = chars

    if isinstance(charsToBeAdded, list):
        for item in charsToBeAdded:
            result = addCharaters(result, item)
    else:
        if not isinstance(charsToBeAdded, unicode):
            charsToBeAdded = unicode(charsToBeAdded, "utf-8")
        for char in charsToBeAdded:
            if not char in result:
                result += char

    result = "".join(sorted(result))
    return result


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __repr__(self):
        return "Point(%f, %f)" % (self.x, self.y)


    def equals(self, point):
        return self.x == point.x and self.y == point.y


def extractParam(tag, paramName, defValue=""):
    import urllib

    paramPrefix = ' %s="' % paramName
    startPos = tag.find(paramPrefix)
    if startPos == -1:
        return defValue

    startPos = startPos + len(paramPrefix)
    endPos = tag.find('"', startPos)
    if endPos == -1:
        return defValue

    return urllib.unquote(tag[startPos: endPos])


def strToListByKeys(str, keys):
    """

    :param str:
    :param keys:
    :return:

    >>> strToListByKeys('M43 662q0 -29 19.5 -48.5t48.5 -19.5t48.5 19.5t19.5 48.5t-19.5 48.5t-48.5 19.5t-48.5 -19.5t-19.5 -48.5zM-2 662q0 23 9 43.5t24.5 36t36 24.5t43.5 9t43.5 -9t36 -24.5t24.5 -36t9 -43.5t-9 -43.5t-24.5 -36t-36 -24.5t-43.5 -9t-43.5 9t-36 24.5t-24.5 36t-9 43.5z', pathElements.keys())

    """
    result = []
    lastFoundKey = None
    while str <> "":
        foundKey = None
        foundKeyPos = None
        for key in keys:
            keyPos = str.find(key)
            if keyPos <> -1 and (not foundKey or (foundKey and foundKeyPos > keyPos)):
                foundKey = key
                foundKeyPos = keyPos

        if foundKey:
            lastKeyValue = str[:foundKeyPos]
            str = str[foundKeyPos + len(foundKey):]
        else:
            lastKeyValue = str
            str = ""
        if lastFoundKey:
            result.append((lastFoundKey, lastKeyValue))
        lastFoundKey = foundKey

    return result



def getPathVertexes(d, precision):
    """

    :param d:
    :param precision:
    :return:

    >>> d = "M828 131q-100 -85 -192.5 -120t-198.5 -35q-175 0 -269 85.5t-94 218.5q0 78 35.5 142.5t93 103.5t129.5 59q53 14 160 27q218 26 321 62q1 37 1 47q0 110 -51 155q-69 61 -205 61q-127 0 -187.5 -44.5t-89.5 -157.5l-176 24q24 113 79 182.5t159 107t241 37.5 q136 0 221 -32t125 -80.5t56 -122.5q9 -46 9 -166v-240q0 -251 11.5 -317.5t45.5 -127.5h-188q-28 56 -36 131zM813 533q-98 -40 -294 -68q-111 -16 -157 -36t-71 -58.5t-25 -85.5q0 -72 54.5 -120t159.5 -48q104 0 185 45.5t119 124.5q29 61 29 180v66z"
    >>> print getPathVertexes(d, 10)
    """
    from svgpathtools import parse_path

    result = []
    if d[len(d) - 1:] == "z":
        d = d[:len(d) - 1]

    for subString in d.split("z"):
        subPath = parse_path(subString)
        vertexes = []
        if subPath.length() > 0:
            step = precision/subPath.length()

            pos = 0
            while pos <= 1:
                p = subPath.point(pos)
                vertexes.append(Point(p.real, p.imag))
                pos += step
            if pos <> 1:
                p = subPath.point(1)
                vertexes.append(Point(p.real, p.imag))

            startVertex = vertexes[0]
            if not startVertex.equals(vertexes[len(vertexes)-1]):
                vertexes.append(Point(startVertex.x, startVertex.y))

            result.append(vertexes)

    if len(result) == 1:
        result = result[0]

    return result

