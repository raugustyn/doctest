_logFileName = None

def logErr(msg):
    import os, codecs
    if _logFileName:
        if os.path.exists():
            mode = "a"
        else:
            mode = "w"
        codecs.open(_logFileName, mode, "utf-8").write(msg)