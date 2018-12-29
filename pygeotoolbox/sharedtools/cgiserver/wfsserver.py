#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"

from cgiserver import runServer, PathContainer

__SYMBOLNAMES = None
__SYMBOLS = None
__DUMP_SYMBOLS_PROC = None


def getWFSData(databaseName, tableName, bbox, srsName, schemaName="", sqlQuery=""):
    from shapely.wkb import loads
    import geojson

    import pygeotoolbox.sharedtools.log as logger
    from pygeotoolbox.database import databaseByName
    from pygeotoolbox.sharedtools import listToSqlStr

    logger.openSection("Building WFS Data...")
    FIELD_DEFS = 'graphic_symbol'
    GEOMETRY_FIELD_NAME = 'geom'

    """
    sampleRequest:
    http://localhost/cgi-bin/mapserv.exe?map=C:/ms4w/Apache/hidden/MapGen/osm_lund.map&service=wfs&version=1.1.0&request=GetFeature&typename=data_area&outputFormat=application/json&srsname=EPSG:3857&bbox=1471006.5443115234,7501014.372741699,1471356.5870361328,7502471.5505981445,EPSG:3857

    """
    if not schemaName:
        schemaName = "mg_work"

    if __SYMBOLNAMES:
        symbolNamesWhereClause = "graphic_symbol in %s and " % listToSqlStr(__SYMBOLNAMES)
    else:
        symbolNamesWhereClause = ""
    logger.info("Symbol names:" + str(listToSqlStr(__SYMBOLNAMES)))
    logger.info("bbox:" + str(bbox))
    sql = "select %s, (st_dump(%s)).geom from %s.%s, (select ST_MakeEnvelope(%s) as envelope) as bbox where %s %s && bbox.envelope" % (FIELD_DEFS, GEOMETRY_FIELD_NAME, schemaName, tableName, bbox, symbolNamesWhereClause, GEOMETRY_FIELD_NAME)
    if sqlQuery:
        sql += " and (%s)" % sqlQuery

    fieldNames = FIELD_DEFS.split(',')

    logger.info("Loading features...")
    features = []
    database = databaseByName(databaseName)
    for row in database.executeSelectSQL(sql):
        shape = loads(row[len(row) - 1], hex=True)
        properties = {}
        for fieldName, fieldIndex in zip(fieldNames, range(len(fieldNames))):
            properties[fieldName] = row[fieldIndex]

        if __DUMP_SYMBOLS_PROC:
            features.extend(__DUMP_SYMBOLS_PROC(shape, properties))
        else:
            features.append(geojson.Feature(geometry=shape, properties=properties))
    logger.info("%d features found" % len(features))
    logger.closeSection()
    return '{ "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::%s" } }, ' % srsName + geojson.dumps(geojson.FeatureCollection(features))[1:]


def getFeaturesProcessor(request, response):
    values = []
    for item in [( 'service', 'wfs'), ('request', 'GetFeature'), ('outputFormat', 'application/json'), ('typename', None), ('bbox', None), ('srsname', None), ('databasename', None)]:
        key, defaultValue = item
        value = request.query.get(key, defaultValue)
        if value:
            values.append(value)
        else:
            response.buildResult("Error: parameter %s is missing" % key, "text/html")
            return
    service, request, outputFormat, typeName, bbox, srsName, databaseName = values

    response.buildResult(getWFSData(databaseName, typeName, bbox, srsName), "application/json")


def processGetFeaturesRequest(request, response, defaultValues={}, sqlQuery="", schemaName=""):
    values = []
    for item in [( 'service', 'wfs'), ('request', 'GetFeature'), ('outputFormat', 'application/json'), ('typename', None), ('bbox', None), ('srsname', None), ('databasename', None)]:
        key, defaultValue = item
        value = request.query.get(key, defaultValue)
        if not value and key in defaultValues:
            value = defaultValues[key]

        if value:
            values.append(value)
        else:
            response.buildResult("Error: parameter %s is missing" % key, "text/html")
            return
    service, request, outputFormat, typeName, bbox, srsName, databaseName = values

    response.buildResult(getWFSData(databaseName, typeName, bbox, srsName, schemaName, sqlQuery), "application/json")


def getRestPaths(symbolNames=None, symbols=None, dumpSymbolsProc=None):
    global __SYMBOLNAMES, __SYMBOLS, __DUMP_SYMBOLS_PROC

    if symbols and not symbolNames:
        __SYMBOLNAMES = symbols.names()
    else:
        __SYMBOLNAMES = symbolNames
    __SYMBOLS = symbols
    __DUMP_SYMBOLS_PROC = dumpSymbolsProc

    return { "wfs/GetFeatures": PathContainer(getFeaturesProcessor, "Gets data_table features as WFS request") }


def runWFSServer(port, symbolNames=None, symbols=None, dumpSymbolsProc=None):
    runServer(port,  getRestPaths(symbolNames, symbols, dumpSymbolsProc))


if __name__ == "__main__":
    runWFSServer(15368)
