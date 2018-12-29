#  -*- coding: utf-8 -*-
# @PRODUCTION MODULE
__author__ = "radek.augustyn@email.cz"


import time
import psycopg2

import pygeotoolbox.sharedtools.log as log
import pygeotoolbox.sharedtools.config as config
from pygeotoolbox.sharedtools import setParameters, Container
from base import DatabaseTemplate


config.registerValue("database.onCreateDatabaseSQL", "create extension postgis;", "Database EPSG Code", "Database EPSG Code")


class Database(DatabaseTemplate):
    def disconnect(self):
        if hasattr(self, "__connection"):
            self.__connection.close()
            self.__connection = None


    @property
    def connectionParams(self):
        import pygeotoolbox.sharedtools.config as config

        items = []
        for key, value in {
            "dbname": config.database.name,
            "user": config.database.user,
            "password": config.database.password
        }.iteritems():
            if value:
                items.append("%s=%s" % (key, value))

        if config.database.host <> "localhost":
            items.append("host=%s" % config.database.host)

        return " ".join(items)


    @property
    def connection(self):
        if not hasattr(self, "__connection"):

            self.__connection = psycopg2.connect(self.connectionParams)

        return self.__connection


    @staticmethod
    def extractSchemaAndTableName(tableSpec):
        assert isinstance(tableSpec, basestring)

        delPos = tableSpec.find(".")
        if delPos >= 0:
            schema = tableSpec[:delPos]
            tableName = tableSpec[delPos+1:]
        else:
            schema = Database.getDefaultSchemaIfNotAssigned("")
            tableName = tableSpec

        return schema, tableName


    def getTableNames(self, schema):
        """Return table names in a given database schema.

        :param str schema: schema name
        :return list of str: list of table names
        """
        assert isinstance(schema, basestring)

        result = []
        cursor = self.executeSelectSQL("SELECT table_name FROM information_schema.tables WHERE table_schema='%s'" % schema)
        if cursor:
            rows = cursor.fetchall()
            for row in rows:
                result.append(row[0])

        return result


    def createSchema(self, schema, dropIfExists = False):
        """Creates database schema with given name.

        :param str schema: schema name
        :param bool dropIfExists: drops schema before creating, if already exists.
        """
        assert isinstance(schema, basestring)
        assert isinstance(dropIfExists, bool)

        sql = "create schema if not exists %s;" % schema
        if dropIfExists:
            sql = "drop schema if exists %s;" % schema
        self.execute(sql)


    def getRowCount(self, tableFullName, whereClause=None):
        """ Returns table row count.

        :param String tableFullName:
        :return LongInt: Row count for the table specified.


        >>> connection = Database()
        >>> connection.getRowCount("public.z_terennirelief_l")
        1099736L
        """
        sql = "select count(*) from %s" % tableFullName
        if whereClause:
            sql += " where " + whereClause

        return self.firstRowFromSelect(sql)[0]


    def execute(self, sql, parameters = {}):
        """Executes sql command. Before execution, it replaces parameters if provided.

        :param str sql: Command sequence to be executed;
        :param dict parameters: Parameters to be used in a query.

        """
        assert isinstance(sql, basestring)
        assert isinstance(parameters, dict)

        if self.muted or not sql:
            return

        sql = setParameters(sql, parameters)

        connection = self.connection
        cursor = connection.cursor()
        #cursor = self.connection.cursor()
        try:
            startTime = time.time()
            cursor.execute(sql)
            self.executeElapsedTime += time.time() - startTime
            connection.commit()
            #self.connection.commit()
        except psycopg2.Error as e:
            log.error(str(e) + "\n" + sql)
        finally:
            cursor.close()


    def firstRowFromSelect(self, sql, parameters = {}):
        cursor = self.executeSelectSQL(sql, parameters)
        if cursor:
            result = cursor.fetchone()
            cursor.close()
            return result
        else:
            return None


    def loadShapes(self, sql, fieldNames, geomFieldName):
        from shapely.wkb import loads
        from pygeotoolbox.sharedtools import Container

        result = []
        for row in self.executeSelectSQL(sql):
            item = Container()
            for value, fieldName in zip(row, fieldNames):
                if fieldName == geomFieldName:
                    value = loads(value, hex=True)
                setattr(item, fieldName, value)
            result.append(item)
        return result


    def executeSelectSQL(self, sql, parameters = {}, iterSize=0):
        """Runs SQL query and returns database cursor with query result.

        :param str sql: Query to be executed.
        :param dict parameters: Parameters to be used in a query.
        :return cursor : Cursor with result or None if fails.
        """

        assert isinstance(sql, basestring)
        assert isinstance(parameters, dict)
        assert isinstance(iterSize, int)

        sql = setParameters(sql, parameters)

        cursor = self.connection.cursor()
        if iterSize:
            cursor.itersize = iterSize
        startTime = time.time()
        cursor.execute(sql)
        self.selectElapsedTime += time.time() - startTime

        return cursor


    @staticmethod
    def getDefaultSchemaIfNotAssigned(schemaName):
        assert isinstance(schemaName, basestring) or schemaName == None

        if not schemaName:
            schemaName = 'public'

        return schemaName


    def cleanTableContent(self, tableName, schema = "temp", whereClause = ""):
        if tableName.find(".") == -1:
            tableName = schema + "." + tableName

        if whereClause:
            sql = "delete from %s where " % (tableName, whereClause)
        else:
            sql = "truncate table " + tableName
        self.execute(sql)


    def getFieldDefinition(self, schemaName, tableName):        
        assert isinstance(schemaName, basestring) or schemaName == None
        assert isinstance(tableName, basestring)


        schemaName = Database.getDefaultSchemaIfNotAssigned(schemaName)
        result = []
        cursor = self.connection.cursor()
        try:
            sql = "select * from information_schema.columns where table_schema = '%s' and table_name = '%s'" % (schemaName, tableName)
            cursor.execute(sql)
            result = cursor.fetchall()

        except Exception as inst:
            log.logger.error("PostGISConnector.getFieldDefinition('%s', '%s'):%s" % (schemaName, tableName, str(inst)))

        finally:
            cursor.close()
            
            return result


    def schemaExists(self, schemaName):
        return self.executeSelectSQL("SELECT exists(select schema_name FROM information_schema.schemata WHERE schema_name = '%s');" % schemaName).fetchone()[0]


    def findSRID(self, schemaName, tableName, fieldName):
        return self.firstRowFromSelect("SELECT Find_SRID('%s', '%s', '%s');" % (schemaName, tableName, fieldName))[0]


    @staticmethod
    def getFieldString(fieldDefinition):
        typeNames = {
            int: "int",
            basestring: "text"
        }

        return typeNames.get(fieldDefinition.type, "None")


    def fieldExists(self, fieldName, tableOrFieldDefinitions):
        assert isinstance(fieldName, basestring)
        assert isinstance(tableOrFieldDefinitions, list) or isinstance(tableOrFieldDefinitions, basestring)

        if isinstance(tableOrFieldDefinitions, basestring):
            schemaName, tableName = Database.extractSchemaAndTableName(tableOrFieldDefinitions)
            fieldDefinitions = self.getFieldDefinition(schemaName, tableName)
        else:
            fieldDefinitions = tableOrFieldDefinitions

        for fieldDefinition in fieldDefinitions:
            if fieldName == fieldDefinition[3]:
                return True

        return False


    def databaseExists(self, databaseName):
        """Returns True if a database with name databaseName exists.

        https://dba.stackexchange.com/questions/45143/check-if-postgresql-database-exists-case-insensitive-way
        :param str databaseName:database name
        :return:
        """
        connection = psycopg2.connect(user=config.database.user, host = config.database.host, password=config.database.password)
        cursor = connection.cursor()

        sql = "select exists(SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower('dbname'));".replace("dbname", databaseName)
        cursor.execute(sql)
        result = cursor.fetchone()[0]
        cursor.close()
        connection.close()

        return result


    def createDatabase(self, databaseName):
        """

        :param databaseName:
        """
        import sys
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

        log.openSection("Creating database '%s'" % config.database.name, level=log.DEBUG)

        sql = "create database %s;" % databaseName
        log.debug(sql)
        connection = psycopg2.connect(user=config.database.user, host = config.database.host, password=config.database.password)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.close()
        connection.close()

        if config.database.onCreateDatabaseSQL:
            log.debug(config.database.onCreateDatabaseSQL)
            self.execute(config.database.onCreateDatabaseSQL)

        log.closeSection()


    def geometryValueFromShape(self, shape):
        return self.geometryValueFromWKT(shape.wkt)


    def geometryValueFromWKT(self, wkt):
        return "st_geometryfromtext('%s', %s)" % (wkt, config.database.epsg)


    def normalizeName(self, name):
        result = ""
        for letter in name:
            if letter.isupper():
                result += "_" + letter.lower()
            else:
              result += letter

        return result


    def getFieldTypeFromValue(self, value):
        if isinstance(value, bool):
            return "boolean"
        elif isinstance(value, float):
            return "float"
        elif isinstance(value, int):
            return "integer"
        elif isinstance(value, basestring):
            return "varchar"

        raise "Field type not recognized"


# @NO-PRODUCTION CODE
if __name__ == "__main__":
    import database # No dummy, creating module variables

    db = Database()
    print "ids:", db.executeSelectSQL("select array_agg(elm_id) from data.elements").fetchone()[0]