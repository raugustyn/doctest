#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"


from base import *

class ReturnType:
    CURSOR = 0
    FIRST_RECORD_CONTENT = 1


class SQLProcedure:
    """ Class holding strored SQL procedure.
    """

    def __init__(self, sqlCommands, template):
        template = template.strip()
        self.sqlCommands = sqlCommands
        self.name = None
        self.params = {}
        self.paramNames = []
        self.sqlTemplate = ""
        self.isSelectQuery = None
        self.returnType = ReturnType.CURSOR

        if template:
            self.template = template
            lines = template.split("\n")
            sqlTemplate = []
            for line in lines:
                if self.name:
                   line = line.strip()
                   if line.find("return: first record content") >= 0:
                       self.returnType = ReturnType.FIRST_RECORD_CONTENT

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
        """Extracts identifier from name.

        :param name: name to be parsed
        :return: identifier parsed from name
        """
        if name in self.params:
            details = self.params[name].strip()
            result = details[details.find("(")+1:details.rfind(")")].strip()
        else:
            result = None

        return result


    def getValues(self, *args, **kwargs):
        """Extracts values from args and kwargs."""
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
        """Replaces values in a template by given parameters."""
        sql = self.sqlTemplate
        for name, value in values.items():
            replaceId = self.nameToId(name)
            if replaceId:
                sql = sql.replace(replaceId, str(value))

        return sql


    def getSQL(self, *args, **kwargs):
        """Extracts parameters from args and kwargs, apply them into template and return result. """
        values = self.getValues(*args, **kwargs)
        return self.getSQLfromValues(values)


    def execute(self, values):
        """Compiles SQL command from template and given parameter values, then execute it and commit. """
        sql = self.getSQLfromValues(values)

        self.sqlCommands.executeSQL(sql)


    def executeSelectSQL(self, values):
        """Compiles SQL query from template and given parameter values, then execute query and returns cursor on result. """
        sql = self.getSQLfromValues(values)

        result = self.sqlCommands.connection.executeSelectSQL(sql)

        if self.returnType == ReturnType.FIRST_RECORD_CONTENT:
            if result:
                result = result.fetchone()
                if result:
                    result = result[0]

        return result


    def _getHeader(self):
        """Returns definition header string. """
        items = []
        for param, defValue in self.params.iteritems():
            items.append("%s=%s" % (param, str(defValue)))

        return "%s(%s)" % (self.name, ", ".join(items))