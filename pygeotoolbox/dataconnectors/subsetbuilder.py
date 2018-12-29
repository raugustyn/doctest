#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"

import sharedtools.config as config
import sharedtools.log as log
from dataconnectors import connection

def buildSubSet(sourceSchema, targetSchema, minX, minY, maxX, maxY, tableNames=[], geometryFieldNames = ["wkb_geometry"]):
    log.logger.openSection("Building database subset %s->%s" % (sourceSchema, targetSchema))
    params = {
        "test_subset" : targetSchema,
        "public": sourceSchema,
        "wkb_geometry": geometryFieldNames[0]
    }
    if not tableNames:
        tableNames = connection.geometryTableNames(geometryFieldNames[0], sourceSchema)

    log.logger.openSection("Creating/cleaning target schema '%s'..." % targetSchema)
    if connection.schemaExists(targetSchema):
        connection.execute("drop schema test_subset", params)
    connection.createSchema(targetSchema)
    log.logger.closeSection()

    log.logger.info("Importing %d tables %s." % (len(tableNames), tableNames))
    mbrGeometrySQL = "st_geomfromtext('linestring(-749045 -1004614, -748967 -1004518)', 5514)"
    for key, value in {
        "-749045":  str(minX),
        "-1004614": str(minY),
        "-748967":  str(maxX),
        "-1004518": str(maxY)
    }.iteritems():
        mbrGeometrySQL = mbrGeometrySQL.replace(key, value)

    for tableName in tableNames:
        log.logger.info(tableName)
        sql = "create table test_subset.z_budova_b as select * from public.z_budova_b where wkb_geometry && MBRGEOMETRYSQL;\n"
        sql = sql.replace("MBRGEOMETRYSQL", mbrGeometrySQL)

        for geometryFieldName in geometryFieldNames:
            sql += "CREATE INDEX z_budova_b_wkb_geometry_geom_idx ON public.z_budova_b USING gist (wkb_geometry);\n".replace("wkb_geometry", geometryFieldName)

        params["z_budova_b"] = tableName
        connection.execute(sql, params)



    log.logger.closeSection()

###############################################################################
# NO-PRODUCTION CODE
###############################################################################
if __name__ == "__main__":
    from pygeotoolbox.sharedtools.log import createLogger
    createLogger("dataconnectors.subsetbuilder")
    buildSubSet("public", "test_subset", -762479,-981037, -753609,-975911)
