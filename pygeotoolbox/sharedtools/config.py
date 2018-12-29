#  -*- coding: utf-8 -*-
###########################################################
#                                                         #
# Copyright (c) 2018 Radek Augustýn, licensed under MIT.  #
#                                                         #
###########################################################
__author__ = "radek.augustyn@email.cz"
# @PRODUCTION MODULE

import os, sys
from json import loads
from basepath import basePath
from base import fileRead
from base import searchForFileAtPath
from types import FunctionType
import log


configFileName = ""
profile = {}
valueInfos = {} # dict of ValueInfo, having ValueInfo.key as a dict key
onChangeListeners = {}
thisModule = sys.modules[__name__]


# ###############################################################################
#
# _ValueInfo internal class
#
# ###############################################################################
class _ValueInfo:
    """ Configuration variable storage class  """

    def __init__(self, key, defValue, caption, description, validationProc = None, required=True, inputPattern="", onChange=None):
        """Configuration variable storage class constructor.

        :param String key:Configuration key, used as a unique identifier.
        :param Any defValue:Default value for variable.
        :param String caption:Short name, used as  label for inputs.
        :param String description:Variable full description.

        """
        self.key = key
        self.defValue = defValue
        self.caption = caption
        self.description = description
        self.validationProc = validationProc
        self.required = required
        self.inputPattern = inputPattern
        self.onChange = onChange


    def isValid(self):
        if self.validationProc:
            return self.validationProc()
        else:
            return ""


def setValue(key, value, callOnChange=True):
    """Set value of configuration variable. If it doesn't exist yet, creates one.

    :param String key:Symbolic name of the variable. Use dot convention to make eventual hierarchy.
    :param Any value:Stored value.
    :param callOnChange: if true, on change value listener events are fired.

    >>> setValue("myDatabase.key", 36)
    >>> thisModule.myDatabase.key
    36
    """
    assert isinstance(key, basestring)
    assert isinstance(callOnChange, bool)

    __setValue(key, value)
    if callOnChange:
        if key in valueInfos:
            valueInfo = valueInfos[key]
            if valueInfo.onChange:
                valueInfo.onChange()

        for listener, keys in onChangeListeners.iteritems():
            if keys or key in keys:
                listener()


def __setValue(key, value, parent=thisModule):
    """Set value of configuration variable. If it doesn't exist yet, creates one.

    :param String key:Symbolic name of the variable. Use dot convention to make eventual hierarchy.
    :param Any value:Stored value.
    :param module or DummyClass instance parent:Parent of the variable.
    """
    class DummyClass:pass

    if parent == thisModule:
        profile[key] = value

    if key.find(".") < 0:
        setattr(parent, key, value)
    else:
        keys = key.split(".")
        firstKey = keys[0]
        if hasattr(parent, firstKey):
            valueObject = getattr(parent, firstKey)
        else:
            valueObject = DummyClass()
            setattr(parent, firstKey, valueObject)

        __setValue(".".join(keys[1:]), value, valueObject)


def registerValue(key, defValue, caption, description, validationProc = None, required=True, inputPattern="[a-zA-Z0-9_-]{1,}", onChange=None):
    """

    :param key:
    :param defValue:
    :param caption:
    :param description:
    :param validationProc:
    :param required:
    :param inputPattern:
    :param onChange:
    :return:
    """
    assert isinstance(key, basestring)
    assert isinstance(caption, basestring)
    assert isinstance(description, basestring)
    assert validationProc == None or isinstance(validationProc, FunctionType)
    assert isinstance(required, bool)
    assert isinstance(key, basestring)
    assert isinstance(key, basestring)
    assert onChange == None or isinstance(onChange, FunctionType)

    valueInfos.update({key: _ValueInfo(key, defValue, caption, description, validationProc, required, inputPattern, onChange)})
    if not key in profile:
        setValue(key, defValue, False)

    return key


def registerChangeListener(onChangeListenerProc, keys = None):
    """
    This procedure registers onChangeListenerProc. When any of the keys values is changed, this procedure is fired.

    :param onChangeListenerProc: Procedure to be fired on change.
    :param keys: Keys to be attached on.
    """
    assert isinstance(onChangeListenerProc, FunctionType)
    assert keys == None or isinstance(keys, list)

    if onChangeListenerProc in onChangeListeners:
        onChangeListeners[onChangeListenerProc].extend(keys)
    else:
        onChangeListeners[onChangeListenerProc] = keys


def getDefaultValue(id):
    if id in valueInfos:
        return valueInfos[id].defValue
    else:
        return None


def getValue(id):
    if id in profile:
        return profile[id]
    else:
        return getDefaultValue(id)


def save(saveAll = False):
    from json import dumps
    from base import saveStrToFile

    saveJSON = {}
    for key in profile:
        value = getValue(key)
        if saveAll or value <> getDefaultValue(key):
            saveJSON[key] = value

    saveStrToFile(dumps(saveJSON, indent=4), configFileName)


def basePathChanged():
    global configFileName

    #configFileName = basePath + os.sep + "config.json"
    for path in [os.path.dirname(sys.argv[0]), os.getcwd()]:
        found, configFileName = searchForFileAtPath(path, "config.json")
        if found:
            break;

    if found:
        configPatch = loads(fileRead(configFileName))
        for key, value in configPatch.iteritems():
            setValue(key, value)

    if found:
        log.info("Found configuration at %s." % configFileName)
    else:
        log.info("Created empty configuration in %s." % configFileName)


basePathChanged()

def doPrint():
    print "configFileName:", configFileName
    for key, value in profile.iteritems():
        print key, "\t=", value


# #############################################################################
# NO-PRODUCTION CODE
# #############################################################################
if __name__ == "__main__":
    registerValue("test", False, "test", "Test description")
    doPrint()
    save(True)