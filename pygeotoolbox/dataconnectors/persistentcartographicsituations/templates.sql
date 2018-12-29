-- # listSymbolNamesSQL List symbol names.
--
-- @representation_id ... 0
-- ------------------------------------------------------------------------------
with symbol_names as (
	select map_symbol from m3_persistent_representations.context_features
			where representation_id = 0
			group by map_symbol
)

select array_agg(map_symbol) from symbol_names;

-- # searchForEquivalentRealFeatureSQL Search for equivalent real features.
--
-- @id ... 1234
-- ------------------------------------------------------------------------------
with stored_feature as (
	select geom, st_buffer(geom, 0.3) as geom_buffer from m3_persistent_representations.context_features where id = 1234
),

context_mbr as (
	select * from m3_persistent_representations.representations  where representation_id = 5678
),

real_features_in_view as (
	select source_geom as geom, st_buffer(source_geom, 0.3) as geom_buffer  from data.elements as elements, context_mbr
		where source_elt_id = 'P4203000' and context_mbr.geom && source_geom
),

real_feature as (

	select * from real_features_in_view, stored_feature
		where st_contains(real_features_in_view.geom_buffer, stored_feature.geom) and st_contains(stored_feature.geom_buffer, real_features_in_view.geom)
)

select count(*) from real_feature;


-- # selectContextRealFeatures Select context real features.
--
-- ------------------------------------------------------------------------------
with context_mbr as (
	select * from m3_persistent_representations.representations  where representation_id = 0
)


select elm_id, source_elt_id from data.elements as elements, context_mbr
		where source_elt_id in ('L3020100', 'P4203000', 'L6060100', 'P3330000', 'L3060000') and context_mbr.geom && source_geom;

-- # cleanStatusSQL Clean status field.
--
-- ------------------------------------------------------------------------------
update m3_persistent_representations.context_features set status=null;
update m3_persistent_representations.cartographic_features set status=null;
update m3_persistent_representations.representations set status=null;