Inspired by http://bugs.debian.org/793471 ...

What happens if you fork a program and in the child, before calling
exec, you raise an exception?  Can the exception 'escape' from the
code that's supposed to be running in the child out into the wider
program (but still running in the child process)?

In Perl the answer is (or at least, was) yes.  I had a poke around in
Python to see if the same is true there.  (I tried Python 2.7.6
because that's what Apple ship.)

To be clear, if you do something like this:

    if os.fork() == 0:
      raise Exception()

...then nobody should be surprised that the exception 'escapes' the
conditional.  That's completely uninteresting.  What is interesting -
or 'interesting' if you're trying to understand it without realizing
what happened - is when this happens unexpectedly, e.g. due to a
poorly-handled error case in a utility function.

1. popen2.py
   This can be subverted if:
     1a. os.dup2 fails - but I can't see how to make that happen.
     1b. os.closerange fails
     1c. testing capturestderr fails (for the Popen3 version only)

   example_popen3.py is a somewhat contrived example of 1c.

   You could monkey-patch os.dup2 or os.closerange.  For example,
   maybe you want to log all the dup2 calls (and maybe other stuff
   that is not relevant here) ... and then the disk fills up.  For
   instance example_popen3bis.py:

     $ python2.7 -u example_popen3bis.py > /dev/full
     starting pid is 9800
     popen3: caught <type 'exceptions.IOError'> (am 9801)

2. subprocess.py:

   try: ... except: follows os.fork.  You'd have to introduce an
   exception between them.

   KeyboardInterrupt seems promising but this isn't particularly easy
   in practice: PyOs_AfterFork calls PyEval_ReInitThreads; this calls
   threading._after_fork and if that raises then it calls
   PyErr_WriteUnraisable and swallows the exception. So you'd have to
   time the SIGINT to be after this has all happened but before the
   try: runs.

   In short I've not managed to cause mischief here yet.

3. pty.py:

   If os.forkpty does not exist then os.setsid throwing would do the
   job, and setsid() blows up in various well-documented conditions.
   However, os.forkpty does exist on my platforms so this isn't very
   easy for me to test.

4. multiprocessing/forking.py and process.py

   Can be subverted if:
     4a. random.seed fails (needs os.urandom to fail)
     4b. sys.stdout.flush fails (or stderr...)
     4c. an error occurs and sys.stderr.write fails
     4d. probably other stuff

   I think you could probably do something with a full disk.
