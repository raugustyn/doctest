#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"

from dataconnectors import connection as database
import sharedtools.config as config
from pygeotoolbox.sharedtools import listToSqlStr


class Config:
    CAPTION_KEY = "Caption"
    SOURCE_FEATURES_KEY = "SourceFeatures"
    TARGET_FEATURES_KEY = "TargetFeatures"


class Representation:

    def __init__(self, caption, scale, context, solution):
        self.caption = caption
        self.scale = scale
        self.context = context
        self.solution = solution

def wktToGraphicType(wkt):
    wkt = wkt.upper()
    for code, values in { "P": ['POLYGON'], "L": ['LINESTRING'], "B": ['POINT']}.iteritems():
        for value in values:
            if wkt.startswith(value):
                return code

    raise NotImplementedError


def dumpItems(tableName, rows, items):
    result = 0
    for row in rows:
        item = {}
        for name, value in zip(["feature_id", "znacka", "geom"], row):
            item[name] = value

        if len(row) > 3:
            isVisible = row[3] == 1
            item["visible"] = isVisible
            item["modified"] = isVisible # and row[2] <> None

        item["znacka"] = wktToGraphicType(row[2]) + str(item["znacka"])
        items.append(item)
        result = result + 1

    return result


def dumpdict(representations, geomFieldNames, visibilityFieldNames):
    result = []
    for representation in representations:
        representationItem = {
            Config.CAPTION_KEY: representation.caption,
            Config.SOURCE_FEATURES_KEY: [],
            Config.TARGET_FEATURES_KEY: []
        }
        result.append(representationItem)
        items = representationItem[Config.SOURCE_FEATURES_KEY]
        for tableName, ids in representation.context.iteritems():
            sql = "select objectid, znacka, st_astext((st_dump(wkb_geometry)).geom) from public.z_plocharuzna_p where objectid in (93473)"
            params = {
                "(93473)": listToSqlStr(ids),
                "z_plocharuzna_p": tableName
            }
            rows = database.executeSelectSQL(sql, params)
            dumpItems(tableName, rows, items)

        items = representationItem[Config.TARGET_FEATURES_KEY]
        if representation.solution == {}:
            solutionItems = representation.context
        else:
            solutionItems = representation.solution

        for tableName, ids in solutionItems.iteritems():
            sql = """
select objectid, znacka, st_astext((st_dump(wkb_geometry)).geom), viditelnost10 from public.z_plocharuzna_p where objectid in (93473) and (viditelnost10=0 or (viditelnost10=1 and zm10_geom is null))
union all
select objectid, znacka, st_astext((st_dump(zm10_geom)).geom), viditelnost10 from public.z_plocharuzna_p where objectid in (93473) and viditelnost10 = 1 and zm10_geom is not null
            """
            #sql = "select objectid, znacka, st_astext((st_dump(wkb_geometry)).geom) from public.z_plocharuzna_p where objectid in (93473)"
            sqlParams = {
                "(93473)": listToSqlStr(ids),
                "z_plocharuzna_p": tableName,
                "zm10_geom": geomFieldNames[str(representation.scale)],
                "viditelnost10": visibilityFieldNames[str(representation.scale)]
            }
            rows = database.executeSelectSQL(sql, sqlParams)
            dumpedItemsCount = dumpItems(tableName, rows, items)
            if dumpedItemsCount <> len(ids):
                from pygeotoolbox.sharedtools import setParameters
                sql = setParameters(sql, sqlParams)
                print sql
                print __file__, "dumpdict() Error", dumpedItemsCount, "<>", len(ids), "representation", representation.caption

    return result


def dump(representations, geomFieldNames, visibilityFieldNames, fileName):
    import codecs
    from json import dump

    result = dumpdict(representations, geomFieldNames, visibilityFieldNames)
    dump(result, codecs.open(fileName, "w", "utf-8"), indent=4)