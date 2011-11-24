import sys
import re
import code
import os

from src.questions import Teacher
from src.watchman import Watchman
from src.countedconsole import CountedConsole
from src.str_format import *

"""This script handles interpreter setup, cleanup, and continuation."""

###
# Core Functions
###
def engine():
  """Sets up and runs the FC environment."""

  # One-time FC banner
  welcome = "Welcome to FlashCode (FC), the interactive Python learning environment."
  print("{0}\n{1}\n{2}".format('='*len(welcome), cyan(welcome), '='*len(welcome)))

  # Runner loop
  while True:

    # Parse, print, and prompt for module choice
    modules = parse_manifest('data/manifest.txt')
    
    print("\nPlease choose your module by inputting the number below.\n")
    for module in modules:
      print(module[0], end='')
    print()
    
    title, datapath = get_module(modules)

    ### Environment setup
    # Teacher returns a question generator object.
    # Stdout/err/in are set to a Watchman object, which handles logging and hooks.
    # Watchman passes the Teacher internally to a FlashCode object, which
    # handles input and output validation.
    teacher = Teacher(datapath)
    sys.stdout = sys.stderr = sys.stdin = Watchman('flashlog.dat', teacher)

    # FlashCode banner and initial prompt
    first_task = '\n{0} '.format(cyan("(FC)")) + '\n'.join(teacher.q(0).task)
    banner = "{0}\n{1}{2}\n{3}\n".format('='*len(title), cyan(title), '='*len(title), first_task)

    ### Interpreter setup
    # CountedConsole (based on code.InteractiveConsole) creates an imbedded interpreter,
    # which allows the user to enjoy multiple module sessions without restarting
    # the program.
    console = CountedConsole()
    console.interact(banner)

    # Removes the logfile and resets stdout/err/in. Necessary for multiple sessions.
    cleanup()

def cleanup():
  try:
    os.remove('flashlog.dat')
  except OSError:
    pass
  
  # Reset stdout/err/in to original values
  sys.stdout = sys.__stdout__
  sys.stderr = sys.__stderr__
  sys.stdin = sys.__stdin__

def get_module(modules):
  """Prompts the user for a valid module. Allows the user to quit the program."""
  module = None
  while not module:
      choice = input("Module number (or 'q' to quit): ")

      # Validate input as a digit
      if re.match(r"\d+", choice):

        # Validate module existence
        try:
          choice = int(choice)
          module = modules[choice-1]
        except IndexError:
          print("Sorry, that module isn't valid.")
        
      elif 'q' in choice.lower():
        quit()

      else:
        print("Didn't catch that.")
  
  return module

def parse_manifest(fname):
  """Parses a module manifest file and returns a list of lists containing
  the module name at index 0 and the datapath at index 1."""

  # Regex patterns for a module title or a file path
  modulematch = re.compile(r"^\((?P<id>\d+)\)\s(?P<name>.+)")
  filematch   = re.compile(r"^\-\->\s(?P<path>.+)")

  modules = []
  with open(fname, 'r') as f:
    
    for line in f:
      mm = modulematch.match(line)
      fm = filematch.match(line)
      
      if mm:
        modules.append([line])
      elif fm:
        modules[-1].append(fm.group('path'))
    
  return modules

###
# Run
###
if __name__ == '__main__':
  engine()