#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"


from sqlprocedure import SQLProcedure
from sqlcommands import SQLCommands


###############################################################################
# NO-PRODUCTION CODE
###############################################################################
if __name__ == "__main__":


    class PrintSQLConnection:
        """Dummy SQL database connector."""
        def execute(self, sql, doCommit=False):
            print sql


        def executeSelectSQL(self, sql, doCommit=False):
            print sql


        def clearBuffer(self, buffer):
            print "clearBuffer(%s)" % str(buffer)
            return []


    connection = PrintSQLConnection()

    if True:
        commands = SQLCommands(connection)
        commands.load("sqlcommands_example.sql")
        print commands
        for proc in commands.procedures:
            print "\t", proc
        print
        for procName, proc in commands.procedures.iteritems():
            print "\t", proc._getHeader()
        print

        print "Execute create nodes table command:"
        print "-----------------------------------"
        commands.execute("buildNodesTable",
            sequenceName = "temporarySequenceRenamed",
            sourceTableName="public.z_budovy_p",
            sourceGeometryField="wkb_geometry_renamed",
            nodesTableName="preprocessing.z_budovy_p_nodes"
        )
        print

        print "Execute drop table command:"
        print "---------------------------"
        commands.execute("dropTable", tableName="preprocessing.z_budovy_p_nodes")

    if False:
        from pygeotoolbox.sharedtools import normalizePath
        from dataconnectors import connection as database

        commands = SQLCommands(database)
        commands.load(normalizePath("generalization/dissolverings.sql"))
        print commands
        for procName, proc in commands.procedures.iteritems():
            print "\t", proc._getHeader()
        print

        commands.dropTemporaryTables()