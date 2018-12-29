#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"


import sharedtools.log as log
from __init__ import connection as database


def getTableCountQueryWhereClause(tableName):
    return "substring(source_id, 1, %d) = '%s'" % (len(tableName), tableName)


class TableLoader:
    class LoadTableContainer:
        def __init__(self, caption, tableName, query, countQuery, ctaDefinition = None):
            self.caption = caption
            self.tableName = tableName
            self.query = query
            self.countQuery = countQuery
            self.ctaDefinition = ctaDefinition


    def __init__(self, description):
        self.__items = []
        self.description = description
        self.__spatialClause = None


    def setViewArea(self, geomFieldName, minX, minY, maxX, maxY):
        self.__spatialClause = "(%s && ST_GeomFromText('LINESTRING(%f %f, %f %f)', 5514))" % (geomFieldName, minX, minY, maxX, maxY)


    def add(self, caption, tableName, query, countQuery, ctaDefinition = None):
        self.__items.append(TableLoader.LoadTableContainer(caption, tableName, query, countQuery, ctaDefinition))


    def loadData(self, caption, tableName, query, countQuery, ctaDefinition):
        if self.__spatialClause:
            if query:
                query = "(%s) and " % query
            query += self.__spatialClause
        database.insertIntoDataElements(tableName, query, ctaDefinition)
        numWaterTowers = database.getRowCount("data.elements", countQuery)
        log.logger.info("%d %s loaded." % (numWaterTowers, caption))


    def execute(self):
        log.logger.openSection("Loading %s..." % self.description)
        database.emptyTableNeeded("data", "elements", None, False)

        for item in self.__items:
            self.loadData(item.caption, item.tableName, item.query, item.countQuery, item.ctaDefinition)

        log.logger.closeSection()

# #############################################################################
# NO-PRODUCTION CODE
# #############################################################################
if __name__ == "__main__":
    from pygeotoolbox.sharedtools.log import createLoggerForModule
    createLoggerForModule(__file__)

    if True:
        loader = TableLoader()
        loader.add("z_vegetaceplocha_p", 'z_vegetaceplocha_p', '', "substring(source_id, 1, 18) = 'z_vegetaceplocha_p'")
        loader.add("z_voda_p", 'z_voda_p', '', "substring(source_id, 1, 8) = 'z_voda_p'")
        loader.execute()