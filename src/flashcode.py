import sys
import re
from src.str_format import *

class FlashCode(object):
  """
  Handles interactive tutorial/module through hooks passed from a Watchman and
  from input/output validation. 

  Requires a log_filename (updated by a Watchman) for validation.
  Requires a Teacher to handle question generation.
  """

  def __init__(self, log_fname, teacher):
    super(FlashCode, self).__init__()
    # Logging
    self.logname = log_fname
    self.reset_io()
    # Teacher/Question
    self.teacher = teacher
    self.current = self.teacher.next()
    # Hook validation
    self.changed = False
    self.empty_prompt = re.compile(r".+\(\d+\).+(>>>|\.\.\.)\s*$")
    self.full_prompt  = re.compile(r""" .+(\(\d+\))           # group 1, matches '(#)'
                                        .+(>>>|\.\.\.)\s(.+)  # group 2, matches input
                                    """, re.X)
  
  def reset_io(self):
    self.input = []
    self.output = []
  
  ###
  # Core Methods
  ###
  def sprint(self, data):
    """Safe print. Prints directly to sys.__stdout__, bypassing Watchman logging."""
    string = "\n\n{0} {1}\n".format(cyan("(FC)"), str(data))
    sys.__stdout__.write(string)
  
  def after_write(self, err=False):
    """Primary hook. Called after a write to stdout/err."""
    # Update object's list of input and output
    self._parse_log()
    # Validate hook call through input/output
    if (self.changed and self.current) and self._validated():
      self.current = self.teacher.next()
      # Print next task, or if module is complete, inform user
      if self.current:
        self.sprint('\n'.join(self.current.task))
      else:
        self.sprint("Congratulations! You've finished this module.\nPress CTRL-d to choose another when you're ready.") 
      if err:
        sys.__stdout__.write('\n')
  
  ###
  # Private Methods
  ###
  def _validated(self):
    """Primary validation through current question's i/o regex patterns."""
    # Assume both are true, as both input and output may not be tested
    validi = True
    valido = True
    # Only test input and output if declared in current question (self.current.test)
    if 'i' in self.current.test and self.input:
      validi = True if self.current.i.match(self.input[-1]) else False
    if 'o' in self.current.test and self.output:
      valido = True if self.current.o.match(self.output[-1]) else False
    # The hook call is only valid if both input and output are valid
    return validi and valido
  
  def _parse_log(self):
    """Parse and read in log. Store input and output in attributes. Set self.changed
    if output has changed by updating."""
    # Store old output and reset
    oldout = list(self.output)
    self.reset_io()
    
    with open(self.logname, 'r') as log:

      for i, line in enumerate(log.readlines()):
        line = line.strip()
        # Full_prompt indicates user input. The log will be updated on
        # a fresh prompt as well, so we have to check for it.
        fullmatch = self.full_prompt.match(line)
        emptymatch = self.empty_prompt.match(line)
        # Skip banner and initial task prompt (both are logged)
        if 0 <= i <= (4 + len(self.teacher.q(0).task)):
          pass
        # Only store if user input is present
        elif fullmatch:
          self.input.append(fullmatch.group(3))
        elif emptymatch:
          pass
        # If there's no prompt match, it must be output
        else:
          self.output.append(line)

    # Validate change
    self.changed = True if self.output != oldout else False

  # Currently unused. Could be useful for multi-line validations.
  def _last_input_block(self):
    """Returns the last block of input submitted. An interpreter code block
    begins with a '>>>' prompt followed by 0 or more '...' prompts."""

    block = []

    if self.input:
      # We want a reversed list of input, so that we're seeing the most recent first
      xinput = list(reversed(self.input))
      for line in xinput:
        # Ignore empty prompts
        if self.full_prompt.match(line):
          # '...' in the prompt means it's part of the block.
          # Return the first '>>>' found.
          if '...' in line:
            block.insert(0, line)
          elif '>>>' in line:
            block.insert(0, line)
            break
    
    return block
