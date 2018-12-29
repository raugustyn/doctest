import json, codecs
from config import *
import os

def readSelectedFeatures(iface):
    jsonFeatures = []
    layer = iface.activeLayer()
    selection = layer.selectedFeatures()
    for feature in selection:
        jsonFeature = {}
        jsonFeature["feature_class"] = layer.name()
        for field in feature.fields():
            name = field.name()
            if name in config.FIELDS_TO_BE_STORED:
                jsonFeature[name] = feature.attribute(name)
        jsonFeature["wkt_geometry"] = feature.geometry().exportToWkt()
        jsonFeatures.append(jsonFeature)
        
    return jsonFeatures
    
class Situation:
    def __init__(self, id):
        self.id = id
        self.json = {
            "name" : config.FILENAME_BASE + self.id,
            "inputFeatures" : [],
            "outputFeatures": []
        }
        self.load()
        
    def getStoreFileName(self):
        return config.STORE_PATH + config.FILENAME_BASE + self.id + ".json"
        
    def load(self):
        if os.path.exists(self.getStoreFileName()):
            inFile = codecs.open(self.getStoreFileName(), "r", config.ENCODING)
            self.json = json.load(inFile)
            inFile.close()
        
    def save(self):
        outFile = codecs.open(self.getStoreFileName(), "w", config.ENCODING)
        outFile.write(json.dumps(self.json, indent=4).encode(config.ENCODING))
        outFile.close()
        