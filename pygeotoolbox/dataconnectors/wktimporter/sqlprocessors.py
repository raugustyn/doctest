import os
from config import config


class SQLProcessor_SaveToIndividualFiles:
    def __init__(self, batchFileName = "importToPostGIS.bat", insertProfileEchos = False):
        self.outputFile = None
        self.batchFileName = batchFileName
        self.batchFile = None
        self.dropIndexSQL = ""
        self.insertProfileEchos = insertProfileEchos

    def __del__(self):
        self.closeFile()
        self.writeProfileEcho("Done.")
        if self.batchFile:
            self.batchFile.close()

    def closeFile(self):
        if self.outputFile:
            self.outputFile.write(self.dropIndexSQL)
            self.outputFile.close()

    def writeProfileEcho(self, msg, createFile = False):
        if self.insertProfileEchos and self.batchFile:
            self.batchFile.write("echo %%time%% %s %s import.log\n" % (msg, [">>", ">"][int(createFile)]))

    def assignFileName(self, fileName, tableName):
        assert fileName

        self.closeFile()
        sqlFileName = fileName + config.SQL_FILE_EXTENSION
        self.outputFile = open(sqlFileName, "w")
        createIndexSQL = "create index %s_%s_idx on public.%s (%s);\n" % (tableName, config.ID_FIELD_NAME, tableName, config.ID_FIELD_NAME)
        self.outputFile.write(createIndexSQL)
        self.dropIndexSQL = "drop index %s_%s_idx;\n" % (tableName, config.ID_FIELD_NAME)


        if not self.batchFile:
            self.batchFile = open(os.path.dirname(fileName) + os.sep + self.batchFileName, "w")
            self.writeProfileEcho("Starting batch.", True)

        self.batchFile.write(config.PQSL_TEMPLATE % os.path.basename(sqlFileName))
        self.writeProfileEcho(sqlFileName)
        self.batchFile.flush()

    def executeSQL(self, sql):
        assert sql

        if self.outputFile:
            self.outputFile.write(sql)
        else:
            raise Exception("sqlProcessor_SaveToIndividualFiles.execSQL(%s).\nassignFileName must be called first!!!" % sql)

    def commit(self):
        if self.outputFile:
            self.outputFile.flush()

class sqlProcessor_SaveToMergedFile:
    def __init__(self, mergedFileName = "wktImport.sql"):
        self.mergedFileName = mergedFileName
        self.outputFile = None

    def __del__(self):
        self.closeFile()

    def closeFile(self):
        if self.outputFile:
            self.outputFile.close()

    def assignFileName(self, fileName, tableName):
        if not self.outputFile:
            self.outputFile = open(os.path.dirname(fileName) + os.sep + self.mergedFileName, "w")

    def executeSQL(self, sql):
        assert sql

        if self.outputFile:
            self.outputFile.write(sql)
        else:
            raise Exception("sqlProcessor_SaveToIndividualFiles.execSQL(%s).\nassignFileName must be called first!!!" % sql)

    def commit(self):
        if self.outputFile:
            self.outputFile.flush()

class sqlProcessor_RunInPostGis:
    def __init__(self):
        import postgis
        self.rowCount = 0
        self.connection = postgis.pg

    def __del__(self):
        self.connection.commit()

    def assignFileName(self, fileName, tableName):
        pass

    def closeFile(self):
        pass

    def executeSQL(self, sql):
        self.connection.executeSQL(sql)

    def commit(self):
        self.connection.commit()
