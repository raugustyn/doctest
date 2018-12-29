if False:
    from qgis.core import QgsProject
    from PyQt4.QtCore import QFileInfo

import os

def getQGISProjectsInPath(path, projectName):
    result = []
    for pathItem in os.listdir(path):
        if not os.path.isfile(path + pathItem):
            projectFileName = path + pathItem + os.sep + projectName
            if os.path.exists(projectFileName):
                result.append(projectFileName)

    return result

def getQGISProjectsInTomasStructure(path, projectNameBase = "", shpSubDir = "shp"):
    result = []
    projectNameBase = projectNameBase.upper()
    for pathItem in os.listdir(path):
        if not os.path.isfile(path + pathItem):
            projectSubDir = path + pathItem + os.sep + shpSubDir + os.sep
            if os.path.exists(projectSubDir):
                for projectPathItem in os.listdir(projectSubDir):
                    if os.path.isfile(projectSubDir + projectPathItem) and projectPathItem.upper().endswith(".QGS"): # projectPathItem.upper().startswith(projectNameBase) and
                        print projectSubDir + os.sep + projectPathItem
                        result.append(projectSubDir + os.sep + projectPathItem)
            else:
                print "Error", projectSubDir

    return result

from pygeotoolbox.sharedtools import base
base.setupEncoding()
names = getQGISProjectsInTomasStructure("C:/Users/Radek Augustyn/Disk Google/TB04CUZK001/TB04CUZK001_WorkingGroup/09_NMet 03/01_Work/_portfolio situaci_nove/", "Kompozice", "shp")
print len(names)
#project = QgsProject.instance()
#print "processing projects"
#projectFileNames = getQGISProjectsInPath("C:/ms4w/Apache/htdocs/Generalizace/TB04CUZK001_TestDataSets_Daniela/", "Kompozice.qgs")
#for projectFileName in projectFileNames:
#    print "\treading", projectFileName
#    project.read(QFileInfo(projectFileName))
#print "Done"


