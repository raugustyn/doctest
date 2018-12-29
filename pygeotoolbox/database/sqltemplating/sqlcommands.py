#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"

import os
from pygeotoolbox.sharedtools import changeFileExtension
import pygeotoolbox.sharedtools.log as log
from base import *
from sqlprocedure import SQLProcedure


class SQLCommands:
    """SQL commands/queries binder class.
    """

    def __init__(self, connection = None, sqlFileName = None, file = None):
        """ Relay from default connection, if provided. Loads a parses SQL script from sqlFileName or file.

        :param connection: database connection, provide in two detabases scenarios only
        :param sqlFileName: SQL file name to be loaded and parsed
        :param file: open file to load and parse script from
        """
        if not connection:
            from pygeotoolbox.database import database
            connection = database

        self.connection = connection
        self.procedures = {}
        self.procedureDecrators = {}
        self.__sqlBuffer = None
        self.setBufferSize(0)
        if file:
            if sqlFileName:
                sqlFileName = os.path.dirname(file) + os.sep + sqlFileName
            else:
                sqlFileName = changeFileExtension(file, '.sql')

        if sqlFileName:
            if os.path.exists(sqlFileName):
                self.load(sqlFileName)
            else:
                log.warning("File <%s> not found." % sqlFileName)


    def __del__(self):
        self.clearBuffer()


    def __str__(self):
        return "SQLCommands([%s])" % (", ".join(self.procedures.keys()))


    def __getDecorator(self, decoratorId):
        if decoratorId in self.procedureDecrators:
            return self.procedureDecrators[decoratorId]
        else:
            return None


    def setBufferSize(self, size):
        """Set SQL buffer to given size.

        :param int size: number of buffer items
        """
        def executeSQLNoBuffer(sql):
            self.connection.execute(sql)

        def executeSQLWithBuffer(sql):
            self.__sqlBuffer = self.connection.executeBuffer(sql, self.__sqlBuffer, self.__bufferSize)

        self.clearBuffer()
        if size > 1:
            self.__sqlBuffer = []
            self.executeSQL = executeSQLWithBuffer
        else:
            self.__sqlBuffer = None
            self.executeSQL = executeSQLNoBuffer

        self.__bufferSize = size


    def clearBuffer(self):
        """Executes all commands in SQL buffer. """
        self.__sqlBuffer = self.connection.clearBuffer(self.__sqlBuffer)


    def _getProcedureHeaders(self):
        """Returns definition header string.
        Since SQL connection is buffered, it is necessary to clear buffer after data creation scripts are executed, before querying data in affected tables.
        You can suppress buffering via setBufferSize(0), which will slow down the execution as a side effect.
        """
        items = []

        for procedure in self.procedures.values():
            items.append(procedure.getHeader())

        return "\n".join(items)


    def __registerDecorator(self, decorator):
        self.procedureDecrators[id(decorator)] = decorator
        setattr(self, decorator.name, decorator)


    def loads(self, sql, doAppend = True):
        """Parses SQL script from sql string and creates commands and queries binders.

        :param str sql: SQL sequence with commands and queries definition
        :param bool doAppend: if False, then deletes all existing binders
        """
        assert isinstance(sql, basestring), "sql parameter must be string"
        assert sql <> "", "sql parameter must not be empty string"

        if not doAppend:
            for proc in self.procedures:
                delattr(self, proc.name)
            self.procedures = {}

        for item in sql.split(SECTIONS_DELIMETER):
            item = item.strip()
            if item:
                proc = SQLProcedure(self, SECTIONS_DELIMETER + item)
                self.procedures[proc.name] = proc
                self.__registerDecorator(proc)


    def load(self, fileName, doAppend = True, encoding = "utf-8"):
        """ Loads and parses SQL script from sql string and creates commands and queries binders.

        :param str fileName: file name to be loaded
        :param bool doAppend: if False, then deletes all existing binders
        :param str encoding: file encoding, "utf-8" as a default value
    
        """
        assert isinstance(fileName, basestring)
        import codecs

        fileStream = codecs.open(fileName, "r", encoding)
        data = fileStream.read()
        fileStream.close()

        return self.loads(data, doAppend)


    def execute(self, commandName, **kwargs):
        """Executes command commanName with arguments specified

        :param str commandName: command name to be executed
        :param kwargs: command parameters to be aplied
        """
        if commandName in self.procedures:
            self.procedures[commandName].execute(kwargs)
            pass


    def executeSelectSQL(self, queryName, **kwargs):
        """Selects query queryName with arguments specified.

        :param str queryName: query name to be executed
        :param kwargs: command parameters to be aplied
        """
        if queryName in self.procedures:
            return self.procedures[queryName].executeSelectSQL(kwargs)
