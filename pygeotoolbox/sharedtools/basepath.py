#  -*- coding: utf-8 -*-
###########################################################
#                                                         #
# Copyright (c) 2018 Radek Augustýn, licensed under MIT.  #
#                                                         #
###########################################################
__author__ = "radek.augustyn@email.cz"
# @PRODUCTION MODULE

import os, sys

# ##########################################################################################
#
# Following sequence ensures that packages path is registered into Python environment.
# It searches in the current directory or it's parent directories file manager.py.
# If not found, then current directory assumed as basePath.
#
# ##########################################################################################

basePath = None


def setupBasePath(pathOrFile, basePathFileName = "README.md"):
    """Setup basePath value according pathOrFile aparameter.

    :param pathOrFile:
    :return: basePath value.
    """
    global basePath

    if os.path.isfile(pathOrFile):
        basePath = os.path.dirname(pathOrFile)
    else:
        basePath = pathOrFile
    basePath = os.path.normpath(basePath)
    basePath = basePath.replace("/", os.sep)

    basePathItems = basePath.split(os.sep)
    while basePathItems and not os.path.exists(os.sep.join(basePathItems) + os.sep + basePathFileName):
        basePathItems = basePathItems[:len(basePathItems)-1]

    if basePathItems:
        basePath = os.sep.join(basePathItems)

    if not basePath in sys.path:
        sys.path.append(basePath)


    return basePath


def normalizePath(relativePath):
    """Path normalizer for template and configuration files.  It will create full path for the file, relativePath is addressed to
    the directory one level higher than this module.

    :param relativePath: RelativePath, addressed to the directory one level higher than this module.
    :return: Absolute path of the relativePath parameter.

    """
    result = basePath
    if result and not basePath.endswith(os.sep):
        result += os.sep
    result += relativePath
    result = os.path.normpath(result)

    return result


def relativizePath(path):
    path = os.path.normpath(path)
    if path.startswith(basePath):
        path = path[len(basePath)+1:]

    return path


setupBasePath(sys.argv[0])