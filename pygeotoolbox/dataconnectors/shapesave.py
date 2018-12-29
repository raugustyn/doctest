#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"

from dataconnectors import connection
from pygeotoolbox.sharedtools import listToSqlStr

class ShapeSaver:
    def __init__(self, geometryFieldDefinition = { "geom" : "Geometry(Geometry, 5514)"} ):
        self.geometryFieldDefinition = geometryFieldDefinition
        self.__validatedTables = []
        self._schema = None
        self._tableName = None
        self._shape = None
        self._attributes = None


    def _createTable(self):
        geometryDefinitions = self.geometryFieldDefinition.copy()
        for fieldName in self._attributes:
            geometryDefinitions[fieldName] = "int"

        fieldSQLValues = []
        for key, value in geometryDefinitions.iteritems():
            fieldSQLValues.append("\t%s %s" % (key, value))


        sql = "create table %s.%s\n%s" % (self._schema, self._tableName, ",\n".join(fieldSQLValues))
        print sql
        #connection.execute(sql)

    def _tableNeeded(self,):
        identifier = "%s.%s" % (self._schema, self._tableName)

        if not identifier in self.__validatedTables:
            if not connection.tableExists(self._schema, self._tableName):
                self._createTable()

            self.__validatedTables.append(identifier)

    def saveShape(self, shape, schema, tableName, attributes = {}):
        self._schema = schema
        self._tableName = tableName
        self._shape = shape
        if attributes:
            self._attributes = attributes
        else:
            self._attributes = shape.__dict__.keys()

        self._tableNeeded()

        fieldDefs = listToSqlStr(self._attributes)
        print fieldDefs

saver = ShapeSaver()

def saveShape(shape, schema, tableName, attributes={}):
    saver.saveShape(shape, schema, tableName, attributes=attributes)

obj = lambda: None    # Dummy function
obj.foo = 'far'
obj.bar = 'boo'
saveShape(obj, "temp", "mojetabulka")