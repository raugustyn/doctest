-- ########################################################################
--
-- createCartographicRepresentationsTables
--
-- ########################################################################

-- context_features table
drop table if exists m3_persistent_representations.context_features;
create table m3_persistent_representations.context_features (
  id serial,
  feature_id integer,
  representation_id integer,
  geom Geometry(Geometry, 5514),
  map_symbol text,
  status integer,
  CONSTRAINT context_features_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
CREATE INDEX context_features_geom_idx  ON m3_persistent_representations.context_features USING gist (geom);

-- cartographic_features table
drop table if exists m3_persistent_representations.cartographic_features;
create table m3_persistent_representations.cartographic_features (
  id serial,
  feature_id integer,
  representation_id integer,
  geom Geometry(Geometry, 5514),
  map_symbol text,
  cartographic_operation text,
  status integer,
  CONSTRAINT cartographic_features_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
CREATE INDEX cartographic_features_geom_idx  ON m3_persistent_representations.cartographic_features USING gist (geom);

-- representations table
drop table if exists m3_persistent_representations.representations;
create table m3_persistent_representations.representations (
  id serial,
  representation_id integer,
  geom Geometry(Polygon, 5514),
  caption text,
  status integer,
  CONSTRAINT representations_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
CREATE INDEX representations_geom_idx  ON m3_persistent_representations.representations USING gist (geom);


-- m3_persistent_representations.load_statistics table
drop table if exists m3_persistent_representations.load_statistics;
create table m3_persistent_representations.load_statistics (
  last_update_timestamp text
)