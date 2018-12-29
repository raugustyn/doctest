# -*- coding: utf-8 -*-
###########################################################
#                                                         #
# Copyright (c) 2018 Radek Augustýn, licensed under MIT.  #
#                                                         #
###########################################################
# @PRODUCTION MODULE
__author__ = "radek.augustyn@email.cz"


import codecs, os, math, sys


def setupEncoding(encoding = 'utf-8'):
    """ Setup program encoding. Using simple undocumented hack with reloading sys module.

    :param encoding: Selected encoding, if utf-8 is not appropriate.

    >>> setupEncoding("windows_1252")

    """
    assert isinstance(encoding, basestring)

    import sys
    reload(sys)
    sys.setdefaultencoding(encoding)


def strToFloatOrNone(str):
    """Returns float representation of str argument or None if empty string.

    :param str: String to ne converted into float number
    :return: Float representation of str or None.


    >>> print strToFloatOrNone("36")
    36.0

    >>> print strToFloatOrNone("")
    None

    """
    if str:
        return float(str)
    else:
        return None


def sqr(value):
    """ returns square of given value.

    :param {float|int} value: Value to be squared.
    :return: Square value
    :rtype: float

    >>> sqr(4)
    16
    """
    return value*value


def extractFileName(fullFileName):
    """Aliaz to pathLeaf. Extracts file name or directory name from given path.

    :param str fullFileName: Full or relative path
    :return: File name from given path.
    :rtype: str

    >>> extractFileName("c:/temp/test.html")
    'test.html'

    >>> extractFileName("c:/temp/")
    'temp'

    """
    return pathLeaf(fullFileName)


def pathLeaf(path):
    """ Extracts file name or directory name from given path.

    :param str path: Full or relative path
    :return: File name from given path.
    :rtype: str

    >>> pathLeaf("c:/temp/test.html")
    'test.html'

    >>> pathLeaf("c:/temp/")
    'temp'

    """
    import ntpath
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def pathWithLastSlash(path):
    if not path.endswith(os.sep):
        path += os.sep

    return path


def getFileExtension(path):
    """getExtension aliaz. Extracts file extension of the given path.

    :param str path: path or file name
    :return: extension including separator
    :rtype: str

    >>> getFileExtension("c:/temp/test.html")
    '.html'
    """
    return getExtension(path)


def getExtension(path):
    """ Extracts file extension of the given path.

    :param str path: path or file name
    :return: extension including separator
    :rtype: str

    >>> getExtension("c:/temp/test.html")
    '.html'
    """
    (fileName, fileExtension) = os.path.splitext(path)
    return fileExtension


def changeFileExtension(fileName, newExtension):
    """Changes file extension with new one.

    :param str fileName: master file name
    :param str newExtension: new file name extension
    :return: new file name with extension changed.
    :rtype: str


    >>> print changeFileExtension("c:/temp/ahoj.txt", ".sql")
    c:/temp/ahoj.sql

    >>> print changeFileExtension("c:/temp/ahoj.txt", "sql")
    c:/temp/ahoj.sql
    """
    (fileName, fileExtension) = os.path.splitext(fileName)
    if newExtension and not newExtension.startswith('.'):
        newExtension = "." + newExtension
    return  fileName + newExtension


def safeMkDir(path):
    """Creates directory under path if not exists. Unlike os.makedirs, first check it and don't raise error if yes.

    :param str path: Path of the directory to be created


    >>> path = "c:/temp/testdir_1234"
    >>> safeMkDir(path)
    >>> import os
    >>> print os.path.exists(path)
    True
    >>> os.rmdir(path)
    """
    if not os.path.exists(path):
        os.makedirs(path)


def getFileContent(fileName):
    """Reads file content into string. Obsolete function provided for backward compatibility only.
    New code should use fileRead instead.

    :param str fileName: name of the file
    :return: file content as a string
    :rtype: str

    """
    if os.path.exists(fileName) and os.path.isfile(fileName):
        f = open(fileName, "rb")
        s = f.read()
        f.close()
        return s


def fileToStr(fileName, encoding="utf-8", baseFileName=None):
    """fileRead aliaz. Reads file content using encoding specified, utf-8 as default if parameter not provided.

    :param str fileName: name of the file
    :param str encoding: encoding codec name, utf-8 as a default
    :return: file content as a string
    :rtype: str

    >>> content = fileRead(__name__ + ".py")
    >>> print content.startswith("# -*- coding: utf-8 -*-")
    True
    """
    return fileRead(fileName, encoding, baseFileName)


def fileRead(fileName, encoding="utf-8", baseFileName=None):
    """ Reads file content using encoding specified, utf-8 as default if parameter not provided.

    :param str fileName: name of the file
    :param str encoding: encoding codec name, utf-8 as a default
    :return: file content as a string
    :rtype: str

    >>> content = fileRead(__name__ + ".py")
    >>> print content.startswith("# -*- coding: utf-8 -*-")
    True
    """
    if baseFileName:
        fileName = os.path.dirname(baseFileName) + os.sep + fileName

    if os.path.exists(fileName) and os.path.isfile(fileName):
        file = codecs.open(fileName, "r", "utf-8")
        result = file.read()
        file.close()
        return result


def pairItems(iterator):
    """Returns new iterator with subsequent tupple pairs of source iterator.
    I could be used for example for converting list of vertexes in a linestring to list of edges.

    :param iterator: Iterator for join pairs
    :return: Pairs iterator

    >>> pairs = pairItems([1, 2, 3, 4, 5])
    >>> for item in pairs:print item
    (1, 2)
    (2, 3)
    (3, 4)
    (4, 5)
    """
    firstItem = None
    for item in iterator:
        if firstItem:
            yield (firstItem, item)
        firstItem = item


def replaceStringBlocks(str, startId, endId, newContent):
    """ Replaces all string sections in blocks given by startId and endId tags by newContent.

    :param str str: Text content to be updated.
    :param str startId: Start identifier of the block to be replaced.
    :param str endId: End identifier of the block to be replaced.
    :param str newContent: New text content.
    :return: Updated str block.
    :rtype: str


    >>> replaceStringBlocks("Text pred.<ReplaceStart>StaryText<ReplaceEnd>Text za.", "<ReplaceStart>", "<ReplaceEnd>", "Next content.")
    'Text pred.Next content.Text za.'

    """
    endPos = 0
    while True:
        startPos = str.find(startId, endPos)
        endPos = str.find(endId, startPos)
        if startPos<0 or endPos<startPos:
            break

        str = str[:startPos] + newContent + str[endPos + len(endId):]

    return str


def setParameters(template, parameters):
    """Replace values in a template string by given real values dictionary. Used mainly for SQL queries,
    enabling leave them working for copy&paste debugging.

    :param str template: template string with identifiers to be replaced
    :param dict parameters: dictionary where keys are identifiers in a template which have to be replaced by values
    :return str: template string with replaced values
    :rtype: str

    >>> template = "select ogc_fid from public.z_terrenrelief_l"
    >>> str = setParameters(template, { "ogc_fid": "zrdoj_id", "public" : "temp"})
    >>> print str
    select zrdoj_id from temp.z_terrenrelief_l
    """
    if parameters:
        keys = sorted(parameters.keys())
        for key in keys:
            template = template.replace(key, str(parameters[key]))

    return template


def makeDir(dirName):
    """Creates directory dirName if not exists.

    :param str dirName: Directory to be created.

    >>> makeDir("c:/temp/testMakeDir")
    >>> os.path.exists("c:/temp/testMakeDir")
    True
    >>> os.rmdir("c:/temp/testMakeDir")
    """
    if dirName and not os.path.exists(dirName):
        os.makedirs(dirName)


def makeDirForFile(fileName):
    """ Create directory for storing file if not exists.

    :param str fileName: Name of the file for creating directory.

    >>> makeDirForFile("c:/temp/testMakeDirForFile/testfile.txt")
    >>> os.path.exists("c:/temp/testMakeDirForFile")
    True
    >>> os.rmdir("c:/temp/testMakeDirForFile")

    """
    makeDir(os.path.dirname(fileName))


def saveStrToFile(str, fileName, encoding = "utf-8"):
    """ Saves given string str into file fileName using encoding parameter.

    :param str str: String to be saved.
    :param str fileName: Name of the created file.
    :param str encoding: Character encoding, utf-8 as defatult.

    >>> saveStrToFile("Ahoj", "c:/temp/testSaveToStr.txt")
    >>> import os
    >>> os.path.exists("c:/temp/testSaveToStr.txt")
    True
    >>> # Cleaning after test
    >>> os.remove("c:/temp/testSaveToStr.txt")
    """
    makeDirForFile(fileName)
    outputFile = codecs.open(fileName, "w", encoding)
    outputFile.write(str)
    outputFile.close()


def saveJSONtoJavaScript(obj, identifier, javaScriptFileName):
    """ Saves obj to the JavaScript file as a identifier variable.

    :param dict obj: object to be saved
    :param str identifier: JavaScript reference variable name
    :param str javaScriptFileName: JavaScript file name

    >>> obj = { "value" : 3 }
    >>> saveJSONtoJavaScript(obj, "testValue", "c:/temp/test.js")
    >>> print open("c:/temp/test.js", "r").read()
    testValue = {
        "value": 3
    }
    >>> os.remove("c:/temp/test.js")

    """
    from json import dumps

    jsonString = "%s = %s" % (identifier, dumps(obj, indent=4, ensure_ascii=False).encode('utf-8'))
    saveStrToFile(jsonString, javaScriptFileName)


def saveDictToJSON(obj, fileName):
    from json import dumps

    if not getFileExtension(fileName):
        fileName = fileName + ".json"

    saveStrToFile(dumps(obj, indent=4, ensure_ascii=False).encode('utf-8'), fileName)


def getMessageIfFalse(condition, msg):
    """If condition is False, then returns msg, otherwise returns empty string.

    :param bool condition: Condition paramater.
    :param str msg: Message returned if condition is False.
    :return: msg or empty string.
    :rtype: str


    >>> getMessageIfFalse(False, "Condition is set to False.")
    'Condition is set to False.'

    """
    if condition:
        return ""
    else:
        return msg


def getTrueFalseMessage(condition, trueMessage, falseMessage):
    """Returns trueMessage if condition is True, otherwise returns falseMessage.

    :param bool condition: condition parameter
    :param str trueMessage: True case string message
    :param str falseMessage: False case string message
    :return: appropriate message string
    :rtype: str

    >>> getTrueFalseMessage(True, "Condition is True", "Condition is False")
    'Condition is True'

    """
    if condition:
        return trueMessage
    else:
        return falseMessage


def formatValueIfNotEmpty(template, value):
    """Formats value if template is given, if not, the just convert it into string. Returns empty string if value is None.

    :param str template: string formating template
    :param str value: value to be formated
    :return: formatted value
    :rtype: str

    >>> formatValueIfNotEmpty("%3.1f", 8.54684)
    '8.5'

    >>> formatValueIfNotEmpty("%f3.1", None)
    ''

    """
    if value:
        if template.find('%') >= 0:
            return template % value
        else:
            return template
    else:
        return ""


class Container:
    """Empty class holding values. Pascal record or CPP union equivalent. """
    def __init__(self, fieldNamesOrFields=None, fields={}, fieldNames=[]):
        if fieldNamesOrFields:
            if isinstance(fieldNamesOrFields, list):
                fieldNames = fieldNamesOrFields
            elif isinstance(fieldNamesOrFields, dict):
                fields = fieldNamesOrFields

        if fields:
            for fieldName, fieldValue in fields.iteritems():
                setattr(self, fieldName, fieldValue)

        if fieldNames:
            for fieldName in fieldNamesOrFields:
                setattr(self, fieldName, None)


def searchForFileAtPath(deepestPath, fileName):
    """Search for file at path. Used mainly to find config file at highest level (shortest path)

    :param str deepestPath: path to start search at
    :param str fileName:  file name to be searched for
    :return: tupple (found, fullFileName)
    :rtype: tupple

    """
    deepestPath = os.path.normpath(deepestPath)
    pathItems = deepestPath.split(os.sep)
    pathLen = len(pathItems)
    while pathLen > 1:
        fullFileName = os.sep.join(pathItems[:pathLen]) + os.sep + fileName
        if os.path.exists(fullFileName):
            return (True, fullFileName)

        pathLen = pathLen - 1

    return (False, deepestPath + os.sep + fileName)


def listToSqlStr(values):
    """Converts list items into SQL list sequence.

    :param list values: list of value to be converted into SQL list sequence
    :return: SQL list values representation
    :rtype: str

    >>> listToSqlStr([4, 5, "Ahoj"])
    "(4, 5, 'Ahoj')"
    """
    return str(values).replace("[", "(").replace("]", ")").replace('"', "'")


def listToSqlFieldList(values):
    """Converts list items into SQL list sequence.

    :param list values: list of value to be converted into SQL field list sequence
    :return: SQL field list values representation
    :rtype: str

    >>> listToSqlFieldList([4, 5, "Ahoj"])
    "4, 5, 'Ahoj'"
    """
    return str(values).replace("[", "").replace("]", "").replace("'", "")


def listToSqlValuesList(values):
    """Converts values list into SQL values list sequence.

    :param list values: list of value to be converted into SQL values list sequence
    :return: SQL values list representation
    :rtype: str

    >>> listToSqlValuesList([4, None, "Ahoj", 4.56])
    "4, Null, 'Ahoj', 4.56"
    """
    result = []
    for value in values:
        if isinstance(value, basestring):
            if value.startswith('st_geometryfromtext'):
                result.append("%s" % str(value))
            else:
                result.append("'%s'" % str(value))
        elif value == None:
            result.append("Null")
        else:
            result.append(str(value))

    return ", ".join(result)


def getTableHTML(rows):
    """ Binds rows items into HTML table code.

    :param list rows: an array of row items
    :return: HTML table code with items at rows
    :rtype: str


    >>> getTableHTML([["Name", "Radek"], ["Street", "Chvalinska"]])
    '<table><tr><td>Name</td><td>Radek</td></tr><tr><td>Street</td><td>Chvalinska</td></tr><table>'
    """
    if rows:
        result = "<table>"
        for row in rows:
            result += "<tr>"
            for item in row:
                result += "<td>%s</td>" % item
            result += "</tr>"
        result += "<table>"
        return result
    else:
        return ""


def dump(shape):
    """ An equivalent of PostGIS st_dump command for shapely geometry. Returns first geom of shape or shape if not compoment element.

    :param shapely.geometry.base.BaseGeometry shape: Shapely geometry to be dumped.
    :return: First geom of shape or shape if not compoment element.


    >>> from shapely.geometry import Point, MultiPoint
    >>> multiPoint = MultiPoint([Point(4, 1)])
    >>> dump(multiPoint).wkt
    'POINT (4 1)'
    >>> dump(Point(5, 7)).wkt
    'POINT (5 7)'

    """
    if hasattr(shape, "geoms") and len(shape.geoms) == 1:
        return shape.geoms[0]
    else:
        return shape


def geomsEnumerator(shape):
    if hasattr(shape, "geoms"):
        if len(shape.geoms) == 1:
            return shape.geoms[0]
        else:
            return shape.geoms
    else:
        return [shape]


def numIntersections(proxyLine, endPoint, shape):
    result = 0
    for intersectionPoint in geomsEnumerator(proxyLine.intersection(shape)):
        if endPoint.distance(intersectionPoint) > 0.1:
            result += 1
    return result


def createContainer(values):
    """ Create container for szmbolic values, equivalent of Pascal record or C struct commands.

    :param list values: values to be added as container properties
    :return: class instance with given properties
    :rtype: Container

    >>> a = createContainer({ "floatNumber": 3, "stringValue": "Test"})
    >>> print a.__class__
    base.Container
    >>> print a.floatNumber, a.stringValue
    3 Test
    """
    class Container:pass

    result = Container()
    for key, value in values.iteritems():
        setattr(result, key, value)

    return result


def sign(a):
    """ @TODO Check, doc or remove.
    """
    return (a > 0) - (a < 0)


def maxWithNone(a, b):
    """ Returns maximal value from two values, if any of them is None, returns other one.

    :param a: int, float or None value
    :param b: int, float or None value
    :return: class instance with given properties
    >>> maxWithNone(None, 1)
    1
    """
    if a == None:
        return b
    elif b == None:
        return a
    else:
        return max(a, b)



def minWithNone(a, b):
    """ Returns minimal value from two values, if any of them is None, returns other one.

    :param a: int, float or None value
    :param b: int, float or None value
    :return: class instance with given properties
    >>> minWithNone(None, 1)
    1
    """
    if a == None:
        return b
    elif b == None:
        return a
    else:
        return min(a, b)


class __DummySelfExplainingClass:
    pass


SelfExplainingClass = __DummySelfExplainingClass


def angleToStr(angle):
    """Returns string representation of angle given in radians.

    :param float angle: angle in radians
    :return: string representation.
    :rtype: str

    >>> angleToStr(math.pi)
    '180.0'
    """
    return str(180*angle/math.pi)


def normalizeAngle(angle, maxValue = math.pi):
    """Returns angle in interval <0, maxValue>.

    :param float angle: angle in radians
    :param float maxValue:  circle value
    :return: angle in interval <0, maxValue>
    :rtype: float
    """
    assert isinstance(angle, float)
    assert isinstance(maxValue, float)

    while angle < 0:
        angle += maxValue

    while angle > maxValue:
        angle -= maxValue

    return angle


def copyAttributes(source, target, attributes):
    """ Copy object instance attributes to other instance.

    :param object source: Source instance.
    :param object target: Target instance.
    :param list attributes:  Copied attribute names.

    """
    for attribute in attributes:
        if hasattr(source, attribute):
            setattr(target, attribute, getattr(source, attribute))


def copyAttributesToItems(source, items, attributes):
    """Copies given attribute values into list of objects.

    :param object source: source instance
    :param list items: target items list
    :param list attributes: copied attribute names

    """
    assert isinstance(items, list)

    for item in items:
        copyAttributes(source, item, attributes)


def extendListNoDuplicates(listToBeExtended, newItems):
    """Extend list with items without duplicities.

    :param list listToBeExtended: list to be extended
    :param list newItems: new items
    :return: extended list
    :rtype: list

    >>> extendListNoDuplicates([1, 2, 3, 4], [4, 5, 6])
    [1, 2, 3, 4, 5, 6]
    """
    for item in newItems:
        if not item in listToBeExtended:
            listToBeExtended.append(item)

    return listToBeExtended


def safeRemoveItemsFromList(listWithItems, itemsToBeRemoved):
    """Removes items from other list with check if it is inside.

    :param list listWithItems: list to be updated
    :param list itemsToBeRemoved: items to be removed
    :return: list without items
    :rtype: list

    >>> safeRemoveItemsFromList([1, 2, 3, 4], [2, 5])
    [1, 3, 4]

    """
    if itemsToBeRemoved:
        for item in itemsToBeRemoved:
            if item in listWithItems:
                listWithItems.remove(item)

    return listWithItems


class WellKnownClass:
    DEFAULT_LANGUAGE = "CZ"
    LANGUAGE = DEFAULT_LANGUAGE

    """Named base class with description. """
    def __init__(self, name, description = ""):
        assert isinstance(name, basestring)
        assert isinstance(description, basestring)

        self.name = name
        self.__description = description
        self.descriptions = {}
        if description:
            print description, description.split("|")
            if len(description.split("|")) > 1:
                pass
            for item in description.split("|"):
                subItems = item.split('::')
                if len(subItems) > 1:
                    itemLanguage = subItems[0].strip()
                    itemDescription = "::".join(subItems[1:])
                else:
                    itemLanguage = WellKnownClass.DEFAULT_LANGUAGE
                    itemDescription = item

                self.descriptions[itemLanguage] = itemDescription
                print "\t", itemLanguage, "'%s'" % itemDescription


    @property
    def description(self):
        if self.descriptions:
            result = self.descriptions.get(WellKnownClass.LANGUAGE, None)
            if not result:
                result = self.descriptions.get(WellKnownClass.DEFAULT_LANGUAGE, None)
            if not result:
                result = self.descriptions.values()[0]
        else:
            result = ''

        return result


    def __repr__(self):
        return "%s('%s', '%s')" % (self.__class__.__name__, self.name, self.description)


    def asDict(self, deep=True):
        """Convert instance into dictionary.

        :param bool deep: if True, it will convert recursive
        :return: dictionary representation of the object
        :rtype: dict
        """
        result = {
            "name": self.name,
            "description": self.description
        }

        if hasattr(self, "asCodeSample"):
            from pygeotoolbox.sharedtools.python2html import convertCode
            result["codeSampleHTML"] = convertCode(self.asCodeSample())

        return result


    def asJSON(self, deep=True):
        """Converts instance into JSON.

        :param bool deep: if True, it will convert recursive
        :return: JSON representation of the object
        :rtype: str
        """
        from json import dumps

        return dumps(self.asDict(), indent=4).decode('unicode-escape').encode('utf8')


    def asCodeSample(self):
        """Returns code sample representation of the instance. """
        return "%s('%s', '%s')" % (self.__class__.__name__, self.name, self.description)


    def saveAsJavaScriptVariable(self, fileName, variableName=""):
        """Creates JavaScript file with instance content in variableName.

        :param str fileName: JavaScript file name
        :param str variableName: variable name in JavaScript file created
        """
        from pygeotoolbox.sharedtools import saveStrToFile
        import log

        log.info("Saving %s to %s" % (self.name, fileName))
        if not variableName:
            variableName = self.__class__.__name__
            variableName = variableName[:1].lower() + variableName[1:]

        saveStrToFile("var %s=%s;" %(variableName, self.asJSON()), fileName)


def variantCombinations(items):
    """ Calculates variant combinations for given list of options. Each item in the items list represents
    unique value with it's variants.

    :param list items: list of values to be combined

    >>> c = variantCombinations([["1.1", "1.2"], ["2.1", "2.2"], ["3.1", "3.2"]])
    >>> len(c)
    8
    >>> for combination in c:print combination
    ['1.1', '2.1', '3.1']
    ['1.1', '2.1', '3.2']
    ['1.1', '2.2', '3.1']
    ['1.1', '2.2', '3.2']
    ['1.2', '2.1', '3.1']
    ['1.2', '2.1', '3.2']
    ['1.2', '2.2', '3.1']
    ['1.2', '2.2', '3.2']

    """
    assert isinstance(items, list) and list

    if len(items) == 1:
        result = items[0]
    else:
        result = []
        subItems = variantCombinations(items[1:])
        for masterItem in items[0]:
            for subItem in subItems:
                if isinstance(subItem, list):
                    item = [masterItem]
                    item.extend(subItem)
                    result.append(item)
                else:
                    result.append([masterItem, subItem])

    return result


def getPathRelativeToFile(fileName, path):
    """Returns absolute path relative to given fileName.

    :param str fileName: file name to be relative to
    :param str path: relative path
    :return: requested absolute path
    :rtype: str

    >>> getPathRelativeToFile('c:/temp/exapleFile.py', './path01/path02/sample.txt')
    'c:/temp/path01/path02/sample.txt'

    """
    targetPath = os.path.join(os.path.dirname(fileName), path)
    targetPath = os.path.normpath(targetPath)

    return targetPath


def getPathRelativeToScript(path):
    return getPathRelativeToFile(sys.argv[0], path)


def pythonVariableCase(s):
    if not s:
        return s
    else:
        return s[0].lower() + s[1:]


def splitOrEmptyList(s, identifier):
    if s.find(identifier) >= 0:
        return filter(lambda x:x <> None and x <> '', s.split(identifier))
    else:
        return []


from shapely.geometry.base import BaseGeometry
setattr(BaseGeometry, "dump", dump)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    if False:
        from shapely.geometry import Point, MultiPoint

        print MultiPoint([Point(4, 1)]).dump()
        print MultiPoint([Point(4, 1), Point(4, 6)]).dump()