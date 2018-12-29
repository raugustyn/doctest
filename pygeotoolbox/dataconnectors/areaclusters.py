from pygeotoolbox.sharedtools import printEvery100rows

_printCount = 0

import sys

def printEvery100rows(rowCount):
    global _printCount
    if rowCount % 100 == 0:
        if _printCount == 0:
            pref = ""
        else:
            pref = "..."
        sys.stdout.write(pref + str(rowCount))
        _printCount = _printCount + 1
        if _printCount == 10:
            _printCount = 0
            print

class SearchForClusterNumber:
    TEMP_SCHEMA = "temp"
    TENP_TABLENAME = "temp_searchforclusternumber"
    TEMP_FULLTABLENAME = "%s.%s" % (TEMP_SCHEMA, TENP_TABLENAME)
    GROUP_NUMBER_FIELDNAME = "group_number"

    def __init__(self, connection, selectSQL, geomFieldName, idFieldName):
        self.connection = connection
        self.selectSQL = selectSQL
        self.geomFieldName = geomFieldName
        self.idFieldName = idFieldName
        self.groupConnectionCursor = None
        self.updateCursor = None
        self.nextGroupNumber = 0
        self.rowCount = None
        self.maxOverlapsCount = None

    def buildTempTable(self):
        print "SearchForClusterNumber.buildTempTable"
        createTempTableSQL = "drop table if exists %s;\n" % self.TEMP_FULLTABLENAME
        createTempTableSQL += "create table %s as %s;\n" % (self.TEMP_FULLTABLENAME, self.selectSQL)
        createTempTableSQL += "alter table %s add column %s integer;\n" % (self.TEMP_FULLTABLENAME, self.GROUP_NUMBER_FIELDNAME)
        createTempTableSQL += "CREATE INDEX sidx_%s_%s ON %s USING gist (%s);" % (self.TENP_TABLENAME, self.geomFieldName, self.TEMP_FULLTABLENAME, self.geomFieldName)
        self.connection.execute(createTempTableSQL)

    def getNextEmptyId(self):
        walkCursor = self.connection.executeSelectSQL("select %s from %s where %s is null limit 1" % (self.idFieldName, self.TEMP_FULLTABLENAME, self.GROUP_NUMBER_FIELDNAME))
        row = walkCursor.fetchone()
        if row:
            return row[0]
        else:
            return None

    def updateGroupNumber(self, id, groupNumber):
        self.rowCount = self.rowCount + 1
        printEvery100rows(self.rowCount)
        updateSQL = "update %s set %s=%d where %s=%s" % (self.TEMP_FULLTABLENAME, self.GROUP_NUMBER_FIELDNAME, groupNumber, self.idFieldName, str(id))
        self.updateCursor.execute(updateSQL)
        self.connection.connection.commit()

    def renameGroupNumber(self, oldGroupNumber, newGroupNumber):
        updateSQL = "update %s set %s=%d where %s=%s" % (self.TEMP_FULLTABLENAME, self.GROUP_NUMBER_FIELDNAME, newGroupNumber, self.GROUP_NUMBER_FIELDNAME, oldGroupNumber)
        self.updateCursor.execute(updateSQL)
        self.connection.connection.commit()

    def buildCluster(self, anchorIdValue, anchorGroupNumber = None):
        groupNumber = None
        selectSQL = "select d2.%s, d2.%s from %s d1, %s d2 where d1.ogc_fid = %s and d1.ogc_fid <> d2.ogc_fid and st_overlaps(d1.geom, d2.geom)" % \
              (self.GROUP_NUMBER_FIELDNAME, self.idFieldName, self.TEMP_FULLTABLENAME, self.TEMP_FULLTABLENAME, str(anchorIdValue))

        self.groupConnectionCursor.execute(selectSQL)
        rows = self.groupConnectionCursor.fetchall()
        emptyIds = []
        if rows:
            if not self.maxOverlapsCount or self.maxOverlapsCount < len(rows):
                self.maxOverlapsCount = len(rows)


            groupNumbers = []
            groupIds = []
            for row in rows:
                groupIds.append(row[1])
                if row[0]:
                    if row[0] not in groupNumbers:
                        groupNumbers.append(row[0])
                else:
                    emptyIds.append(row[1])

            groupNumbers = sorted(groupNumbers)
            if groupNumbers:
                groupNumber = groupNumbers[0]
                for groupNumberToBeRenamed in groupNumbers[1:]:
                    self.renameGroupNumber(groupNumberToBeRenamed, groupNumber)

            if not groupNumber:
                self.nextGroupNumber = self.nextGroupNumber + 1
                groupNumber = self.nextGroupNumber
        else:
            groupNumber = 0

        self.updateGroupNumber(anchorIdValue, groupNumber)

        for emptyId in emptyIds:
            self.updateGroupNumber(emptyId, groupNumber)

        for emptyId in emptyIds:
            self.buildCluster(emptyId)

    def execute(self):
        self.buildTempTable()
        rowCount = self.connection.getRowCount("%s.%s" % (self.TEMP_SCHEMA, self.TENP_TABLENAME))
        self.connection.execute("update temp.temp_searchforclusternumber set group_number = null")
        self.groupConnectionCursor = self.connection.connection.cursor()
        self.updateCursor = self.connection.connection.cursor()
        try:
            self.rowCount = 0
            emptyId = True
            while emptyId:
                emptyId = self.getNextEmptyId()
                if emptyId:
                    self.buildCluster(emptyId)

        finally:
            self.groupConnectionCursor.close()
            self.updateCursor.close()

if __name__ == "__main__":
    from dataconnectors import listenpostgis
    connector = listenpostgis.PostGISConnector("dbname=data10 user=postgres")

    #processor = SearchForClusterNumber(connector, "select ogc_fid, st_buffer(wkb_geometry, 22) as geom from datasubset.z_budova_p", "geom", "ogc_fid")
    #processor = SearchForClusterNumber(connector, "select ogc_fid, st_buffer(wkb_geometry, 15) as geom from public.z_stavebniobjekt_b where znacka = 1180100", "geom", "ogc_fid")
    processor = SearchForClusterNumber(connector, "select ogc_fid, st_buffer(wkb_geometry, 150) as geom from public.z_stavebniobjekt_b where znacka = 1260000", "geom", "ogc_fid")

    processor.execute()
    print ""
    print "maxOverlapsCount:", processor.maxOverlapsCount
    print "nextGroupNumber:", processor.nextGroupNumber

"""
update datasubset.z_budova_p
	set group_number = temp_searchforclusternumber.group_number
	from temp.temp_searchforclusternumber
	where z_budova_p.ogc_fid = temp_searchforclusternumber.ogc_fid;
"""