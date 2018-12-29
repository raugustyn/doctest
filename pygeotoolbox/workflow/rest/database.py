#!c:/python27/python.exe
#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"

import psycopg2


class Connection:
    _connection = None
    _connectionString = "user=postgres password=postgres"
    _databaseNames = []

    @staticmethod
    def connection():
        if not Connection._connection:
            Connection.connection = psycopg2.connect(Connection.connectorString)

        return Connection.connection


    @staticmethod
    def setConnectionString(connectionString):
        if Connection <> Connection.Connection:
            Connection._connectionString = connectionString
            if Connection._connection:
                Connection._connection.close()
            Connection._connection = None


    @staticmethod
    def getDatabaseNames():
        """

        :return:

        >>> print Connection.getDatabaseNames()
        ['postgres', 'data10', 'tb04cuzk001_testbed', 'gensmd', 'lms', 'zabarak']

        """

        if not Connection._databaseNames:
            connection = psycopg2.connect(Connection._connectionString)
            cursor = connection.cursor()
            cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
            result = []
            for row in cursor:
                result.append(row[0])
            return  result

        return Connection._databaseNames


    @staticmethod
    def execute(sql, databaseName):
        databaseName = databaseName.lower()

        connection = psycopg2.connect(Connection._connectionString + " dbname='%s'" % databaseName)
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            connection.commit()
        finally:
            cursor.close()
            connection.close()


    @staticmethod
    def createDatabase(databaseName):
        databaseName = databaseName.lower()
        sql = "CREATE DATABASE data10 WITH OWNER = postgres ENCODING = 'UTF8' TABLESPACE = pg_default LC_COLLATE = 'Czech_Czech Republic.1250' LC_CTYPE = 'Czech_Czech Republic.1250' CONNECTION LIMIT = -1;"
        sql = sql.replace("data10", databaseName)

        connection = psycopg2.connect(Connection._connectionString + " dbname='postgres'")
        cursor = connection.cursor()
        try:
            from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor.execute(sql)
            connection.commit()
        finally:
            cursor.close()
            connection.close()

        sql = 'CREATE EXTENSION postgis SCHEMA public VERSION "2.2.2";'
        Connection.execute(sql, databaseName)


def processDatabaseRequest(databaseName, pathList, queryParams, response):
    from json import dumps

    if pathList:
        pathItem = pathList[0].lower()
        if pathItem == "schemas":
            html = dumps(["schemaa", "schemab"], indent=4)
            response.mimeFormat = "application/json"
        else:
            html = "Unknown request at database %s : %s" % (databaseName, pathItem)

    else:
        html = "No request at database " + databaseName

    response.handled = True
    response.htmlData = html
    return response


def processRequest(pathList, queryParams, response):
    from json import dumps
    from pygeotoolbox.sharedtools import normalizePath, fileRead

    if pathList:
        pathItem = pathList[0].lower()
        if pathItem == "names":
            html = dumps(Connection.getDatabaseNames(), indent=4)
            response.mimeFormat = "application/json"
        elif pathItem == "fields":
            html = fileRead(normalizePath("workflow/rest/FieldEditors/DatabaseName.html"))
        elif pathItem == "create":
            if len(pathList) == 2:
                Connection.createDatabase(pathList[1])
                html = "Database created"
            else:
                html = "Create database. Database name not provided."

        elif pathItem in Connection.getDatabaseNames():
            return processDatabaseRequest(pathItem, pathList[1:], queryParams, response)
        else:
            html = "Unknown request " + pathItem

    else:
        html = "No database request defined"

    response.handled = True
    response.htmlData = html
    return response

if __name__ == "__main__":
    from workflow.rest.workflows import registerPath, runServer

    registerPath("database", processRequest)
    runServer("workflow.rest.database") # , aDefaultPath = "database/names")