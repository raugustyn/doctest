import os
from config import *
from pygeotoolbox.sharedtools.base import pathLeaf, getExtension
from situation import *

class Situations:
    def __init__(self):
        self.situations = []
        self.tableDefinitions = {}

        for pathItem in os.listdir(config.STORE_PATH):
            (fileName, fileExtension) = os.path.splitext(pathItem)
            if os.path.isfile(config.STORE_PATH + pathItem) and pathItem.startswith(config.FILENAME_BASE) and fileExtension == config.JSON_EXTENSION:
                id = pathItem[len(config.FILENAME_BASE):pathItem.find(".")]
                situation = Situation(id)
                print situation.json
                self.situations.append(situation)

    def getTableDefinitions(self):
        self.tableDefinitions = {}

        def processFeature(feature):
            tableName = feature[config.FEATURE_CLASS_KEY]
            if tableName in self.tableDefinitions:
                tableDefinition = self.tableDefinitions[tableName]
            else:
                tableDefinition = []

            for key in feature:
                if key <> config.FEATURE_CLASS_KEY:
                    if key not in tableDefinition:
                        tableDefinition.append(key)
                    pass #print "\t", key

            self.tableDefinitions[tableName] = tableDefinition

        for situation in self.situations:
            for feature in situation.json["outputFeatures"]:
                processFeature(feature)
            for feature in situation.json["inputFeatures"]:
                processFeature(feature)


if __name__ == "__main__":
    situations = Situations()
    situations.getTableDefinitions()
    for tableName in situations.tableDefinitions:
        print tableName, ":", situations.tableDefinitions[tableName]
