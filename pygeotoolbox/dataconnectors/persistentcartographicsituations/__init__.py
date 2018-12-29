import sys

def printEvery100rows(rowCount):
    if rowCount % 100 == 0:
        print rowCount

_printCount = 0
def printEvery100rowsInLongLine(rowCount):
    global _printCount
    if rowCount % 100 == 0:
        if _printCount == 0:
            pref = ""
        else:
            pref = "..."
        sys.stdout.write(pref + str(rowCount))
        _printCount = _printCount + 1
        if _printCount == 10:
            _printCount = 0
            print
