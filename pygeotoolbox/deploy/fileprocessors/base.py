#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"


import codecs, os
import sharedtools.log as log
from pygeotoolbox.sharedtools import saveStrToFile
from deploy.updatemode import UPDATE_MODE
from deploy.dependenciesmanager import dependencies
from deploy.modulelistbuilder import moduleListBuilder



def needsToBeUpdated(sourceFileName, cloneFileName):
    """Returns True if cloneFileName is older than sourceFileName.

    :param sourceFileName: Current version of the file.
    :param cloneFileName: Archive version of the file.
    :return: True if cloneFileName is older than sourceFileName.

    >>> saveStrToFile("c:/temp/source.txt", "Test file.")
    >>> saveStrToFile("c:/temp/clone.txt", "Test file.")
    >>> needsToBeUpdated("c:/temp/source.txt", "c:/temp/clone.txt")
    False
    >>> import os
    >>> os.remove("c:/temp/source.txt")
    >>> os.remove("c:/temp/clone.txt")
    """
    if os.path.exists(cloneFileName):
        return os.path.getmtime(sourceFileName) > os.path.getmtime(cloneFileName)
    else:
        return True


class ProcessFileProcessor:

    def __init__(self, processor, fileName, outputFileName, commentIdentifier = None, encodingIdentifier = None, searchForIsProductionModule = True):
        self.config = None
        self.mode = UPDATE_MODE.OVERWRITE
        self.commentIdentifier = commentIdentifier
        self.encodingIdentifier = encodingIdentifier
        self.headerLines = ""
        self.authorName = ""
        self.description = ""
        self.moduleName = ""
        self.version = ""
        self.fileName = fileName
        self.processor = processor
        self.outputFileName = outputFileName
        self.isProductionModule = not searchForIsProductionModule
        if self.commentIdentifier:
            self.noProductionComment = self.commentIdentifier + " @NO-PRODUCTION CODE"
            self.productionComment = self.commentIdentifier + " @PRODUCTION CODE"
            self.productonModuleComment = self.commentIdentifier + " @PRODUCTION MODULE"
        else:
            self.noProductionComment = None
            self.productionComment = None
            self.productonModuleComment = None


    def getHeaderDict(self):
        result = {}

        if self.config:
            if self.authorName and self.authorName in self.config.authors:
                authorInfo = self.config.authors[self.authorName]
                result.update(authorInfo)

        for caption, value in {
            "Version": self.version,
            "Description": self.description,
            "Module Name": self.moduleName
        }.iteritems():
            if value:
                result[caption] = value

        return result


    def processDependencyLine(self, line):
        line = line.strip().replace(", ", ",").replace("  ", " ")
        lineItems = line.split(" ")
        if lineItems:
            if lineItems[0] == "import":
                modules = lineItems[1].split(",")
                for module in modules:
                    moduleName = module
                    import imp
                    try:
                        imp.find_module(module)
                    except ImportError:
                        dependencies.append(module, self.fileName)


    def processLine(self, builder, line):
        return line


    def getHeader(self):
        return ""


    def processFile(self, directoryProcessor):
        log.logger.openSection("Processing file " + self.fileName)
        isProductionCode = True
        inFile = codecs.open(self.fileName, "r", "utf-8")
        try:
            fileContent = u""
            for line in inFile:
                stripLine = line.strip()
                if self.commentIdentifier and stripLine.startswith(self.commentIdentifier):
                    pass

                if self.encodingIdentifier and stripLine.startswith(self.encodingIdentifier):
                    log.logger.info("Found encoding in %s" % self.fileName)
                    self.headerLines += stripLine + "\n"
                    continue

                if self.commentIdentifier:
                    if stripLine.startswith(self.noProductionComment):
                        log.logger.info("Found no production comment")
                        isProductionCode = False
                        continue

                    if stripLine.startswith(self.noProductionComment):
                        log.logger.info("Found no production comment")
                        isProductionCode = False
                        continue

                    if stripLine.startswith(self.productonModuleComment):
                        log.logger.info("Found production module comment")
                        self.isProductionModule = True
                        continue

                line = self.processLine(directoryProcessor, line)

                if isProductionCode:
                    fileContent += line

            if self.isProductionModule and (
                        self.mode == UPDATE_MODE.OVERWRITE
                        or
                        (self.mode == UPDATE_MODE.UPDATE and needsToBeUpdated(self.fileName, self.outputFileName))
                    ):
                if self.moduleName:
                    moduleListBuilder.addModule(self.moduleName, self.description, self.outputFileName)
                fileContent = self.getHeader() + fileContent
                log.logger.info("Saving file %s %s" % (self.fileName, self.outputFileName))
                directoryProcessor.processedAndSavedFiles.append(self.fileName)
                saveStrToFile(fileContent, self.outputFileName)
            else:
                log.logger.info("File is not production one, skipped!!!")
                directoryProcessor.skippedNoProductionSourceFiles.append(self.fileName)

        finally:
            inFile.close()
        log.logger.closeSection()