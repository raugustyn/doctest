# @PRODUCTION MODULE
__author__ = "radek.augustyn@email.cz"
__description__ = "Modul pro import souborů s daty ve formátu WKT (Well Known Text) do databáze PostGIS."
__moduleName__ = "WKTImporter"
__version__ = 0.1

if __name__ == "__main__":
    from pygeotoolbox.sharedtools.log import createLogger;
    createLogger("wktimport")

from pygeotoolbox.sharedtools.log import logger

import os, time
from pygeotoolbox.sharedtools.base import pathLeaf
import postgis
from config import config
import sqlprocessors
from pygeotoolbox.sharedtools import printEvery100rowsInLongLine

def fixPolygonWKT(wkt):
    wkt = wkt.strip()
    POLYGON_ID = "POLYGON"
    if wkt.upper().startswith(POLYGON_ID):
        body = wkt[len(POLYGON_ID):].strip()
        if not body.startswith("(("):
            wkt = POLYGON_ID + "(" + body + ")"


        componentParts = []
        hasChanged = False
        for part in wkt[len(POLYGON_ID)+2:].strip().replace("))", ")").split("),"):
            coordinatePairs = part.replace(")", "").replace("(", "").split(",")
            firsCoordinatePair = coordinatePairs[0].strip()
            lastCoordinatePair = coordinatePairs[len(coordinatePairs)-1].strip()

            if firsCoordinatePair <> lastCoordinatePair:
                coordinatePairs.append(firsCoordinatePair)
                hasChanged = True
                part =  ", ".join(coordinatePairs)
            componentParts.append("(" + part + ")")

        if hasChanged:
            wkt = POLYGON_ID + "(" + ", ".join(componentParts) + ")"
            wkt = wkt.replace(", ( (", ", (")
            wkt = wkt.replace(")))", "))")
            wkt = wkt.replace("POLYGON(((", "POLYGON((")

    return wkt


def processWKTFile(fileName, schema, idFieldName, sqlProcessor, geomFieldName = ""):
    startTime = time.time()
    srid = "0"

    def processWKT(wkt):
        wkt = wkt.replace("\n", "")
        wkt = fixPolygonWKT(wkt)

        return wkt

    def getGeometrySQLDefinition(wkt):
        wkt = processWKT(wkt)
        if wkt:
            result = "ST_GeomFromText('%s', %s)" % (wkt, srid)
            if isMultiGeometry and not wkt.upper().startswith("MULTI"):
                result = "ST_Multi(%s)" % result
        else:
            result = ""

        return result

    pg = postgis.pg

    tableName = os.path.splitext(pathLeaf(fileName))[0].lower()

    if pg.tableExists(tableName, schema):
        fieldNames = pg.getColumnNames(tableName, schema)

        (geometryType, srid) = pg.getGeometryFieldDefinition(schema, tableName, config.MASTER_GEOMETRY_FIELDNAME)
        templateFieldDefinition = pg.buildGeometryFieldDefinitionSQL(geometryType, srid)

        isHeaderRow = True
        inFile = open(fileName, "r")
        sqlProcessor.assignFileName(os.path.splitext(fileName)[0], tableName)

        if geomFieldName:
            geomFieldsList = [geomFieldName]
        else:
            geomFieldsList = ["zm25_geom", "zm10_geom"]

        fieldsToBeClearedSQLItems = []
        for geomFieldName in geomFieldsList:
            if geomFieldName not in fieldNames:
                sql = pg.getCreateFieldSQL(schema, tableName, geomFieldName, templateFieldDefinition)
                sqlProcessor.executeSQL(sql + "\n")
            else:
                fieldsToBeClearedSQLItems.append(geomFieldName + "=null")

        if fieldsToBeClearedSQLItems:
            sqlProcessor.executeSQL("update %s.%s set %s;\n" % (schema, tableName, ",".join(fieldsToBeClearedSQLItems)))

        id = None
        sql = None
        zm25count = 0
        zm10count = 0
        try:
            rowCount = 0
            isMultiGeometry = geometryType.upper().startswith("MULTI")
            for line in inFile:
                if isHeaderRow:
                    isHeaderRow = False
                else:
                    lineItems = line.split(";")
                    while len(lineItems) < 3:
                        lineItems.append("")

                    id, wktZM10, wktZM25 = lineItems
                    if wktZM25:zm25count = zm25count + 1
                    if wktZM10:zm10count = zm10count + 1

                    setItems = []
                    for (fieldName, wkt) in [("zm10_geom", getGeometrySQLDefinition(wktZM10)), ("zm25_geom", getGeometrySQLDefinition(wktZM25))]:
                        if wkt:
                            setItems.append("%s=%s" % (fieldName, wkt))

                    setSQL = ", ".join(setItems)
                    if setSQL == "":
                        raise "No updated fields"

                    sql = "update %s.%s set %s where %s = '%s';\n" % (schema, tableName, setSQL, idFieldName, id)
                    sqlProcessor.executeSQL(sql)
                rowCount = rowCount + 1
                printEvery100rowsInLongLine(rowCount)

            if zm10count == 0:
                sqlProcessor.executeSQL("alter table %s.%s drop column zm10_geom;\n" % (schema, tableName))
            if zm25count == 0:
                sqlProcessor.executeSQL("alter table %s.%s drop column zm25_geom;\n" % (schema, tableName))

        except Exception as inst:
            print "Error: %s:\tid=%s.\t%s\t%s" % (tableName, str(id), str(inst), sql)

        finally:
            inFile.close()
            sqlProcessor.commit()
            print tableName, "-", rowCount, "rows"
    else:
        print "Error, table", tableName, "does not exist."

    logger.info("%s -\t%d rows in\t%f seconds." % (tableName, rowCount, (time.time() - startTime)))

def processDirectory(path, processor):
    logger.openSection("Processing directory %s" % path)
    for fileName in os.listdir(path):
        (nameBase, extension) = os.path.splitext(fileName)
        geomFieldNames = {
            "_ZM10" : "zm25_geom",
            "_ZM25" : "zm10_geom"
        }
        geomFieldName = ""
        for key in geomFieldNames:
            if nameBase.lower().endswith(key):
                geomFieldName = geomFieldNames[key]

        if extension.lower() == ".wkt":
            processWKTFile(path + fileName, "public", config.ID_FIELD_NAME, processor, geomFieldName)

    logger.closeSection()

if __name__ == "__main__":
    #processor = sqlprocessors.sqlProcessor_RunInPostGis()
    #processor = sqlProcessor_SaveToMergedFile()
    processor = sqlprocessors.SQLProcessor_SaveToIndividualFiles(insertProfileEchos = True)
    logger.openSection("Importing WKT files")
    processDirectory("C:/Users/Radek Augustyn/Desktop/DataToImport/DATA10_20160803_WKT/", processor)
    logger.closeSection()