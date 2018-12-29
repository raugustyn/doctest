#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"
"""
This module loads Permanent Cartographic Representations in GeoJSON format into PostGIS working space in m3_persistent_representations schema:

representations:        Overview table with high level representation information.
context_features:       Table storing object model (source) data.
cartographic_features:  Table storing cartographic (target) data.
load_statistics:        Table with last database update information.

"""

import os
from json import load
from pygeotoolbox.sharedtools import normalizePath
from dataconnectors import connection as database
from operations import Operations
import sharedtools.log as log


dataFileName = normalizePath("m3/persistentrepresentations/PersistentCartographicRepresentations.json")


def loadFeatures(features, tableName, caption, id):
    for feature in features:
        wkt = feature["geom"]

        operationValue = ""
        if "visible" in feature and not feature["visible"]:
            operationValue = ", '%s'" % Operations.getCaption(Operations.HIDE)
        elif "modified" in feature and feature["modified"]:
            operationValue = ", '%s'" % Operations.getCaption(Operations.CHANGE_GEOMETRY)

        if operationValue:
            #print "#%s\t%s\t%s\t%s" % (str(id), feature["feature_id"], operationValue.replace(", ", ""), str(feature["visible"]))
            operationFieldDef = ", cartographic_operation"
        else:
            operationFieldDef = ""

        if wkt:
            geometry = "st_geometryfromtext('%s', 5514)" % wkt
        else:
            geometry = "null"

        database.execute(
            "insert into m3_persistent_representations.context_features (representation_id, geom, map_symbol, feature_id%s) values(1234, st_geometryfromtext('POINT(-564876.0 -1170159.0)', 5514), '1260000', 5678%s);" % (operationFieldDef, operationValue),
            {
                "context_features": tableName,
                "1234": id,
                "st_geometryfromtext('POINT(-564876.0 -1170159.0)', 5514)": geometry,
                '1260000': feature["znacka"],
                "5678": feature["feature_id"]
            }
        )

    if caption:
        envelope = database.firstRowFromSelect("select st_astext(st_buffer(st_envelope(ST_Collect (geom)), 0.1)) as geom from m3_persistent_representations.context_features where representation_id = 1234", { "1234": id})[0]
        if envelope:
            database.execute(
                "insert into m3_persistent_representations.representations (representation_id, geom, caption) values(1234, st_geometryfromtext('POINT(-564876.0 -1170159.0)', 5514), '1260000');",
                {
                    "1234": id,
                    "POINT(-564876.0 -1170159.0)": envelope,
                    '1260000': caption
                }
            )
        #else:
        #    print "No context found"


def loadDatabase(cleanBefore = False):
    """Loads Permanent cartographic representations items into m3_persistent_representations database schema.

    :param cleanBefore: If True, then database is dropped before load. If False, it appends records to existing content.
    """
    log.logger.openSection("Loading database of Permanent cartographic representations.")
    if cleanBefore or not database.schemaExists("m3_persistent_representations") or not database.tableExists("m3_persistent_representations", "cartographic_features"):
        from pygeotoolbox.sharedtools import fileRead
        sql = fileRead(os.path.splitext(__file__)[0] + ".sql")
        database.execute(sql)

    log.logger.info("Loading data file %s" % dataFileName)
    data = load(open(dataFileName, "r"))
    log.logger.info("%d records loaded." % len(data))
    for situation, id in zip(data, range(len(data))):
        loadFeatures(situation["SourceFeatures"], "context_features", situation["Caption"], id)
        loadFeatures(situation["TargetFeatures"], "cartographic_features", None, id)

    database.execute("insert into m3_persistent_representations.load_statistics (last_update_timestamp) values ('%s');" % str(os.path.getmtime(dataFileName)))
    log.logger.closeSection()


def databaseNeeded():
    """Checks whether Permanent cartographic representations database is up to date. If not, loadDatabase procedure is called.
    """
    if not database.schemaExists("m3_persistent_representations") or \
       not database.tableExists("m3_persistent_representations", "load_statistics") or \
       database.firstRowFromSelect("select * from m3_persistent_representations.load_statistics")[0] < str(os.path.getmtime(dataFileName)):
       loadDatabase(True)
    else:
        log.logger.info("Permanent cartographic representations database is up to date.")

# @NO-PRODUCTION CODE
if __name__ == "__main__":
    log.createLogger("dataconnectors.persistentcartographicsituations.loader")

    databaseNeeded()