#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"


import pygeotoolbox.sharedtools.log as log


def processor(shape):
    import sys
    log.openSection("processor at <%s>" % str(__file__), level=log.DEBUG, profile=sys.modules[__name__])
    log.debug(shape)
    log.closeSection()