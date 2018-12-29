#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"

"""Database mockup for logging demonstration.
"""

from random import randint


class Database:
    class __Cursor:
        def __init__(self):
            self.index = 0
            self.limit = 100
            self.fieldNames = []


        def query(self, sql):
            """
            Executes SQL select query.

            :param str sql: query to be executed.
            """
            SELECT_IDENTIFIER = "select"
            FROM_IDENTIFIER = "from"
            LIMIT_IDENTIFIER = "limit"

            self.fieldNames = []
            for delimeter in ["\t", "\n"]:
                sql = sql.replace(delimeter, " ")
            sql = sql.lower().replace("  ", " ")
            if sql.startswith(SELECT_IDENTIFIER) and sql.find(FROM_IDENTIFIER) > 0:
                self.fieldNames = sql[len(SELECT_IDENTIFIER):sql.find(FROM_IDENTIFIER)].strip().replace(" ", "").split(",")
                log.debug("fieldDefs=%s" % str(self.fieldNames))

            if sql.find(LIMIT_IDENTIFIER)>=0:
                self.limit = int(sql[sql.find(LIMIT_IDENTIFIER)+len(LIMIT_IDENTIFIER):].replace(";", "").strip())
                log.debug("limit=%d" % self.limit)


        def __iter__(self):
            """
            Iterates query rows.
            """
            return self


        def next(self):
            """
            Iterator next function. Returns next row in SQL query.

            :return:
            """
            if self.index > self.limit:
                raise StopIteration
            else:
                result = []
                for fieldName in self.fieldNames:
                    if fieldName == "id":
                        value = self.index
                    elif fieldName == "geom":
                        geomType = randint(0, 3)
                        if geomType == 0:
                            value = "POINT (30 10)"
                        elif geomType == 1:
                            value = "LINESTRING (30 10, 10 30, 40 40)"
                        else:
                            value = "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))"
                    else:
                        value = "%s_%d" % (fieldName, self.index)

                    result.append(value)

                self.index += 1
                return result


    def cursor(self):
        """
        Creates and returns new database cursor.

        :return:
        """
        return Database.__Cursor()


if __name__ == "__main__":
    from shapely.wkt import loads
    from shapely.geometry import Point, Polygon, LineString
    from point import processor as pointProcessor
    from linestring import processor as linestringProcessor
    from polygon import processor as polygonProcessor
    import pygeotoolbox.sharedtools.log as log

    processors = {
        Point: pointProcessor,
        Polygon: polygonProcessor,
        LineString: linestringProcessor
    }

    import point
    log.LOGGED_PROFILES = [point]
    database = Database()
    cursor = database.cursor()
    cursor.query("select id, name, geom from public.roads limit 13;")
    log.openSection("Reading database rows", level=log.DEBUG)
    for row in cursor:
        log.openSection("Processing row:%s" % str(row), level=log.DEBUG)
        shape = loads(row[2])
        if shape.__class__ in processors:
            processor = processors[shape.__class__]
            processor(shape)
        # else: element is skipped
        log.closeSection()
    log.closeSection()


