#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"


import datetime
import sharedtools.log as log
from base import ProcessFileProcessor

pythonFileHeaderTemplate = """"
#-------------------------------------------------------------------------------
# Name:        #NAME#
# Purpose:     #PURPOSE#
#
# Author:      Ing. Radek Augustýn
# Copyright:   Radek Augustýn, 2018
# License:     MIT
# Version:     1.0.0
#-------------------------------------------------------------------------------
"""


class PythonProcessFileProcessor(ProcessFileProcessor):
    def __init__(self, processor, fileName, outputFileName):
        ProcessFileProcessor.__init__(self, processor, fileName, outputFileName, '#', '#  -*- coding: utf-8 -*-', True)


    def getHeader(self):
        result = self.headerLines
        headerDict = self.getHeaderDict()
        if headerDict:
            result += "\n#-------------------------------------------------------------------------------\n#"
            captionLen = 0
            for caption in headerDict:
                captionLen = max(captionLen, len(caption))
            for caption, value in headerDict.iteritems():
                captionStr = caption
                while len(captionStr) < captionLen:
                    captionStr = captionStr + " "
                result += "\n# %s: %s" % (captionStr, str(value))
            result += "\n#\n#-------------------------------------------------------------------------------"
        return result


    def processLine(self, builder, line):
        stripLine = line.strip()
        if stripLine.startswith("#!"):
            self.headerLines += stripLine + "\n"
            return ""

        if stripLine.startswith("import "):
            self.processDependencyLine(stripLine)
            log.logger.info(line)
        else:
            for (attrIdentifier, attrName) in {
                "__author__" : "authorName",
                "__description__": "description",
                "__moduleName__" : "moduleName",
                "__version__" : "version"
            }.iteritems():
                if stripLine.startswith(attrIdentifier):
                    value = line[line.find("=")+1:].strip()
                    if value.startswith('"') or value.startswith("'"):
                        value = value[1:len(value) - 1]
                    else:
                        value = str(value)
                    setattr(self, attrName, value)
                    line = ""
                    break

        return line

        if stripLine.startswith("from "):
            self.addDependencyLine(stripLine)
            log.logger.info(line)

        return line