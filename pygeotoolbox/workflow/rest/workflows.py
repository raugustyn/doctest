#!c:/python27/python.exe
# -*- coding: utf-8 -*-
from workflow.workflowsequence import WorkflowSequence

__version__ = 0.1
import sys, os, urllib, codecs
import web # http://webpy.org/cookbook/
import sharedtools


TEPMLATE_RequestNotHandled = """
<p style="text-align:left">
<table>
    <tr><td><a href="Workflows">Workflows</a></td><td>Registered workflows</td></tr>
</table>
<hr>
<h4>Request Details</h4>
<p>Path: #PATH#</p>
<table>
#QUERY_LINES#
</table>
</p>
"""

import sharedtools.log as log
if __name__ == "__main__":
    logger = log.createLogger("workflows")

from workflow import getRegisteredWorkflows, WorkflowItem
from workflow import buildHTMLPageContent
from workflow.rest import buildFloatingListPage

import sharedtools.config as config


workflowItems = None
defaultPath = "workflows"
__paths = { }

def registerPath(path, requestProcessor):
    global __paths

    path = path.lower()
    __paths[path] = requestProcessor


class HTTPResponse():
    def __init__(self, handled, mimeFormat = "text/html", htmlData = ""):
        self.handled = handled
        self.mimeFormat = mimeFormat
        self.htmlData = htmlData

urls = ('/(.*)', 'handler', 'createsituation')

def ProcessRequest(fullPathList, queryParams, response):
    global _registeredRunObjects, workflowItems

    if fullPathList:
        mainPath = fullPathList[0].lower()
        if mainPath == "workflows":
            if len(fullPathList) == 1:
                if len(workflowItems) == 0:
                    html = buildHTMLPageContent("Registrovaná workflow", "Žádná workflow nejsou registrována")
                else:
                    content = []
                    for workflowItem in workflowItems:
                        content.append({
                            "title" : workflowItem.caption,
                            "shortdesc" : workflowItem.getShortDescription(),
                            "link": 'workflows/' + workflowItem.id
                        })
                    html = buildFloatingListPage("Registrovaná workflow", "", content)
            else:
                workflowItem = WorkflowItem.getItemById(fullPathList[1])
                if workflowItem:
                    if len(fullPathList) == 3 and fullPathList[2].lower() == "execute":
                        startNumberOfLines = log.logger.getNumberOfLines()
                        workflowItem.execute()
                        lines = log.logger.getLines(startNumberOfLines-1, log.logger.getNumberOfLines()-1)
                        html = lines;
                    elif len(fullPathList) == 3 and fullPathList[2].lower() == "validate":
                        isValid, message = workflowItem.validate()
                        html = "%s:%s" % (str(isValid), message)
                    else:
                        html = workflowItem.getHTML()
                else:
                    html = buildHTMLPageContent("Requested Workflow", "%s not found!!!" % fullPathList[1])

        elif mainPath == "config":
            content = []
            for info in config.valueInfos.values():
                content.append({
                    "title": info.caption,
                    "shortdesc" : info.getFullDescription(),
                    "link": ""
                })
            html = buildFloatingListPage("Konfigurace", "", content)
            html = html.replace("height: 140px;", "height: 260px;")

        elif mainPath == "console":
            html = log.logger.getLines(0, None, "\n")
            response.mimeFormat = "text/plain"

        elif mainPath == "statusinfo":
            html = sharedtools.getStatusInfo()
            response.mimeFormat = "text/plain"

        elif mainPath == "values":
            if len(fullPathList) == 3 and fullPathList[2].lower() == "set":
                valueName = fullPathList[1]
                value = urllib.unquote(queryParams["newValue"])
                html = "%s=%s" % (valueName, value)
                config.setValue(valueName, value)
                config.save()

        elif mainPath in __paths:
            response = __paths[mainPath](fullPathList[1:], queryParams, response)
        else:
            html = "Empty"

        if not response.handled:
            response.handled = True
            response.htmlData = html

    if not response.handled:
        response.handled = True
        queryLines = ""
        for key, value in queryParams.iteritems():
            queryLines += "%s %s" % (key, value)

        if not queryLines:
            queryLines = "No query params provided."

        dynamicContent = TEPMLATE_RequestNotHandled
        dynamicContent = dynamicContent.replace("#QUERY_LINES#", queryLines)
        page = "/".join(fullPathList)
        if not page:
            page = "No script path provided in query."

        dynamicContent = dynamicContent.replace("#PATH#", page)

        html = buildHTMLPageContent("Workflow Manager", dynamicContent)

        response.htmlData = html

    return response


class WorkflowsApplication(web.application):
    def run(self, port, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ("localhost", port))

class handler:
    def doProcessRequest(self, page):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')

        if not page and defaultPath:
            web.header("Content-Type", "text/html;charset=utf-8")
            web.redirect(defaultPath)
            return None
        else:
            response = ProcessRequest(page.split("/"), web.input(), HTTPResponse(False))
            web.header("Content-Type", response.mimeFormat + ";charset=utf-8")
            return response.htmlData

    def GET(self, page):
        return self.doProcessRequest(page)

    def POST(self, page):
        return self.doProcessRequest(page)

def runServer(loggerName="RunWorkflowServer", port=65423, registeredWorkflows = None, aDefaultPath = None):
    global workflowItems, defaultPath

    if loggerName:
        import sharedtools.log as log
        logger = log.createLogger(loggerName)
        logger.debug("Configuration file:%s" % config.configFileName)

    if registeredWorkflows:
        if isinstance(registeredWorkflows, list):
            workflowItems = registeredWorkflows
        elif isinstance(registeredWorkflows, WorkflowItem) or isinstance(registeredWorkflows, WorkflowSequence):
            workflowItems = [registeredWorkflows]
            defaultPath = "workflows/" + registeredWorkflows.id
    else:
        workflowItems = getRegisteredWorkflows()

    if aDefaultPath:
        defaultPath = aDefaultPath

    import os
    if os.environ.has_key('SERVER_SOFTWARE'):
        import cgi
        import cgitb
        cgitb.enable()

        form = cgi.FieldStorage()
        if os.environ.has_key('PATH_INFO'):
            pathInfo = os.environ['PATH_INFO']
        else:
            pathInfo = ""
        if pathInfo[:1] == "/":  pathInfo = pathInfo[1:]

        fullPathList = pathInfo.replace("//", "/")
        fullPathList = fullPathList.split("/")  # REST parametry

        query = {}
        queryList = form.list
        for item in queryList:
            decodedValue = urllib.unquote(item.value)
            try:
                decodedValue = unicode(decodedValue, "utf-8")
            except:
                decodedValue = codecs.decode(decodedValue, "latin-1")
            decodedValue = urllib.unquote(decodedValue)
            query[item.name] = decodedValue

        response = ProcessRequest(fullPathList, query, HTTPResponse(False))

        if response.mimeFormat in ["text/html", "text/javascript", "text/plain"]:
            print "Content-Type: " + response.mimeFormat + ";charset=utf-8"  # HTML is following
            print  # blank line, end of headers
            sys.stdout.write(response.htmlData.encode('utf-8'))
        else:
            print "Content-Type: " + "application/octet-stream"  # response.mimeFormat
            print  # blank line, end of headers
            if sys.platform != "win32":
                sys.stdout.write(response.htmlData)
                sys.stdout.flush()
            else:
                import os, msvcrt

                msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
                sys.stdout.write(response.htmlData)
                sys.stdout.flush()
                msvcrt.setmode(sys.stdout.fileno(), os.O_TEXT)

    else:
        app = WorkflowsApplication(urls, globals())
        app.run(port=port)