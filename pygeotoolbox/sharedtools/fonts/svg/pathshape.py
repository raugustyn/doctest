#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"

import pygeotoolbox.sharedtools.log as log
from base import *
from pathshapeitem import PathShapeItem, pathKeys


class PathShape:
    def __init__(self, shapeDef, precision):
        self.vertexes = getPathVertexes(shapeDef, precision)


    def old__init__(self, shapeDef, penPosition):
        self.shapeItems = []
        self.vertexes = []
        shapeItemsDef = strToListByKeys(shapeDef, pathKeys)
        for shapeItemDef in shapeItemsDef:
            itemCode, itemParams = shapeItemDef
            log.debug(itemParams)
            itemParams = map(float, itemParams.split(" "))
            shapeItem = PathShapeItem(itemCode, itemParams, penPosition)
            self.vertexes.extend(shapeItem.vertexes)
            self.shapeItems.append(shapeItem)
        if self.vertexes:
            firstVertex = self.vertexes[0]
            self.vertexes.append(Point(firstVertex.x, firstVertex.y))

    @property
    def wkt(self):
        return "Polygon((%s))" % (", ".join(map(lambda point:'%f %f' % (point.x, point.y), self.vertexes)))

    def __repr__(self):
        return "PathShape(%d items, %d vertexes, '%s')" % (len(self.shapeItems), len(self.vertexes), self.wkt)



if __name__ == "__main__":
    d = "M828 131q-100 -85 -192.5 -120t-198.5 -35q-175 0 -269 85.5t-94 218.5q0 78 35.5 142.5t93 103.5t129.5 59q53 14 160 27q218 26 321 62q1 37 1 47q0 110 -51 155q-69 61 -205 61q-127 0 -187.5 -44.5t-89.5 -157.5l-176 24q24 113 79 182.5t159 107t241 37.5 q136 0 221 -32t125 -80.5t56 -122.5q9 -46 9 -166v-240q0 -251 11.5 -317.5t45.5 -127.5h-188q-28 56 -36 131zM813 533q-98 -40 -294 -68q-111 -16 -157 -36t-71 -58.5t-25 -85.5q0 -72 54.5 -120t159.5 -48q104 0 185 45.5t119 124.5q29 61 29 180v66z"
    penPosition = Point(0, 0)
    shapeDefs = d.split("z")
    for shapeDef in shapeDefs:
        shape = PathShape(shapeDef, penPosition)
