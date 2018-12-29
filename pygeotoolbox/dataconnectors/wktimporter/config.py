class Config:
    MASTER_GEOMETRY_FIELDNAME = "wkb_geometry"
    SCHEMA = "public"
    SQL_FILE_EXTENSION = ".sql"
    DATABASE_NAME = "gensmd"
    PQSL_TEMPLATE = '"c:/Program Files/PostgreSQL/9.5/bin/psql.exe" -U postgres -q -d %s -f %s\n' % DATABASE_NAME
    ID_FIELD_NAME = "zdroj_id"
    PG_CONNECTOR = "dbname=%s user=postgres" % DATABASE_NAME

config = Config()