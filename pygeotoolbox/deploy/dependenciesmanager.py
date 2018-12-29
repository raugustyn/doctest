#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"

import os
from pygeotoolbox.sharedtools import normalizePath

class DependenciesManager(object):
    def __init__(self):
        self.dependencies = []
        self._basePath = None
        self.__iterIndex = 0

    def __getDependency(self):
        if self.__iterIndex >= len(self.dependencies):
            return None
        else:
            return self.dependencies[self.__iterIndex]

    def __iter__(self):
        self.__iterIndex = 0
        return self.__getDependency()

    def __next__(self):
        self.__iterIndex += 1
        return self.__getDependency()

    def append(self, module, fileName):
        fileName = os.path.abspath(fileName)
        filePath = os.path.dirname(fileName) + os.sep
        if module.find(".") < 0 and filePath <> self.basePath:
            modulePath = filePath[len(self.basePath):]
            module = modulePath.replace(os.sep, ".") + module
        self.dependencies.append((module, fileName))

    def clear(self):
        self.dependencies = []

    @property
    def basePath(self):
        return self._basePath

    @basePath.setter
    def basePath(self, basePath):
        self._basePath = normalizePath(basePath)
        self.clear()


    def isRegistered(self, module):
        for (registeredModuleName, fileName) in self.dependencies:
            if registeredModuleName == module:
                return True

        return False

    def extractPackageName(self, moduleName):
        items = moduleName.split(".")
        return ".".join(items[:len(items)-1])

    def getPackages(self):
        result = []

        for module, fileName in self.dependencies:
            package = self.extractPackageName(module)
            if not package in result:
                result.append(package)

        return result


dependencies = DependenciesManager()