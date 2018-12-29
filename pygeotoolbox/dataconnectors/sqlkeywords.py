#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"

import sharedtools.config as config

sqlKeywords = {}
sqlKeywordsValues = {}

def buildSqlKeywordsValues():
    global sqlKeywordsValues

    sqlKeywordsValues = {}
    for key, value in sqlKeywords.iteritems():
        value = config.getValue(value)
        if value <> key:
            sqlKeywordsValues[key] = value

def registerSQLKeyword(keyword, valueIdentifier):
    sqlKeywords[keyword] = valueIdentifier
    config.registerChangeListener(buildSqlKeywordsValues, [valueIdentifier])
    buildSqlKeywordsValues()
