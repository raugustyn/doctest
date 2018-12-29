#  -*- coding: utf-8 -*-
###########################################################
#                                                         #
# Copyright (c) 2018 Radek Augustýn, licensed under MIT.  #
#                                                         #
###########################################################

__author__ = "radek.augustyn@email.cz"
# @PRODUCTION MODULE [Full]

from base import fileRead

templates = { }

def registerTemplate(templateName, fileName, content = None):
    templates[templateName] = (fileName, content)

templates["sample"] = (None, 'ahoj<div id="mojeTestId"><p class="caption">Moje Caption</p><p class="shortDescription">Moje shortDescription</p><p class="description">Moje dDescription</p></div>')

def getTemplate(name):
    """Returns HTML template content. For the first time in a given template it reads data from the file.

    :param String name: Name of the template.
    :return String: Template HTML content.

    >>> print getTemplate("sample")
    ahoj<div id="mojeTestId"><p class="caption">Moje Caption</p><p class="shortDescription">Moje shortDescription</p><p class="description">Moje dDescription</p></div>

    """
    if name in templates:
        fileName, content = templates[name]
        if not content:
            content = fileRead(fileName)
            registerTemplate(name, fileName, content)

        return content
    else:
        return ""

def getHtmlDiv(templateName, identifier):
    """Extracts content of the html DIV element with given id. There must not be another div inside.

    :param String templateName: Name of the template in the templates list.
    :param String identifier: Id of the selected DIV element.
    :return String: Content of DIV element with given id.

    >>> getHtmlDiv("sample", "mojeTestId")
    '<p id="caption">Moje Caption</p><p id="shortDescription">Moje shortDescription</p><p id="description">Moje dDescription</p>'

    """
    html = getTemplate(templateName)
    startPos = html.find('<div id="%s"' % identifier)
    startPos = html.find(">", startPos)
    endPos = html.find('</div>', startPos)
    if  startPos >= 0 and endPos >= 0:
        return html[startPos+1:endPos]
    else:
        return ""

def getHtmlItems(templateName, identifier):
    """

    :param templateName:
    :param identifier:
    :return:

    >>> getHtmlItems("sample", "mojeTestId")
    {'caption': 'Moje Caption', 'shortDescription': 'Moje shortDescription', 'description': 'Moje dDescription'}
    """
    result = {}
    divContent = getHtmlDiv(templateName, identifier)
    for paragraph in divContent.split("</p>"):
        paragraph = paragraph.strip()
        if paragraph and paragraph.startswith("<p"):
            classNameStart = paragraph.find('class="') + 7
            classNameEnd = paragraph.find('"', classNameStart)
            className = paragraph[classNameStart:classNameEnd]
            content = paragraph[paragraph.find(">") + 1:]
            result[className] = content

    return result

def setAttrsFromHTML(obj, templateName, identifier):
    """

    :param obj:
    :param templateName:
    :param identifier:
    :return:

    >>> class A:pass
    >>> a = A
    >>> setAttrsFromHTML(a, "sample", "mojeTestId")
    >>> a.caption
    """
    for key, value in getHtmlItems(templateName, identifier).iteritems():
        setattr(obj, key, value)

class HTMLFormatter:
    def __init__(self):
        self.html = ""
        self._indent = 0
        self.indentStr = ""

    def add(self, str):
        self.html += str

    def addLine(self, str):
        for i in range(self._indent):
            str = "\t" + str
        self.add(str + "\n")

    def addLineAndIndent(self, str):
        self.addLine(str)
        self.indent()

    def unIndentAndAddLine(self, str):
        self.unIndent()
        self.addLine(str)

    def indent(self, count = 1):
        self._indent = self._indent + count

    def unIndent(self, count = 1):
        self._indent = self._indent - count
        if self._indent < 0 :
            self._indent = 0