#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"


CREATE_GLYPHSTABLE_SQL = """
create schema if not exists mg_temp;
drop table if exists mg_temp.glyphs_overview;
create table mg_temp.glyphs_overview (
  id serial,
  name text,
  unicode_name text,
  unicode_number integer,
  overview_geom Geometry(Geometry, 5514)
);
"""


if __name__ == "__main__":
    import pygeotoolbox.sharedtools.log as log
    from pygeotoolbox.database import database


