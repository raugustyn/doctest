#  -*- coding: utf-8 -*-
###########################################################
#                                                         #
# Copyright (c) 2018 Radek Augustýn, licensed under MIT.  #
#                                                         #
###########################################################
__author__ = "radek.augustyn@email.cz"


import types
from database import database
import log


class DebugProfile:
    def __init__(self, tableName='rendering_debug', propertiesMapping={}):
        self.tableName = tableName
        self.propertiesMapping = propertiesMapping
        self.geometryFieldName = "geom"


    def clearTable(self):
        database.cleanTableContent(self.tableName, "m3_cartographicmodel")


    def save(self, elements, propertiesValues = {}):
        if elements:
            if isinstance(elements, list):
                for element in elements:
                    self.save(element, propertiesValues)
            else:
                if propertiesValues:
                    fieldsToBeStored = self.propertiesMapping.copy()
                    fieldsToBeStored.update(propertiesValues)
                else:
                    fieldsToBeStored = self.propertiesMapping

                feature = elements

                fieldValues = []
                for (fieldName, fieldValue) in fieldsToBeStored.iteritems():
                    value = getattr(feature, fieldName, None)
                    if not value:
                        if isinstance(fieldValue, types.FunctionType):
                            value = fieldValue(feature)
                        elif isinstance(fieldValue, basestring):
                            if fieldValue.startswith("$"):
                                value = getattr(feature, fieldValue[1:], None)
                                if value == None:
                                    value = getattr(feature, fieldValue, None)
                    if value == None:
                        value = fieldValue

                    if value <> None:
                        if isinstance(value, basestring):
                            fieldValue = "'%s'" % value
                        else:
                            fieldValue = str(value)
                    else:
                        fieldValue = "null"

                    fieldValues.append(fieldValue)

                fieldNames = ", ".join(fieldsToBeStored.keys())
                fieldValuesStr = ",".join(fieldValues)
                sql = "insert into m3_cartographicmodel.%s (%s, %s) values (%s, ST_GeomFromText('%s', 5514));\n" % (self.tableName, fieldNames, self.geometryFieldName, fieldValuesStr, feature.wkt)
                if sql.find('$happenies') >= 0:
                    print sql
                database.execute(sql)


# @NO-PRODUCTION CODE
if __name__ == "__main__":
    log.createLogger("mapgraphic.symbolization.bridge.debug")
    import base.config as config
    from shapely.wkt import loads

    debug = DebugProfile(propertiesMapping={"happenies_value": "$happenies"})
    debug.clearTable()

    element = loads("Polygon ((-823513.45441961172036827 -1132328.67423133295960724, -823505.43875900970306247 -1132322.25736112194135785, -823508.95279737829696387 -1132321.86808699904941022, -823514.23663852375466377 -1132326.09802193893119693, -823513.45441961172036827 -1132328.67423133295960724))")
    element.happenies = 56
    debug.save(element)