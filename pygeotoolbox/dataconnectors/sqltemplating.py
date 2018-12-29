SECTIONS_DELIMETER = "-- #"
PARAMETERS_DELIMETER = "-- @"

class SQLProcedure:


    def __init__(self, sqlCommands, template):
        template = template.strip()
        self.sqlCommands = sqlCommands
        self.name = None
        self.params = {}
        self.paramNames = []
        self.sqlTemplate = ""
        self.isSelectQuery = None

        if template:
            self.template = template
            lines = template.split("\n")
            sqlTemplate = []
            for line in lines:
                if self.name:
                   line = line.strip()
                   if line.startswith(PARAMETERS_DELIMETER):
                       delimeterPosition = line.find("...")
                       paramName = line[4:delimeterPosition].strip()
                       paramDescription = line[delimeterPosition+3:].strip()
                       self.params[paramName] = paramDescription
                       self.paramNames.append(paramName)
                   elif not line.startswith("--") and line:
                       sqlTemplate.append(line)
                else:
                    line = line[len(SECTIONS_DELIMETER):].strip()
                    self.name = line[:line.find(" ")]
            self.sqlTemplate = "\n".join(sqlTemplate)
            self.isSelectQuery = self.sqlTemplate.lower().startswith("select") or self.sqlTemplate.lower().startswith("with") or self.name.startswith('select')


    def __str__(self):
        return "SQLProcedure.%s(%s)" % (self.name, str(self.params))


    def __repr__(self):
        return "SQLProcedure.%s(%s)" % (self.name, str(self.params))


    def nameToId(self, name):
        if name in self.params:
            details = self.params[name].strip()
            result = details[details.find("(")+1:details.rfind(")")].strip()
        else:
            result = None

        return result


    def getValues(self, *args, **kwargs):
        values = {}
        if args:
            index = 0
            for arg in args:
                values[self.paramNames[index]] = arg
                index += 1

        if kwargs:
            for key, value in kwargs.iteritems():
                values[key] = value

        return values

    def __call__(self, *args, **kwargs):
        values = self.getValues(*args, **kwargs)
        if self.isSelectQuery:
            return self.executeSelectSQL(values)
        else:
            self.execute(values)


    def getSQLfromValues(self, values):
        sql = self.sqlTemplate
        for name, value in values.items():
            replaceId = self.nameToId(name)
            if replaceId:
                sql = sql.replace(replaceId, str(value))

        return sql


    def getSQL(self, *args, **kwargs):
        values = self.getValues(*args, **kwargs)
        return self.getSQLfromValues(values)

    def executeWithArgs(self, *args):
        values = {}

        print self.name, "executeWithArgs", str(args), str(values)


    def execute(self, values):
        sql = self.getSQLfromValues(values)

        self.sqlCommands.executeSQL(sql)


    def executeSelectSQL(self, values):
        sql = self.getSQLfromValues(values)

        return self.sqlCommands.connection.executeSelectSQL(sql)


    def getHeader(self):
        items = []
        for param, defValue in self.params.iteritems():
            items.append("%s=%s" % (param, str(defValue)))

        return "%s(%s)" % (self.name, ", ".join(items))


class SQLCommands:


    def __init__(self, connection, sqlFileName = None):
        self.connection = connection
        self.procedures = {}
        self.procedureDecrators = {}
        self.__sqlBuffer = None
        self.setBufferSize(0)
        if sqlFileName:
            self.load(sqlFileName)


    def __del__(self):
        self.clearBuffer()


    def setBufferSize(self, size):
        def executeSQLNoBuffer(sql):
            self.connection.execute(sql)

        def executeSQLWithBuffer(sql):
            self.__sqlBuffer = self.connection.executeBuffer(sql, self.__sqlBuffer, self.__bufferSize)

        self.clearBuffer()
        if size > 1:
            self.__sqlBuffer = []
            self.executeSQL = executeSQLWithBuffer
        else:
            self.__sqlBuffer = None
            self.executeSQL = executeSQLNoBuffer

        self.__bufferSize = size


    def clearBuffer(self):
        self.__sqlBuffer = self.connection.clearBuffer(self.__sqlBuffer)


    def __getDecorator(self, decoratorId):
        if decoratorId in self.procedureDecrators:
            return self.procedureDecrators[decoratorId]
        else:
            return None


    def getProcedureHeaders(self):
        items = []

        for procedure in self.procedures.values():
            items.append(procedure.getHeader())

        return "\n".join(items)


    def __registerDecorator(self, decorator):
        self.procedureDecrators[id(decorator)] = decorator
        setattr(self, decorator.name, decorator)


    def loads(self, sql, doAppend = True):
        assert isinstance(sql, basestring), "sql parameter must be string"
        assert sql <> "", "sql parameter must not be empty string"

        if not doAppend:
            for proc in self.procedures:
                delattr(self, proc.name)
            self.procedures = {}

        for item in sql.split(SECTIONS_DELIMETER):
            item = item.strip()
            if item:
                proc = SQLProcedure(self, SECTIONS_DELIMETER + item)
                self.procedures[proc.name] = proc
                self.__registerDecorator(proc)


    def __str__(self):
        return "SQLWrapper(%s)" % (",".join(self.procedures.keys()))


    def load(self, fileName, doAppend = True, encoding = "utf-8"):
        assert isinstance(fileName, basestring)
        import codecs

        fileStream = codecs.open(fileName, "r", encoding)
        data = fileStream.read()
        fileStream.close()

        return self.loads(data, doAppend)


    def execute(self, commandName, **kwargs):
        if commandName in self.procedures:
            self.procedures[commandName].execute(kwargs)
            pass


    def executeSelectSQL(self, commandName, **kwargs):
        if commandName in self.procedures:
            return self.procedures[commandName].executeSelectSQL(kwargs)


###############################################################################
# NO-PRODUCTION CODE
###############################################################################
if __name__ == "__main__":

    class PrintSQLConnection:
        def execute(self, sql, doCommit=False):
            print sql


        def executeSelectSQL(self, sql, doCommit=False):
            print sql



    connection = PrintSQLConnection()

    if False:
        commands = SQLCommands(connection)
        commands.load("sqlcommands.sql")
        print commands
        for proc in commands.procedures:
            print "\t", proc
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

    if True:
        from pygeotoolbox.sharedtools import normalizePath
        from dataconnectors import connection as database

        commands = SQLCommands(database)
        commands.load(normalizePath("generalization/dissolverings.sql"))
        print commands
        for procName, proc in commands.procedures.iteritems():
            print "\t", proc.getHeader()
        print

        commands.dropTemporaryTables()
