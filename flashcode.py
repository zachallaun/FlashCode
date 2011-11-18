import sys
import re

class FlashCode(object):
  
  def __init__(self, log_fname, teacher):
    super(FlashCode, self).__init__()
    # Logging attrs
    self.logname = log_fname

    # Teacher/Question attrs
    self.teacher = teacher
    self.current = self.teacher.next()

    # Hooks
    self.changed = False
    self.reset_io()
    self.empty_prompt = re.compile(r".+\(\d+\).+(>>>|\.\.\.)\s*")
    self.full_prompt  = re.compile(r""" .+(\(\d+\))           # group 1, matches '(#)'
                                        .+(>>>|\.\.\.)\s(.+)  # group 2, matches input
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
    if (self.changed and self.current) and self._validated():
      # if self._validated():
      self.current = self.teacher.next()
      if self.current:
        self.sprint('\n'.join(self.current.task))
      else:
        self.sprint("Congrats! You've finished this module.\nPress CTRL-d to choose another when you're ready.") 
  
  def _validated(self):
    validi = True
    valido = True
    if 'i' in self.current.test and self.input:
      validi = True if self.current.i.match(self.input[-1]) else False
    if 'o' in self.current.test and self.output:
      valido = True if self.current.o.match(self.output[-1]) else False
    return validi and valido
  
  # Bugged and shitty
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

        if 0 <= i <= (4 + len(self.teacher.q(0).task)): # Skip banner
          pass
        elif fullmatch:
          self.input.append(fullmatch.group(3))
        elif emptymatch:
          pass
        else:
          self.output.append(line)
    self.changed = True if self.output != oldout else False
