# -*- coding: utf-8 -*-
###########################################################
#                                                         #
# Copyright (c) 2018 Radek Augustýn, licensed under MIT.  #
#                                                         #
###########################################################
__author__ = "radek.augustyn@email.cz"
# @PRODUCTION MODULE


import logging, codecs, os
from logging import INFO, DEBUG, WARNING # No dummy, used for export
from __init__ import updateStatusInfo


# Local state variables
__sharedAdapter = None
__sharedLogger = None
__logFileName = ""
__SHARED_LOG_PATH = "c:/temp"


DEBUG_ENABLED = True
LOGGED_PROFILES = [] # None or empty list means "ALL PROFILES ARE LOGGED"
PROFILE = None

def getAdapter():
    return __sharedAdapter


class MessageContainer():
    SYSTEM_MSG = "System"
    COMMAND_MSG = "Command"

    def __init__(self):
        self.msgs = []
        self.systemEndIndex = None
        self.commandStartIndex = None


    def log(self, msg):
        self.msgs.append(msg)


    def startCommand(self):
        self.commandStartIndex = len(self.msgs)
        if not self.systemEndIndex:
            self.systemEndIndex = len(self.msgs)


    def getMsgs(self, lineHeaders="", bookmark=None):
        if not self.systemEndIndex:
            self.systemEndIndex = 0
        if not self.commandStartIndex:
            self.commandStartIndex = 0

        if lineHeaders:
            systemMsg = MessageContainer.SYSTEM_MSG + " " + lineHeaders
            commandMsg = MessageContainer.COMMAND_MSG + " " + lineHeaders
        else:
            systemMsg = MessageContainer.SYSTEM_MSG
            commandMsg = MessageContainer.COMMAND_MSG

        if not bookmark:
            bookmark = 0
        result = map(lambda x: systemMsg + x, self.msgs[bookmark:self.systemEndIndex]) + map(lambda x: commandMsg + x, self.msgs[self.commandStartIndex:])
        self.startCommand()

        return result


    def getBookmark(self):
        return len(self.msgs)



class CustomAdapter(logging.LoggerAdapter):
    def __init__(self, logger, extra):
        logging.LoggerAdapter.__init__(self, logger, extra)
        self.logIndent = 0
        self.__onLogProc = None
        self.maxLogIndent = None
        self.__muted = False
        self.sectionLevels = []
        self.errors = MessageContainer()
        self.warnings = MessageContainer()


    def startCommand(self):
        self.warnings.startCommand()
        self.errors.startCommand()


    @property
    def muted(self):
        return self.__muted


    def mute(self):
        self.__muted = True


    def unMute(self):
        self.__muted = False


    def process(self, msg, kwargs):
        if LOGGED_PROFILES:
            if PROFILE not in LOGGED_PROFILES:
                if PROFILE <> None:
                    print "profile:" + str(PROFILE)
                return None, {}

        msg = '%s%s' % (self.getIndent(), msg)

        global __onLogProc
        if self.__onLogProc:
            self.__onLogProc(msg)

        return msg, kwargs


    def getIndent(self):
        result = ""
        for i in range(0, self.logIndent):result += "\t"
        return result


    def openSection(self, msg, level = logging.INFO):
        if self.__muted:return

        updateStatusInfo(msg)

        self.log(level, msg)
        self.logIndent = self.logIndent + 1
        while len(self.sectionLevels) <= self.logIndent:
            self.sectionLevels.append(INFO)
        self.sectionLevels[self.logIndent] = level


    def closeSection(self, msg="Done.", level = None, closeEmptySections=False):
        if self.__muted: return

        if level == None:
            level = self.sectionLevels[self.logIndent]

        updateStatusInfo("")
        self.logIndent = self.logIndent - 1
        if self.logIndent < 0:self.logIndent = 0
        self.log(level, msg)


    def getBookmark(self):
        return self.getNumberOfLines()


    def getNumberOfLines(self):
        logFile = codecs.open(getLogFileName(), "r", "utf-8")
        result = 0
        for line in logFile:
            result = result + 1

        return result


    def getLines(self, startRowNumber, endRowNumber, newLineSequence="\n", lineProcessor=None):
        result = ""

        logFileName = getLogFileName()
        if logFileName:
            logFile = codecs.open(getLogFileName(), "r", "utf-8")
            rowNumber = 0
            for line in logFile:
                if rowNumber > startRowNumber and (endRowNumber == None or rowNumber <= endRowNumber):
                    if lineProcessor:
                        line = lineProcessor(line)
                    if newLineSequence <> "\n":
                        line = line.rstrip('\n') + newLineSequence
                    result += line
                rowNumber = rowNumber + 1

        return result


def createLogger(logFileName, level = None):
    global __logFileName
    global __sharedLogger
    global __sharedAdapter
    global logger


    if not __sharedAdapter:
        if logFileName:
            loggerName = logFileName
        else:
            loggerName = "pygeotoolbox_log"
        __sharedLogger = logging.getLogger(loggerName)
        if level:
            __sharedLogger.setLevel(level)
        else:
            __sharedLogger.setLevel(logging.DEBUG)

        msg = "create logger " + loggerName
        logging.basicConfig(format='%(asctime)s - %(levelname)s %(message)s', datefmt="%H:%M:%S")
        __sharedAdapter = CustomAdapter(__sharedLogger, {'connid': __name__})
        logger = __sharedAdapter

        if logFileName:
            from __init__ import basePath
            from base import makeDir

            if os.path.exists(__SHARED_LOG_PATH):
                logFilePath = __SHARED_LOG_PATH
            else:
                logFilePath = basePath
            logFilePath +=  os.sep + "logs" + os.sep

            makeDir(logFilePath)

            __logFileName = logFilePath + logFileName + ".log"
            fileHandler = logging.FileHandler(__logFileName, mode='w')
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            fileHandler.setFormatter(formatter)
            __sharedLogger.addHandler(fileHandler)

            __sharedAdapter.info("Create logger %s." % __logFileName)
            msg += " => " + __logFileName
        logger.info(msg)

    return __sharedAdapter


def loggerNeeded():
    if not __sharedAdapter:
        createLogger("log")


def getLogFileName():
    return __logFileName


def createLoggerForModule(module, level = None):
    from __init__ import relativizePath

    logFileName = relativizePath(module).replace(os.sep, ".").replace(".py", "")

    return createLogger(logFileName, level)


def mute():
    logger.mute()


def unMute():
    logger.unMute()


def getIndent():
    return logger.getIndent()


def setProfile(profile):
    global PROFILE

    PROFILE = profile


def openSection(msg, level=logging.INFO, profile=None):
    setProfile(profile)
    logger.openSection(msg, level)


def info(msg, profile=None):
    setProfile(profile)
    logger.info(msg)


def debug(msg, profile=None):
    if DEBUG_ENABLED:
        setProfile(profile)
        logger.debug(msg)


def warning(msg, profile=None):
    logger.warnings.log(msg)

    setProfile(profile)
    logger.warning(msg)


def error(msg, profile=None):
    logger.errors.log(msg)

    setProfile(profile)
    logger.error(msg)


def startCommand():
    logger.startCommand()

def getErrorLines(lineSeparator="\n", lineHeader="Error: "):
    lines = logger.errors.getMsgs(lineHeader)
    return lineSeparator.join(lines)


def getWarningLines(lineSeparator="\n", lineHeader="Warning: "):
    lines = logger.warnings.getMsgs(lineHeader)
    return lineSeparator.join(lines)


def closeSection(msg="Done.", level=None, profile=None):
    setProfile(profile)
    logger.closeSection(msg, level)


def getNumberOfLines():
    return logger.getNumberOfLines()


def getLines(startRowNumber, endRowNumber, newLineSequence="\n"):
    return logger.getLines(startRowNumber, endRowNumber, newLineSequence)


logger = createLogger("default", DEBUG)
logging.openSection = openSection
logging.closeSection = closeSection


# #############################################################################
# NO-PRODUCTION CODE
# #############################################################################
if __name__ == '__main__':

    # #############################################
    # Not proper use, custom logger direct create
    # #############################################
    logger.openSection("Not proper use, custom logger direct create")
    logger.info("Logger test info")
    logger.debug("Logger test debug")
    logger.error("Logger test error")
    logger.critical("Logger test critical")
    logger.warning("Logger test warning")
    logger.log(INFO, "Logger test log")
    logger.closeSection()

    # #############################################
    # Proper use of shared logging
    # #############################################

    import logging

    # Case A: We do not know shared logger name
    logging.openSection("Case A: We do not know shared logger name")
    logging.info("Logger test info")
    logging.debug("Logger test debug")
    logging.error("Logger test error")
    logging.critical("Logger test critical")
    logging.warning("Logger test warning")
    logging.log(INFO, "Logger test log")
    logging.closeSection()

    # Case B: We do know shared logger name
    logging.openSection("Case B: We do know shared logger name")
    testappLogger = logging.getLogger("testapp")
    testappLogger.info("Logger test info")
    testappLogger.debug("Logger test debug")
    testappLogger.error("Logger test error")
    testappLogger.critical("Logger test critical")
    testappLogger.warning("Logger test warning")
    testappLogger.log(INFO, "Logger test log")
    logging.closeSection()
