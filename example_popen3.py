import os,sys,popen2

class Echild(Exception): pass

class ExplodingBoolean(object):
    def __init__(self, value=True):
        self.cling=os.getpid()
        self.value=value
    def __nonzero__(self):
        if os.getpid()!=self.cling: raise Echild()
        return self.value

try:
    popen2.Popen3("true", ExplodingBoolean(value=False)).wait()
except Exception as e:
    print >>sys.stderr, "popen3: caught %s (am %d)" % (type(e), os.getpid())
    sys.exit(0)
