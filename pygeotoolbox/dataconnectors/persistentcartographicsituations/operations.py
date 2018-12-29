#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"

class Operations:
    HIDE = 0
    CHANGE_GEOMETRY = 1

    defs = {
        0:['hide', "state=2, target_geom=null"],
        1:['change geometry', "state=1, target_geom=$geom$"]
    }

    @staticmethod
    def getCaption(operation):
        return Operations.defs[operation][0]


    @staticmethod
    def getSQLSetStatement(operation):
        return Operations.defs[operation][1]


    @staticmethod
    def captionToOperation(caption):
        for key, values in Operations.defs.iteritems():
            if values[0] == caption:
                return key

        raise "%s:Operation '%s' not found" % (__file__, caption)


    @staticmethod
    def captionToSQLSetStatement(caption):
        return Operations.getSQLSetStatement(Operations.captionToOperation(caption))

