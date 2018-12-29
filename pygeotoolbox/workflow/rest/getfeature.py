#!c:/python27/python.exe
# -*- coding: utf-8 -*-
__version__ = 0.1
import sys, os

basePath = "C:/ms4w/Apache/htdocs/Generalizace/TB04CUZK001_CartoModel".replace("/", os.sep)
if not basePath in sys.path:
    sys.path.append(basePath)

if __name__ == "__main__":
    from logging import INFO
    from pygeotoolbox.sharedtools.log import createLogger;
    logger = createLogger("getfeature", level=INFO)

createTableSQL = """
drop table if exists  temp.zavrty;
create table temp.zavrty as (
	select row_number() over() as id, ogc_fid, geom from (
		select ogc_fid, st_astext((st_dump(wkb_geometry)).geom) as geom from public.z_terennirelief_l where ruleid_zm10 = 6
	) as d1
)
"""

def getSQLRow(sql):
    import psycopg2

    connection = psycopg2.connect("dbname=data10 user=postgres password=postgres")
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()

    return result


def getWKT(feature):
    if feature:
        return feature.toWKT()
    else:
        return ""


def getPropustkyResult(form):
    from json import dumps

    if "index" in form:
        index = form["index"].value.lower()
        if index == "min":
            sql = "select min(ogc_fid) from datasubset.z_komobjekt_b where znacka=2850001"
            index = getSQLRow(sql)[0]
            whereOperator = "="
        elif index == "max":
            sql = "select max(ogc_fid) from datasubset.z_komobjekt_b where znacka=2850001"
            index = getSQLRow(sql)[0]
            whereOperator = "="
        else:
            index = int(index)
            if "operator" in form:
                operator = form["operator"].value.lower()
            else:
                operator = "equal"

            whereOperator = {
                "lessthan" : "<",
                "equal" : "=",
                "greatherthan" : ">"
            }[operator]

        sql = "select ogc_fid, st_astext(wkb_geometry) from datasubset.z_komobjekt_b where znacka=2850001 and ogc_fid %s %d limit 1" % (whereOperator, index)

        row = getSQLRow(sql)
        from model.feature.geo import wktToFeature
        from generalization.streampasses.streampassesfinder import StreamPassLineGenerator

        if row:
            streamPass = wktToFeature(row[1], row[0])
            generator = StreamPassLineGenerator(streamPass)
            try:
                (edge, passLengt, passOrientation) = generator.getPassEdge()
            finally:
                pass

            jsonStr = {
                "ogc_fid" : row[0],
                "wkt": row[1],
                "centerLine" : getWKT(generator.centerLine),
                "edge" : getWKT(edge)
            }
            row = dumps(jsonStr, indent=4)
        else:
            row = ""

    return row

def getZavrtyResult(form):
    if "index" in form:
        id = int(form["index"].value) + 1

        format = "application/json"
        import psycopg2
        from pygeotoolbox.sharedtools import planarmath
        from pygeotoolbox.sharedtools.circletools.circletools import calculateCircleToFit
        from shapely.geometry import Point
        from json import dumps
        from shapely.wkt import loads

        result = { "version": 1.0, "caption" : "Závrty"}

        connection = psycopg2.connect("dbname=data10 user=postgres password=postgres")
        cursor = connection.cursor()
        row = cursor.firstRowFromSelect("select ogc_fid, geom from temp.zavrty where id=%d" % (id))
        geometry = loads(row[1])
        vertexes = []
        for coordinate in geometry.coords:
            (x, y) = coordinate
            vertexes.append(planarmath.Point(x, y))
        (circle, variation) = calculateCircleToFit(vertexes)
        origin = Point(circle.origin.x, circle.origin.y)
        buffer = origin.buffer(circle.radius, resolution=45)

        result["optimalCircle"] = {
            "wkt" : buffer.wkt,
            "radius" : circle.radius,
            "origin" : origin.wkt
        }

        result["inputFeature"] = {
            "ogc_fid": row[0],
            "wkt" : row[1]
        }

        cursor.close()
        connection.close()

        return dumps(result, indent=4)
    else:
        return None

if __name__ == "__main__":
    # Nastavení znakové sady na utf-8
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    import os

    pathInfo = ""
    if os.environ.has_key('SERVER_SOFTWARE'):
        import cgitb, cgi
        cgitb.enable()
        form = cgi.FieldStorage()
        if os.environ.has_key('PATH_INFO'):
            pathInfo = os.environ['PATH_INFO']
    else:
        class Field1:value="53473"
        class Field2:value="Propustky"
        class Field3:value="greatherthan"
        form = { "index" : Field1(), "profile" : Field2(), "operator": Field3()}

    if "profile" in form and form["profile"].value == "Propustky":
        row = getPropustkyResult(form)
    elif "profile" in form and form["profile"].value == "Zavrty":
        row = getZavrtyResult(form)
    else:
        format = "text/html"
        row = """Script for loading data in WKT format. You must provide index parameter.<br>
<br>
Script name:%s<br>
Path info:%s<br>
<br>
Try:<br>
<a href="?profile=Zavrty&index=1">?profile=Zavrty&index=1</a><br>
<a href="?profile=Propustky&index=min">?profile=Propustky&index=min</a>
""" % (str(__file__), pathInfo)

    print "Content-Type: %s;charset=utf-8" % format
    print  # blank line, end of headers
    print row