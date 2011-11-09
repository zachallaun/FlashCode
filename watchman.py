import sys
from flashcode import FlashCode

class Watchman(object):
  """
  Watchman sets up full logging to an external file and triggers
  post-input hooks.

  Usage:
  sys.stdout = sys.stderr = sys.stdin = Watchman(log_fname, mode)
  """
  
  def __init__(self, log_fname, teacher, mode='w'):
    self.log      = open(log_fname, mode)
    self.lname    = log_fname
    self.flash    = FlashCode(log_fname, teacher) # implements after_write hook

  def __del__(self):
    # Restore sin, so, se
    sys.stdout  = sys.__stdout__
    sys.stdin   = sys.__stdin__
    sys.stderr  = sys.__stderr__
    self.log.close()

  def write(self, data):
    # Called when an object is printed to screen.
    self.log.write(data)
    self.log.flush()
    sys.__stdout__.write(data)
    sys.__stdout__.flush()
    self.flash.after_write()

  def readline(self):
    # Called when input is accepted.
    s = sys.__stdin__.readline()
    self.log.write(s)
    self.log.flush()
    return s

  def flush(self):
    # Hack to avoid "Attribute Error: flush() method missing" on exit
    pass
