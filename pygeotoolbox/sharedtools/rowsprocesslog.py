#  -*- coding: utf-8 -*-
###########################################################
#                                                         #
# Copyright (c) 2018 Radek Augustýn, licensed under MIT.  #
#                                                         #
###########################################################
__author__ = "radek.augustyn@email.cz"
# @PRODUCTION MODULE


import time, sys


__statusInfo = ""
__waitStatusInfoLastTime = None
__printMuted = False


def logPrint(msg=""):
    if not __printMuted:
        print(msg)


def mutePrint():
    global __printMuted

    __printMuted = True


def unMutePrint():
    global __printMuted

    __printMuted = False


def updateStatusInfo(msg):
    global __statusInfo, __waitStatusInfoLastTime

    if __waitStatusInfoLastTime and __statusInfo == msg:
        deltaTime = time.time() - __waitStatusInfoLastTime
        if deltaTime>1:
            msg = "%s (%gs)" % (msg, deltaTime)

    __waitStatusInfoLastTime = time.time()
    __statusInfo = msg


def getStatusInfo():
    return __statusInfo


def printEvery100rows(rowCount):
    if rowCount % 100 == 0:
        logPrint(str(rowCount))


__isConsoleApp = True
_printCount = 0
__lastPrintTime = None
TIME_PRINT_LIMIT = 5


def printEvery100rowsInLongLine(rowCount, printCount = 100, msgTemplate="Zpracováno %d záznamů."):
    import sys
    global _printCount, __lastPrintTime

    if msgTemplate:
        msg = msgTemplate % rowCount
        updateStatusInfo(msg)

    if rowCount % printCount == 0 or not __lastPrintTime or (time.time() - __lastPrintTime) > TIME_PRINT_LIMIT:
        __lastPrintTime = time.time()
        if _printCount == 0:
            pref = ""
        else:
            pref = "..."
        if __isConsoleApp and not __printMuted:
            sys.stdout.write(pref + str(rowCount))

        _printCount = _printCount + 1
        if _printCount == 20:
            _printCount = 0
            print


def printToStdOut(msg = ""):
    if not __printMuted:
        sys.stdout.write(msg)


def printRowCount(rowCount, msg = ""):
    if not msg:
        msg = "Row count="

    sys.stdout.write("\n" + msg + str(rowCount) + "\n")


def printRows(rowCount, flushCount = 1000, msg = ""):
    if rowCount % 100 == 0:
        if msg:
            logPrint(msg)
        else:
            logPrint(str(rowCount))