import psycopg2, time
from shapely.wkt import loads
from shapely.wkb import loads as wkbLoads

from pygeotoolbox.sharedtools import setParameters, listToSqlStr, printEvery100rows
import sqlkeywords
import sharedtools.log as log
import sharedtools.config as config

def getGeometrySQl(wkt):
    return "st_geometryfromtext('%s', %s)" % (wkt, config.getEPSGCode())

PUBLIC_SCHEMA_NAME = "public"

DEBUG_TABLE_DEFINITIONS = {
    "verticalLines" : ("m3_cartographicmodel", "vertical_lines", """

DROP TABLE if exists m3_cartographicmodel.vertical_lines;

CREATE TABLE m3_cartographicmodel.vertical_lines
(
  id serial NOT NULL,
  geom geometry(LineString,5514),

  element_id integer,
  master_width float,
  slave_width float,
  color_treshold float,

  caption character varying,
  first_id integer,
  first_length float,
  is_on_left_from_first boolean,
  is_vertex boolean,

  second_element_id integer,
  second_length float,
  is_on_left_from_second boolean,
  is_partofintersection boolean DEFAULT false,

  tag integer,
  tag_double double precision,
  stringtag character varying,

  CONSTRAINT vertical_lines_pkey PRIMARY KEY (id)
)
WITH (OIDS=FALSE);
ALTER TABLE m3_cartographicmodel.vertical_lines OWNER TO postgres;"""),
    "intersections" : ("m3_cartographicmodel", "intersections", """
DROP TABLE if exists m3_cartographicmodel.intersections;

CREATE TABLE m3_cartographicmodel.intersections
(
  id serial NOT NULL,
  geom geometry(Point, 5514),

  master_element_id integer,
  slave_element_id integer,
  first_length float,

  CONSTRAINT intersections_lines_pkey PRIMARY KEY (id)
)
WITH (OIDS=FALSE);
ALTER TABLE m3_cartographicmodel.intersections OWNER TO postgres;
    """)
}

def printError(row, errException):
    log.logger.error("Error: %s:%s" % (str(row), str(errException)))

class FieldDefinition:
    def __init__(self, name, definition, defValueString):
        self.name = name
        self.definition = definition
        self.defValueString = defValueString

class ExecuteBuffer:
    def __init__(self, limit = 100):
        self.buffer = []
        self.limit = limit

def buildConnectionParams(database, user, password, host):
    """Builds connection parameters string for psycopg2.connect. Only not empty parameters are used.
    See http://initd.org/psycopg/docs/usage.html fro mnore details.

    :param String database:Database name parameter.
    :param String user:Database user parameter.
    :param String password:Database password parameter.
    :param String host:Host IP address parameter.
    :return String:Connection string.

    >>> buildConnectionParams("mydatabase", "myuser", "mypassword", "localhost")
    'dbname=mydatabase user=myuser password=mypassword'

    """
    items = []

    def addItem(key, value):
        if value:
            items.append("%s=%s" % (key, value))

    addItem("dbname", database)
    addItem("user", user)
    addItem("password", password)
    if host <> "localhost":
        addItem("host", host)

    return " ".join(items)


class PostGISConnector:
    def __init__(self, connectionParams = None):
        # type: (object) -> object
        self.__connectionParams = connectionParams
        self.lastLoadedRowFirstItem = None
        self.__mute  = False
        self.__connection = None
        self.executeElapsedTime = 0
        self.selectElapsedTime = 0

    def disconnect(self):
        if self.__connection:
            self.__connection.close()
            self.__connection = None

    @property
    def connectionParams(self):
        if not self.__connectionParams:
            self.__connectionParams = buildConnectionParams(config.database.name, config.database.user, config.database.password, config.database.host)

        return self.__connectionParams

    @connectionParams.setter
    def connectionParams(self, value):
        self.disconnect()
        self.__connectionParams = value

    def schemaExists(self, schemaName):
        rows = self.executeSelectSQL("SELECT schema_name FROM information_schema.schemata WHERE schema_name = '%s';" % schemaName).fetchone()
        return rows <> None

    def mute(self):
        self.__mute = True

    def unMute(self):
        self.__mute = False

    def __del__(self):
        self.disconnect()

    def createSchema(self, schema):
        if not self.schemaExists(schema):
            sql = "create schema if not exists %s;" % schema
            self.execute(sql)


    def cleanTableContent(self, tableName, schema = "temp", whereClause = ""):
        if tableName.find(".") == -1:
            tableName = schema + "." + tableName

        if whereClause:
            sql = "delete from %s where " % (tableName, whereClause)
        else:
            sql = "truncate table " + tableName
        self.execute(sql)

    @property
    def connection(self):
        if not self.__connection:
            try:
                self.__connection = psycopg2.connect(self.connectionParams)
            except Exception as inst:
                log.logger.error("PostGISConnector.connection():'%s'." %  inst)

        return self.__connection

    def getTableNames(self, schema = PUBLIC_SCHEMA_NAME):
        result = []
        cursor = self.executeSelectSQL("SELECT table_name FROM information_schema.tables WHERE table_schema='%s'" % schema)
        if cursor:
            rows = cursor.fetchall()
            for row in rows:
                result.append(row[0])

        return result

    def emptyTableNeeded(self, schemaName, tableName, createSQLsequence, forceCreateTable, values = {}):
        self.createSchema(schemaName)
        if not self.tableExists(schemaName, tableName) or forceCreateTable:
            self.execute(createSQLsequence, values)
        else:
            self.cleanTableContent(tableName, schemaName)

    def cleanOrCreateTable(self, schemaName, tableName, createSQLsequence, values = {}):
        self.emptyTableNeeded(schemaName, tableName, createSQLsequence, False, values)


    def tableExists(self, schema, tableName):
        return tableName in self.getTableNames(schema)

    def dropTable(self, schema, tableName):
        self.execute("drop table %s.%s" % (schema, tableName))

    def debugTableRequested(self, name):
        (schema, tableName, sql) = DEBUG_TABLE_DEFINITIONS[name]
        if not self.tableExists(tableName, schema):
            self.execute(sql)

    def clearDebugTable(self, name):
        (schema, tableName, sql) = DEBUG_TABLE_DEFINITIONS[name]
        self.cleanTableContent(tableName, schema)

    def saveToDB(self, tableName, features, fieldsToStore={"tag": None, "tag2" : None, "tag3": None, "tag_double": 0.0}, indexFieldName="tag", geometryFieldName = "geom", executeBuffer = None):
        if features:
            fieldNames = ", ".join(fieldsToStore.keys())
            sql = ""
            for (feature, index) in zip(features, range(len(features))):
                fieldValues = []
                for (fieldName, fieldValue) in fieldsToStore.iteritems():
                    import types
                    value = getattr(feature, fieldName, None)
                    if not value:
                        if isinstance(fieldValue, types.FunctionType):
                            value = fieldValue(feature)
                        elif isinstance(fieldValue, basestring):
                            if fieldValue.startswith("$"):
                                value = getattr(feature, fieldValue[1:], None)
                                if value <> None:
                                    value = "'%s'" % str(value)
                                else:
                                    value = getattr(feature, fieldValue, None)
                    if not value:
                        value = fieldValue

                    if value <> None:
                        fieldValue = str(value)
                    else:
                        if fieldName == indexFieldName:
                            fieldValue = str(index)
                        else:
                            fieldValue = "null"
                    fieldValues.append(fieldValue)

                fieldValuesStr = ",".join(fieldValues)
                sql += "insert into %s (%s, %s) values (%s, ST_GeomFromText('%s', 5514));\n" % (tableName, fieldNames, geometryFieldName, fieldValuesStr, str(feature))

            if executeBuffer:
                executeBuffer.buffer = self.executeBuffer(sql, executeBuffer.buffer, executeBuffer.limit)
            else:
                self.execute(sql)

    def loadSourceFeatures(self, tableName, whereClause, geometryFieldName = "wkb_geometry", fields = [], graphicFieldName=None):
        from model.feature import BaseGeometry

        if tableName.find(".") < 0:
            tableName = "public." + tableName

        BaseGeometry.FEATURE_CLASS = tableName[tableName.find(".")+1:]
        sql = "select st_astext((st_dump(%s)).geom)" % geometryFieldName

        if graphicFieldName:
            sql += ", st_astext(%s)" % graphicFieldName
            graphicFieldIndex = 1
        else:
            graphicFieldIndex = None

        if fields:
            sql += ", " + ",".join(fields)
        sql += " from %s" % tableName
        if whereClause:
            sql += " where %s" % whereClause
        return self.loadFeatures(sql, 0, graphicFieldIndex=graphicFieldIndex)

    def loadFeatureByIdList(self, tableName, idList, geometryFieldName = "wkb_geometry", schema = "public", fieldList = ['ogc_fid']):
        fieldList.append(geometryFieldName)
        sql = "select %s from %s.%s where ogc_fid in %s " % (", ".join(fieldList), schema, tableName, listToSqlStr(idList))
        return self.loadFeatures(sql, len(fieldList) - 1)

    def loadFeatures(self, sql, geometryIndex, progressHandler = printEvery100rows, exceptionHandler = printError, featureClassIndex = None, symbolNameIndex = None, graphicFieldIndex=None):
        from model.feature import BaseGeometry
        from model.feature import shapelyToFeature

        result = []
        try:
            cursor = self.executeSelectSQL(sql)
            row = None
            for row in cursor:
                geometry = loads(row[geometryIndex])

                attrs = []
                for (i, attr) in zip(range(len(row)), row):
                    if i <> geometryIndex:
                        attrs.append(attr)

                if featureClassIndex <> None:
                    BaseGeometry.FEATURE_CLASS = row[featureClassIndex]
                feature = shapelyToFeature(geometry, attrs)
                if symbolNameIndex <> None:
                    feature.symbolName = row[symbolNameIndex]

                if graphicFieldIndex <> None:
                    if row[graphicFieldIndex]:
                        feature.graphicShape = loads(row[graphicFieldIndex])
                    else:
                        feature.graphicShape = None

                result.append(feature)
                if progressHandler:
                    progressHandler(len(result))

        except Exception as inst:
            if exceptionHandler:
                exceptionHandler(row, inst)

        return result

    def getDataSetCursor(self, sql):
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql)
            return cursor

        except Exception as inst:
            log.logger.error("PostGISConnector.getDataSetCursor():%s, %s" % (str(inst), sql))
            cursor.close()
            return None

    def getNextDataRow(self, dataSetCursor, geometryIndex):
        from model.feature import shapelyToFeature

        row = dataSetCursor.fetchone()
        if row:
            self.lastLoadedRowFirstItem = row[0]
            geometry = loads(row[geometryIndex])
            feature = shapelyToFeature(geometry, row)
            return feature
        else:
            return None

    def geometryTableNames(self, geometryFieldName = "wkb_geometry", schema = PUBLIC_SCHEMA_NAME):
        result = []
        for tableName in self.getTableNames(schema):
            fieldNames = self.getFieldNames(tableName, schema)
            if geometryFieldName in fieldNames:
                result.append(tableName)

        return result

    def getFieldNames(self, tableName, schema = PUBLIC_SCHEMA_NAME):
        sql = "select column_name, table_schema from information_schema.columns where table_name='%s' and table_schema = '%s';" % (tableName, schema)
        cursor = self.executeSelectSQL(sql)
        fieldNames = []
        for row in cursor.fetchall():
            fieldNames.append(row[0])
        return fieldNames

    def getFieldDefinition(self, schemaName, tableName):
        schemaName = self.getSchemaIfNotAssigned(schemaName)
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

    def insertIntoDataElements(self, tableName, whereClause, ctaDefinition = None):
        delPos = tableName.rfind("_")
        symbolType = tableName[delPos+1:delPos+2].upper()
        if whereClause:
            whereClause = " where " + whereClause

        if ctaDefinition:
            ctaPrefix, ctaTables = ctaDefinition
            ctaTables = ", " + ctaTables + " "
        else:
            ctaPrefix = ""
            ctaTables = ""

        sql = setParameters("""with cta as ()
insert into data.elements (source_id, source_elt_id, target_elt_id, source_geom, target_geom)
	select 'z_plocharuzna_b::' || objectid::text as source_id,
          'B' || znacka::text as source_elt_id,
		 'B' || znacka::text as target_elt_id,
		 wkb_geometry as source_geom,
		 null as target_geom
		 from public.z_plocharuzna_b, cta_tables where znacka = 4202700
        """,
                            {
                                ", cta_tables": ctaTables,
                                "with cta as ()": ctaPrefix,
                                "z_plocharuzna_b": tableName,
                                "'B'": "'%s'" % symbolType,
                                "where znacka = 4202700": whereClause
                            }
                            )
        self.execute(sql)


    def executeSQLFile(self, fileName):
        from pygeotoolbox.sharedtools import fileRead

        sql = fileRead(fileName)
        self.execute(sql)

    def execute(self, sql, values = {}):
        if self.__mute:
            return

        sql = setParameters(sql, sqlkeywords.sqlKeywordsValues)
        sql = setParameters(sql, values)

        cursor = self.connection.cursor()
        try:
            startTime = time.time()
            cursor.execute(sql)
            self.executeElapsedTime += time.time() - startTime
            self.connection.commit()

        except Exception as inst:
            log.logger.error("PostGISConnector.execute():" + str(inst) + " at " + sql)

        finally:
            cursor.close()

    def flushBuffer(self, buffer):
        self.clearBuffer(buffer)

    def clearBuffer(self, buffer):
        if buffer:
            sql = "\n".join(buffer)
            self.execute(sql)

        return []

    def executeBuffer(self, sql, buffer, limit=1000):
        if not sql.endswith(";"):
            sql += ";"

        buffer.append(sql)
        if len(buffer) > limit:
            buffer = self.clearBuffer(buffer)
        return buffer

    def getRowCount(self, tableFullName, whereClause=None):
        """ Returns table row count.

        :param String tableFullName:
        :return LongInt: Row count for the table specified.

        >>> connection = PostGISConnector("dbname=data10 user=postgres password=postgres")
        >>> connection.getRowCount("public.z_terennirelief_l")
        1099736L
        """
        if whereClause:
            whereClause = " where " + whereClause
        else:
            whereClause = ""
        rowCount = self.firstRowFromSelect("select count(*) from %s%s" % (tableFullName, whereClause))[0]

        return rowCount

    def firstRowFromSelect(self, sql, parameters = {}):
        cursor = self.executeSelectSQL(sql, parameters)
        if cursor:
            result = cursor.fetchone()
            cursor.close()
            return result
        else:
            return None

    def executeSelectSQL(self, sql, parameters = {}):
        sql = setParameters(sql, sqlkeywords.sqlKeywordsValues)
        sql = setParameters(sql, parameters)

        if True: # @TODO Hook fro error 'current transaction is aborted, commands ignored until end of transaction block'
            cursor = self.connection.cursor()
        else:
            c = psycopg2.connect(self.connectionParams)
            cursor = c.cursor()
        try:
            startTime = time.time()
            cursor.execute(sql)
            self.selectElapsedTime += time.time() - startTime
            return cursor

        except Exception as inst:
            log.logger.error("PostGISConnector.executeSelectSQL:'%s' '%s'" % (sql, str(inst)))
            return None

    def getSchemaIfNotAssigned(self, schemaName):
        if schemaName == '':
            schemaName = 'public'

        return schemaName

    def addFieldsIfNotExists(self, schemaName, tableName, fieldDict, fieldDefinitions = []):
        """

        :param String schemaName: Table schema.
        :param String tableName: Table name.
        :param fieldDict:
        :param list [FieldDefinition] fieldDefinitions: Field tefinitions of he table. If empty, then it would be retrieved from the database.
        :return (list fieldDefinitions, l;ist addedFields): New field definitions, list of added fields.

        """
        schemaName = self.getSchemaIfNotAssigned(schemaName)

        if not fieldDefinitions:
            fieldDefinitions = self.getFieldDefinition(schemaName, tableName)

        addedFields = []
        alterSQL = ""
        for requestedFieldDef in fieldDict:
            requestedFieldName = requestedFieldDef.name
            fieldExists = False
            for fieldDefinition in fieldDefinitions:
                fieldName = fieldDefinition[3]
                if fieldName == requestedFieldName:
                    fieldExists = True
                    break

            if not fieldExists:
                addedFields.append(requestedFieldName)
                alterSQL += 'alter table %s.%s add column %s %s;' % (schemaName, tableName, requestedFieldName, requestedFieldDef.definition)

        if alterSQL != "":
            self.execute(alterSQL)
            fieldDefinitions = self.getFieldDefinition(schemaName, tableName)

        return (fieldDefinitions, addedFields)

    def commit(self):
        """ Commits active connection.

        >>> connector = PostGISConnector("dbname=data10 user=postgres password=postgres")
        >>> connector.commit()
        """
        if self.connection:
            self.connection.commit()

    def getTableBBOX(self, schema, tableName, whereItems = []):
        """ Retrieves table box as tupple of (minX, minY, maxX, maxY).

        :param String schema: Schema with table to retrieve.
        :param String tableName: Table name to retrieve.
        :param List of String whereItems: List of where clause items, default is empty list.

        :return (minX, minY, maxX, maxY): Table bounding box.

        >>> connection = PostGISConnector("dbname=data10 user=postgres password=postgres")
        >>> print connection.getTableBBOX("public", "z_terennirelief_l", ["znacka=6060100"])
        (-904572.514770508, -1227214.76251221, -432383.396484375, -935351.153991699)
        """
        if whereItems:
            whereClause = " where " + " and ".join(whereItems)
        else:
            whereClause = ""

        cursor = self.executeSelectSQL(
            """with extent_table as (
	SELECT ST_Extent(wkb_geometry)as extent_field FROM public.z_terennirelief_l where znacka=6060100
)

select st_Xmin(extent_field), st_Ymin(extent_field), st_Xmax(extent_field), st_Ymax(extent_field) from extent_table""",
            {"public": schema, "z_terennirelief_l" : tableName, " where znacka=6060100": whereClause }
        )
        if cursor:
            result = cursor.fetchone()
            cursor.close()
            return result
        else:
            return None

def getDatabaseNames(connectorString = "user=postgres password=postgres"):
    conn = PostGISConnector(connectorString)
    cursor = conn.executeSelectSQL("SELECT datname FROM pg_database WHERE datistemplate = false;")
    result = []
    for row in cursor:
        result.append(row[0])
    return  result