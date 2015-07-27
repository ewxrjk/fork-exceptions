import os,signal,subprocess,sys

parent=os.getpid()

if os.fork()==0:
    while True:
        try: os.kill(parent+2,signal.SIGINT)
        except: pass

try:
    subprocess.call("true")
except KeyboardInterrupt as e:
    print "caught %s (running=%d root=%d)" % (type(e), os.getpid(), parent)
    sys.exit(0)

# But:
#  PyOs_AfterFork calls PyEval_ReInitThreads
#  which calls PyErr_WriteUnraisable if threading._after_fork raises
#  - which in this case, it does.
