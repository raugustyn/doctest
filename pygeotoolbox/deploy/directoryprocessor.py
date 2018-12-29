#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"


import os, shutil
from pygeotoolbox.sharedtools import normalizePath, getExtension, makeDirForFile
import sharedtools.log as log
from modulelistbuilder import moduleListBuilder
from updatemode import UPDATE_MODE
from dependenciesmanager import dependencies


class DirectoryProcessor:
    def __init__(self, path, outputPath, config):
        self.config = config
        self.mode = UPDATE_MODE.OVERWRITE
        self.sourcePath = os.path.normpath(path)
        self.targetPath = os.path.normpath(outputPath)
        self.sourcePathLength = len(self.sourcePath) + 1
        self.targetPathLength = len(self.targetPath) + 1
        self.copiedFiles = []
        self.simplySkippedFiles = []
        self.skippedNoProductionSourceFiles = []
        self.processedAndSavedFiles = []
        self.analysedSourceFileNames = []


    def deploy(self):
        dependencies.basePath = self.sourcePath
        moduleListBuilder.clear()
        if os.path.exists(self.targetPath):
            shutil.rmtree(self.targetPath)
        self.copiedFiles = []
        self.simplySkippedFiles = []
        self.skippedNoProductionSourceFiles = []
        self.processedAndSavedFiles = []
        self.analysedSourceFileNames = []
        self.processDirectory(self.sourcePath, self.targetPath)
        moduleListBuilder.saveToFile(self.targetPath + os.sep + "modules.html")


    def relativizeTargetPath(self, path):
        return path[self.targetPathLength:]


    def relativizeSourcePath(self, path):
        return path[self.sourcePathLength:]


    def processDirectory(self, path, outputPath, prefix = ''):
        log.logger.openSection("Directory" + prefix + path)
        for dirItem in os.listdir(path):
            itemPath = path + os.sep + dirItem
            if os.path.isdir(itemPath):
                if not dirItem in self.config.skipedDirectories:
                    self.processDirectory(itemPath, outputPath + os.sep + dirItem, prefix + '  ')
            elif os.path.isfile(itemPath):
                if getExtension(itemPath) in self.config.skippedExtensions:
                    pass
                else:
                    if itemPath in self.analysedSourceFileNames:
                        continue
                    else:
                        self.processFile(itemPath, outputPath + os.sep + dirItem)
            else:
                pass # islink, ismount intentionally skip
        log.logger.closeSection()


    def processFile(self, fileName, outputFileName):
        extension = getExtension(fileName)
        processorFound = False

        for key, processorClass in self.config.data.iteritems():
            if key == extension:
                processorFound = True
                if processorClass:
                    processor = processorClass(self, fileName, outputFileName)
                    processor.mode = self.mode
                    processor.config = self.config
                    processor.processFile(self)
                    self.analysedSourceFileNames.append(fileName)
                else:
                    log.logger.info("Skipping " + fileName)
                    self.simplySkippedFiles.append(fileName)

        if not processorFound:
            makeDirForFile(outputFileName)
            log.logger.info("%s->%s" % (self.relativizeSourcePath(fileName), self.relativizeTargetPath(outputFileName)))
            shutil.copyfile(fileName, outputFileName)
            self.copiedFiles.append(fileName)


    def printStatistics(self):
        def printList(message, listToBePrinted):
            log.logger.openSection("%s (%d):" % (message, len(listToBePrinted)))
            for fileName in listToBePrinted:
                log.logger.info(self.relativizeSourcePath(fileName))
            log.logger.closeSection()

        statistics = {
            "processedAndSavedFiles" : self.processedAndSavedFiles,
            "skippedNoProductionSourceFiles" : self.skippedNoProductionSourceFiles,
            "simplySkippedFiles" : self.simplySkippedFiles,
            "copiedFiles" : self.copiedFiles
        }

        for message, listToBePrinted in statistics.iteritems():
            printList(message, listToBePrinted)

        for message, listToBePrinted in statistics.iteritems():
            log.logger.info("%d in %s" % (len(listToBePrinted), message))

        if True:
            log.logger.openSection("Dependencies:")
            for dependency in dependencies.dependencies:
                log.logger.info(str(dependency))
            log.logger.closeSection("%d dependencies found in total." % len(dependencies.dependencies))


            log.logger.openSection("Packages:")
            packages = dependencies.getPackages()
            for packageName in packages:
                log.logger.info(packageName)
            log.logger.closeSection("%d packages found in total." % len(packages))
