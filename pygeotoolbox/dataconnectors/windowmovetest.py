#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"

import time
from dataconnectors import connection as database

RETRIEVE_CENTERPOINT_SQL = """
with center_point as (
	select ST_Line_Interpolate_Point ((st_dump(wkb_geometry)).geom, 0.5) as geom from public.z_terennirelief_l where ogc_fid = 200397
)

select st_Xmin(geom), st_Ymin(geom) from center_point"""

CREATE_TEMPTABLE_SQL = """
drop table if exists temp_candidates;
                    create temp table temp_candidates as
	                  select ogc_fid, wkb_geometry from public.z_komruzna_l where wkb_geometry && st_GeometryFromText('Linestring(-867921.0 -1017517.0, -865921.0 -1015517.0)', 5514)
	                  union all
	                  select ogc_fid, wkb_geometry from public.z_voda_l where wkb_geometry && st_GeometryFromText('Linestring(-867921.0 -1017517.0, -865921.0 -1015517.0)', 5514)
	                  union all
	                  select ogc_fid, wkb_geometry from public.z_komsilnice_l where wkb_geometry && st_GeometryFromText('Linestring(-867921.0 -1017517.0, -865921.0 -1015517.0)', 5514);

                      create index wkb_geometry_idx on temp_candidates using gist (wkb_geometry);"""

SEARCH_FORCANDIDATES_SQL = """
with master_element as (
	select wkb_geometry from public.z_terennirelief_l where ogc_fid = 200397
),

slave_elements as (
	select * from public.z_komruzna_l as slave_table, master_element
		where st_distance(master_element.wkb_geometry, slave_table.wkb_geometry) <= 100
)

select * from slave_elements
"""

FASTSEARCH_FORCANDIDATES_SQL = """
with master_element as (
	select wkb_geometry, st_buffer(wkb_geometry, 100) as search_geom from public.z_terennirelief_l where ogc_fid = 200397
),

slave_elements as (
	select * from public.z_komruzna_l as slave_table, master_element
		where search_geom && slave_table.wkb_geometry and st_distance(master_element.wkb_geometry, slave_table.wkb_geometry) <= 100
)

select * from slave_elements
"""

for elementID in [200397, 175151, 772893]:
    # Retrieving element center point
    centerX, centerY = database.executeSelectSQL(RETRIEVE_CENTERPOINT_SQL, { "200397": elementID} ).fetchone()

    print "Spatial window speed for element %d (%f, %f)" % (elementID, centerX, centerY)
    print "-----------------------------------------------------------------------------------------------"
    print "Dist   Select range                                   Elm count   Time      Fast query"
    for distance in [500.0, 1000.0, 5000.0, 10000.0, 20000.0, 30000.0, 50000.0]:
        # Calculating view extent
        delta = distance/2
        minX = centerX - delta
        minY = centerY - delta
        maxX = centerX + delta
        maxY = centerY + delta

        # Creating temporary table
        database.execute(CREATE_TEMPTABLE_SQL,
                     {
                         "-867921.0" : minX,
                         "-1017517.0": minY,
                         "-865921.0" : maxX,
                         "-1015517.0": maxY
                     }
        )

        # Reading selected row number
        rowCount = database.executeSelectSQL("select count(*) from temp_candidates;").fetchone()[0]

        # Querying via normal query
        startTime = time.time()
        candidates = database.executeSelectSQL(SEARCH_FORCANDIDATES_SQL, { "200397": elementID} )
        elapsedTime = time.time() - startTime

        # Querying via optimized query
        startTime = time.time()
        candidates = database.executeSelectSQL(FASTSEARCH_FORCANDIDATES_SQL, { "200397": elementID} )
        fastElapsedTime = time.time() - startTime

        # Printing results
        print "%5.0f (%8.0f, %8.0f, %8.0f, %8.0f) --> %5d elements %fs %fs" % (distance, minX, minY, maxX, maxY, rowCount, elapsedTime, fastElapsedTime)
    print