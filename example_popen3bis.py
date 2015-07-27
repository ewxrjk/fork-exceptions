import os,sys,popen2

class Echild(Exception): pass

print >>sys.stderr, "starting pid is %d" % os.getpid()

# I want to log all the dup2 calls.
dup2=os.dup2
def monkey_dup2(a,b):
    print "dup2 %d -> %d" % (a,b)
    return dup2(a,b)
os.dup2=monkey_dup2

try:
    popen2.Popen3("true").wait()
except Exception as e:
    print >>sys.stderr, "popen3: caught %s (am %d)" % (type(e), os.getpid())
    sys.exit(0)
