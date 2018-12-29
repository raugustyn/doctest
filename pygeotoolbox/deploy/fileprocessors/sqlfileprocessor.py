#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"

from base import ProcessFileProcessor


class SQL_FileProcessor(ProcessFileProcessor):
    def __init__(self, processor, fileName, outputFileName):
        ProcessFileProcessor.__init__(self, processor, fileName, outputFileName, '#', None, False)