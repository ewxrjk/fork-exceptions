import os,sys,popen2

class Echild(Exception): pass

try:
    if os.fork() == 0: raise Echild()
except Exception as e:
    print >>sys.stderr, "os.fork: caught %s (am %d)" % (type(e), os.getpid())
    sys.exit(0)
os.wait()

# Yields:
# os.fork: caught <class '__main__.Echild'> (am 12592)
