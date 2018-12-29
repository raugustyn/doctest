from config import config

class PostGIS:
    def __init__(self, connectionString):
        import psycopg2
        self.connection = psycopg2.connect(connectionString)

    def tableExists(self, tableName, schema = "public"):
        sql = "select * from information_schema.tables where table_name='%s' and table_schema = '%s'" % (tableName, schema)
        cursor = self.executeSelectSQL(sql)

        return cursor.rowcount == 1

    def executeSelectSQL(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)

        return cursor

    def executeSQL(self, sql, commit = True):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        if commit:
            self.connection.commit()
        cursor = None

    def getColumnNames(self, tableName, schemaName = "public"):
        sql = "select column_name from information_schema.columns where table_name='%s' and table_schema = '%s'" % (tableName, schemaName);
        cursor = self.executeSelectSQL(sql)

        result = []
        for row in cursor.fetchall():
            result.append(row[0])

        return result


    def getGeometryFieldDefinition(self, schema, tableName, fieldName):
        sql = "select * FROM geometry_columns where f_table_name = '%s' and f_table_schema = '%s'" % (tableName, schema)
        cursor = self.executeSelectSQL(sql)

        row = cursor.fetchone()
        (srid, geometryType) = (row[5], row[6])

        return (geometryType, srid)

    def buildGeometryFieldDefinitionSQL(self, geometryType, srid):
        if srid == 0:
            sridStr = ""
        else:
            sridStr = ", " + str(srid)

        result = "geometry(%s%s)" % (geometryType, sridStr)

        return result

    def createField(self, schema, tableName, fieldName, fieldDefinition):
        sql = self.getCreateFieldSQL(schema, tableName, fieldName, fieldDefinition)
        self.executeSQL(sql)

    def getCreateFieldSQL(self, schema, tableName, fieldName, fieldDefinition):
        return "alter table %s.%s add column %s %s;" % (schema, tableName, fieldName, fieldDefinition)

    def commit(self):
        self.connection.commit()

pg = PostGIS(config.PG_CONNECTOR)
