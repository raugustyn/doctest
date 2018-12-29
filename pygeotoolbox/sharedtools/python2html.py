#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"
# @PRODUCTION MODULE [Full]

from pygeotoolbox.sharedtools import setParameters


def convertCode(code, lexer="python", removeFirstDiv = True):
    import sys, os
    import pygments.cmdline
    from pygeotoolbox.sharedtools import saveStrToFile, fileRead

    workingDir = os.path.dirname(__file__)
    codeFileName = workingDir + "/~temp.txt"
    htmlFileName = workingDir + "/~temp.html"

    saveStrToFile(code, codeFileName)
    args = []
    args.extend(sys.argv)
    args.extend(['-l', lexer,'-o', htmlFileName, codeFileName])

    pygments.cmdline.main(args)
    result = fileRead(htmlFileName)
    result = setParameters(result, {
        '"': "'",
        "\n": "<br>",
        "\t": "&nbsp;&nbsp;&nbsp;&nbsp;"
    })

    os.remove(codeFileName)
    os.remove(htmlFileName)

    if removeFirstDiv:
        result = result[result.find(">")+1:]
        result = result[:result.rfind("</pre>")]
    return result