import code
import sys
import re


class FlashCode(object):
  
  def __init__(self, log_fname):
    super(FlashCode, self).__init__()
    self.logname = log_fname
    self.changed = False
    self.reset_io()
    self.empty_prompt = re.compile(r".+\(\d+\).+(>>>|\.\.\.)\s*")
    self.full_prompt  = re.compile(r""" .+(\(\d+\))           # group 1, matches '(#)'
                                        .+((>>>|\.\.\.)\s.+)  # group 2, matches prompt and input
                                    """, re.X)
  
  def reset_io(self):
    self.input = []
    self.output = []

  def sprint(self, data):
    """Safe print. Prints directly to sys.__stdout__, bypassing Watchman."""
    string = "\n\n{0}(FC){1} {2}\n".format('\033[96m', '\033[0m', str(data))
    sys.__stdout__.write(string)
  
  def after_write(self):
    self._parse_log()
    if self.changed:
      pass
      # How I think I want to impliment this: the class has an attribute
      # self.currentq, which is a question object. Every time self.changed is True,
      # I attempt to match self.currentq.in to _last_input_block() and self.currentq.out
      # to self.output[-1]. If they match, the question has completed, and I call something
      # like self.nextquestion(), which gets the next currentq and prints the task.
  
  def _last_input_block(self):
    """Returns the last block of input submitted. An interpreter code block
    begins with a '>>>' prompt followed by 0 or more '...' prompts."""
    prompt = re.compile(r"\(\d+\)(>>>|...)\s.+")
    block = []

    if self.input:
      xinput = list(self.input)
      for i in range(len(xinput)-1, -1, -1):
        match = prompt.match(xinput[i])
        if match:
          if match.group(1) == '>>>':
            block.insert(0, xinput[i])
            return block
          elif match.group(1) == '...':
            block.insert(0, xinput.pop(i))
    return block

  def _parse_log(self):
    oldout = list(self.output)
    self.reset_io()
    
    with open(self.logname, 'r') as log:
      for i, line in enumerate(log.readlines()):
        line = line.strip()
        fullmatch = self.full_prompt.match(line)
        emptymatch = self.empty_prompt.match(line)

        if 0 <= i <= 3: # Skip banner
          pass
        elif fullmatch:
          # Append in the format '(1)>>> input' to keep internal
          # representation of input clean
          self.input.append(fullmatch.group(1)+fullmatch.group(2))
        elif emptymatch:
          pass
        else:
          self.output.append(line)
    self.changed = True if self.output != oldout else False


class Watchman(object):
  """
  Watchman sets up full logging to an external file and triggers
  post-input hooks.

  Usage:
  sys.stdout = sys.stderr = sys.stdin = Watchman(log_fname, mode)
  """
  
  def __init__(self, log_fname, mode='w'):
    self.log      = open(log_fname, mode)
    self.lname    = log_fname
    self.flash    = FlashCode(log_fname) # implements after_write hook

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

sys.stdout = sys.stderr = sys.stdin = Watchman('flashlog.dat')


class CountedConsole(code.InteractiveConsole):
  """Used in the exact same way as code.InteractiveConsole.
  The self.raw_input() method has been redefined to stylize the prompt
  and count lines."""
  
  def __init__(self):
    code.InteractiveConsole.__init__(self)
    self.linecount = 0
  
  def raw_input(self, prompt=''):
    self.linecount += 1
    color = "\033[92m" if ">" in prompt else "\033[93m"  # Green if ">>>", yellow if "..."
    pre = "{0}({1})\033[0m".format(color, str(self.linecount))
    return input(pre + prompt)

welcome = "Welcome to FlashCode (FC), the interactive Python learning environment."
banner  = "{0}\n{1}\n{2}\n".format('='*len(welcome), welcome, '='*len(welcome))
console = CountedConsole()
console.interact(banner)