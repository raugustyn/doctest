import select
import time

import psycopg2
import psycopg2.extensions

from dataconnectors import listenpostgis
from model.feature import shapelyToFeature

pg = listenpostgis.PostGISConnector("dbname=data10 user=postgres")

def modifyGeometry(id):
    global listeningSuspended
    id = str(id)
    pgRow = pg.loadFeatures("select st_astext(geom) from temp.templstrings where id=%s" % str(id), 0)[0]
    feature = shapelyToFeature(pgRow.geometry)
    print feature
    for vertex in feature.vertexes:
        vertex.x = vertex.x + 20
    print feature

    pg.execute("UPDATE temp.templstrings SET generalized = ST_GeomFromText('%s', 5514) where id=%s;" % (str(feature), id))


def doListen():
    global listeningSuspended

    connection = pg.connection
    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    cursor.execute("LISTEN test;")
    print "Waiting for notifications on channel 'test'"
    while True:
        if select.select([connection],[],[],5) == ([],[],[]):
            print time.strftime("%H:%M:%S")
        else:
            connection.poll()
            while connection.notifies:
                notify = connection.notifies.pop(0)
                print time.strftime("%H:%M:%S"), "Got NOTIFY:", notify.pid, notify.channel, notify.payload
                modifyGeometry(notify.payload)

#modifyGeometry("4")
doListen()