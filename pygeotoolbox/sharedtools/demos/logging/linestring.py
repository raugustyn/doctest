#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"


import pygeotoolbox.sharedtools.log as log


def processor(shape):
    log.openSection("processor at <%s>" % str(__file__), level=log.DEBUG)
    log.debug(shape)
    log.closeSection()