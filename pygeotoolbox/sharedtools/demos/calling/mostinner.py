#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"


def caller_name():
    import inspect

    frame=inspect.currentframe()
    frame=frame.f_back.f_back
    code=frame.f_code
    return code.co_filename

def info(msg):
    caller = caller_name()
    print '[%s] %s' % (caller, msg)