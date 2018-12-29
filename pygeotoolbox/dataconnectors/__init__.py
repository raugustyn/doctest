#  -*- coding: utf-8 -*-
# @PRODUCTION MODULE
from pygeotoolbox.sharedtools import listToSqlStr, printRows
import postgis


from workflow import WorkflowItem
import sharedtools.config as config


def validateDatabaseConnection():
    import psycopg2

    try:
        paramString = postgis.buildConnectionParams(config.database.name, config.database.user, config.database.password, config.database.host)
        connection = psycopg2.connect(paramString)
        connection.close()

        return (True, "")

    except Exception as inst:
        return (False, "Connection to the PostGres database failed. psycopg2.connect('%s'). %s " % (paramString, str(inst)))

connection = None

databaseConnectionWorkflow = WorkflowItem("Napojení do databáze", "Nastavení napojení do pracovní databáze PostGIS.", None, True, True, paramNames=[
    "database.name",
    "database.user",
    "database.password",
    "epsg"
])
databaseConnectionWorkflow.validateProc = validateDatabaseConnection

def onConnectionParamsChange():
    if connection:
        connection.disconnect()
        connection.connectionParams = postgis.buildConnectionParams(config.database.name, config.database.user, config.database.password, config.database.host)

config.registerValue("database.name", "gensmd", "Databáze", "Jméno databáze v databázi PostGIS.",     onChange=onConnectionParamsChange)
config.registerValue("database.user", "postgres", "Uživatel", "Jméno uživatele v databázi PostGIS.",  onChange=onConnectionParamsChange)
config.registerValue("database.password", "postgres", "Heslo", "Jméno uživatele v databázi PostGIS.", onChange=onConnectionParamsChange)
config.registerValue("database.host", "localhost", "Server", "IP adresa serveru.")

connection = database = postgis.PostGISConnector()