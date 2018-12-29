from situation import *
from selectedfeatures import *
           
def extendBySelectedFeatures(situationId, outputKey):           
    situation = Situation(situationId)
    selectedFeatures = readSelectedFeatures(iface)
    situation.json[outputKey].extend(selectedFeatures)
    #print json.dumps(situation.json, indent=4)
    situation.save()
    print "Append ", outputKey, "features:", len(selectedFeatures), "features inserted resulting in", len(situation.json[outputKey]), "records."
    
#extendBySelectedFeatures("01", "inputFeatures")
extendBySelectedFeatures("01", "outputFeatures")
