#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"


import codecs


class ModuleListBuilder:
    def __init__(self):
        self.clear()


    def clear(self):
        self.moduleList = []


    def addModule(self, name, description, path):
        self.moduleList.append((name, description, path))


    def saveToFile(self, fileName):
        content = "<html>\n\t<head>\n\t\t<style>\n\t\tbody { font-family:tahoma}\n\t</style>\n\t</head>\n\t<body>"
        content += "\n\t\t<table>"
        for (name, description, path) in self.moduleList:
            content += "\n\t\t\t<tr valign='top'>\n\t\t\t\t<td><a href='%s'>%s</a></td>\n\t\t\t\t<td>%s\n\t\t\t\t</td>\n\t\t\t</tr>" % (path, name, description)
        content += "\n\t\t</table>"
        content += "\n\t</body>\n</html>"
        codecs.open(fileName, "w", "utf-8").write(content)


moduleListBuilder = ModuleListBuilder()