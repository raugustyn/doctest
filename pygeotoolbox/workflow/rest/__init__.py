# -*- coding: utf-8 -*-

import sharedtools

def buildFloatingListPage(title, description, content):
    from json import dumps

    html = sharedtools.fileRead(sharedtools.basePath + "/workflow/FloatingList.html")
    contentScript = "<script language='JavaScript'>var info = { examples: %s};</script>" % dumps(content, indent=4)
    html = html.replace('<script language="JavaScript" src="example-list.js"></script>', contentScript)
    html = html.replace("<#DESCRIPTION#/>", title)

    return html