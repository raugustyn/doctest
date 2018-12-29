#  -*- coding: utf-8 -*-
# @PRODUCTION MODULE
__author__ = "radek.augustyn@email.cz"


import pygeotoolbox.sharedtools.config as config
from pygeotoolbox.sharedtools import fileRead, setParameters


config.registerValue("database.name", "gensmd", "Database", "Database name on the SQl server.")
config.registerValue("database.user", "postgres", "User", "Database user name.")
config.registerValue("database.password", "postgres", "Password", "Database user password")
config.registerValue("database.host", "localhost", "Server", "Server IP adress")
config.registerValue("database.type", "postgis", "Database type", "Database type (postgis etc)")
config.registerValue("database.epsg", 5514, "Database EPSG Code", "Database EPSG Code")
config.registerValue("database.proj4Def", "+proj=krovak +lat_0=49.5 +lon_0=24.83333333333333 +alpha=30.28813972222222 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +towgs84=570.8,85.7,462.8,4.998,1.587,5.261,3.56 +units=m +no_defs", "proj4 EPSG", "")

class DatabaseTemplate:
    """Template for geodatabase class. Methods with NotImplementedError must be implemented by all descendants.

    """
    def __init__(self):
        self.__muted  = False
        self.__connection = None
        self.executeElapsedTime = 0
        self.selectElapsedTime = 0


    @property
    def muted(self):
        """Returns True if database is muted."""
        return self.__muted


    def mute(self):
        """Switch database into muted state, in which neither execute or executeSelectSQL commands are not commited.

        """
        self.__muted = True


    def unMute(self):
        """Switch database into unmuted state, in which both execute or executeSelectSQL commands works.

        """
        self.__muted = False


    def __del__(self):
        self.disconnect()


    def disconnect(self):
        """Disconnects database connection."""
        raise NotImplementedError("Database descendants must implement disconnect method.")


    def execute(self, sql, parameters={}):
        """Executes sql command. Before execution, it replaces parameters if provided.

        :param str sql: Command sequence to be executed;
        :param dict parameters: Parameters to be used in a query.

        """
        raise NotImplementedError("Database descendants must implement execute method.")


    def executeSelectSQL(self, sql, parameters={}):
        """Runs SQL query and returns database cursor with query result.

        :param str sql: Query to be executed.
        :param dict parameters: Parameters to be used in a query.
        :return cursor : Cursor with result or None if fails.
        """
        raise NotImplementedError("Database descendants must implement executeSelectSQL method.")


    def getTableNames(self, schema):
        """Return table names in a given database schema.

        :param str schema: schema name
        :return list of str: list of table names
        """
        raise NotImplementedError("Database descendants must implement getTableNames method.")


    def tableExists(self, schema, tableName):
        """Returns True if table exists in given schema.

        :param str schema: Schema name.
        :param str tableName: Table name.
        :return bool: True if table schema.tableName exists.
        """
        return tableName in self.getTableNames(schema)


    def createSchema(self, schema, dropIfExists = False):
        """Creates database schema with given name.

        :param str schema: schema name
        :param bool dropIfExists: drops schema before creating, if already exists.
        """
        raise NotImplementedError("Database descendants must implement createSchema method.")


    def executeSQLFile(self, fileName, parameters = {}):
        """Loads SQL script from the file, compiles parameters into it and executes it.

        :param str fileName: file name to be loaded as SQL script
        :param parameters: paramaters to be compiled
        """
        self.execute(fileRead(fileName), parameters)


    def loadAndExecute(self, fileName, params={}):
        """Loads SQL script from the file and executes it.

        :param str fileName: file name to be loaded as SQL script
        """
        self.execute(fileRead(fileName), params)


    def clearBuffer(self, buffer):
        """Executes all commands in a buffer, commits the database and returns empty buffer.

        :param list of string buffer: List of SQL commands.
        :return: empty buffer.
        """
        if buffer:
            sql = "\n".join(buffer)
            self.execute(sql)

        return []


    def flushBuffer(self, buffer):
        """clearBuffer method alias. Executes all commands in a buffer, commits the database and returns empty buffer.

        :param list of string buffer: List of SQL commands.
        :return: empty buffer.
        """
        return self.clearBuffer(buffer)


    def executeBuffer(self, sql, buffer, limit=1000, parameters=None):
        """Inserts sql into buffer, then executes it, if number of commands in it is higher than limit or does nothing. returns either empty or original buffer.

        :param str sql:sql command to be inserted to buffer
        :param list of str buffer: buffer of SQL commands
        :param int limit: maximum number of items in a buffer before being executed
        :return list of str: empty list or buffer
        """
        if not sql.endswith(";"):
            sql += ";"

        if parameters:
            sql = setParameters(sql, parameters)

        buffer.append(sql)
        if len(buffer) > limit:
            buffer = self.clearBuffer(buffer)
        return buffer


    def databaseExists(self, databaseName):
        """Returns True if a database with name databaseName exists.

        :param str databaseName:database name
        :return:
        """
        raise NotImplementedError("Database descendants must implement databaseExists method.")


    def cleanTableContent(self, tableName, schema = "temp", whereClause = ""):
        raise NotImplementedError("Database descendants must implement cleanTableContent method.")


    def createDatabase(self, databaseName):
        """

        :param databaseName:
        :return:
        """
        raise NotImplementedError("Database descendants must implement createDatabase method.")


    def createOrCleanTable(self, schema, tableName, createSQL):
        if self.tableExists(schema, tableName):
            self.cleanTableContent(tableName, schema)
        else:
            self.execute(createSQL)
