-- # prepareFontSchema Preparse font schema.
--
-- ------------------------------------------------------------------------------
create schema if not exists mg_fonts;

create table if not exists mg_fonts.fonts (
  id serial,
  name text,
  table_name text
);

-- # getFontInfo Gets font identifier.
--
-- @fontName ... Font name (Arial)
-- ------------------------------------------------------------------------------
select id, table_name from mg_fonts.fonts where name = 'Arial';

-- # registerFont Register font.
--
-- @fontName ... Font name (Arial)
-- @tableName ... Table name (arial_font)
-- ------------------------------------------------------------------------------
insert into mg_fonts.fonts (name, table_name) values('Arial', 'arial_font');

-- # createFontTable Register font.
--
-- @fontTableName ... Font name (font_table_name)
-- ------------------------------------------------------------------------------
drop table if exists mg_fonts.font_table_name;
create table if not exists mg_fonts.font_table_name (
  id serial,
  unicode_code integer,
  name text,
  geom Geometry(Geometry, 5514),
  letters Geometry(Geometry, 5514),
  footprint Geometry(Geometry, 5514)
);


-- # getFontInfos Retrieve font information records.
--
-- ------------------------------------------------------------------------------
select name, table_name from mg_fonts.fonts;


-- # getGlyphs Retrieves glyphs from glyphs table.
--
-- @glyphsTableName ... Glyphs table name (glyphs_table_name)
-- ------------------------------------------------------------------------------
select name, unicode_code, geom from mg_fonts.glyphs_table_name;
