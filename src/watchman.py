import sys
from src.flashcode import FlashCode

class Watchman(object):
    """
    Watchman sets up logging to an external file and triggers hooks through
    a FlashCode object. Requires a log_filename and a teacher object to be passed.

    Usage:
    sys.stdout = sys.stderr = sys.stdin = Watchman(log_fname, mode)
    """
    
    def __init__(self, log_fname, teacher, mode='w'):
        self.log = open(log_fname, mode)
        self.flash = FlashCode(log_fname, teacher) # implements after_write hook

    def __del__(self):
        self.log.close()

    def write(self, data):
        """Called when data is passed to stdout/err. Writes this data to log and
        original stdout."""
        self.log.write(data)
        self.log.flush()
        sys.__stdout__.write(data)
        sys.__stdout__.flush()
        # Triggers input/output validation hook
        self.flash.after_write()

    def readline(self):
        """Called when input is accepted from stdin"""
        s = sys.__stdin__.readline()
        self.log.write(s)
        self.log.flush()
        return s

    def flush(self):
        # Hack to avoid "Attribute Error: flush() method missing" on exit
        pass
