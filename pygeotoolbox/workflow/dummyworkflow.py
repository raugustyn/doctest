#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"

from workflow import WorkflowItem, WorkflowSequence

from pygeotoolbox.sharedtools.log import logger

def dummyExecute01():
    logger.openSection("dummyExecute01")
    logger.info("Parsing files")
    logger.info("Building indexes")
    logger.closeSection()


def dummyExecute02():
    logger.openSection("dummyExecute02")
    logger.info("Opening table")
    logger.info("Updating table")
    logger.info("Closing table")
    logger.closeSection()

def getWorkflows():
    return WorkflowSequence("Dummy", "", [
        WorkflowItem("Dummy01", "", dummyExecute01, True, True),
        WorkflowItem("Dummy02", "", dummyExecute02, True, True)
    ], True, True)