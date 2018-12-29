-- # buildNodesTable Create nodes table
--
-- @sequenceName ... name of the temporary sequence (temp_seq)
-- @sourceTableName ... source table name including schema (datasubset.z_terennirelief_l)
-- @sourceGeometryField ... source geometry (wkb_geometry)
-- @nodesTableName ... output nodes table name including schema (nodes_table)
-- @nodeTypeFieldName ... 1 for start point, 2 for endpoint (node_type)
-- ------------------------------------------------------------------------------

-- create sequence for row_number
drop sequence if exists temp_seq;
create temporary sequence temp_seq;

-- build nodes table
drop table if exists nodes_table;
create temporary table nodes_table as
	select nextval('temp_seq') As row_number, node_type, ogc_fid, geom from
		(
			(select 1 as node_type, ogc_fid, st_startpoint((ST_Dump(wkb_geometry)).geom) as geom from datasubset.z_terennirelief_l)
			union
			(select 2 as node_type,  ogc_fid, st_endpoint((ST_Dump(wkb_geometry)).geom) as geom from datasubset.z_terennirelief_l)
		) as input_data;

-- clean after process
drop sequence temp_seq;

-- # dropTable Drops nodes table
--
-- @tableName ... Table name including schema to be dropped (nodes_table)
-- ------------------------------------------------------------------------------
drop table if exists nodes_table;
