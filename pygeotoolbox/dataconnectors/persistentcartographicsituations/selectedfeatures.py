from config import *

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
