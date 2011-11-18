import sys
import re
import code

from fc.questions import Teacher
from fc.watchman import Watchman
from fc.countedconsole import CountedConsole

def start():
  welcome = "Welcome to FlashCode (FC), the interactive Python learning environment."
  print("{0}\n{1}\n{2}\n".format('='*len(welcome), cyan(welcome), '='*len(welcome)))
  
  while True:
    print("Please choose your module by inputting the number below.\n")
    modules = parse_manifest('data/manifest.txt')

    for module in modules:
      print(module[0], end='')
    print()

    title, datapath = get_module(modules)

    teacher = Teacher(datapath)
    sys.stdout = sys.stderr = sys.stdin = Watchman('flashlog.dat', teacher)

    # FlashCode banner and initial prompt
    first_q     = teacher.q(0)
    first_task  = '\n{0} '.format(cyan("(FC)")) + '\n'.join(first_q.task)
    banner      = "{0}\n{1}{2}\n{3}\n".format('='*len(title), cyan(title), '='*len(title), first_task)

    console = CountedConsole()
    console.interact(banner)

def get_module(modules):
  module = None
  while not module:
      choice = input("Module number (or 'q' to quit): ")
      if re.match(r"\d+", choice):
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
  modulematch = re.compile(r"^\((?P<id>\d+)\)\s(?P<name>.+)")
  filematch   = re.compile(r"^\-\->\s(?P<path>.+)")
  modules = []
  with open(fname, 'r') as f:
    for line in f:
      if re.match(r"^#.*", line):
        pass
      mm = modulematch.match(line)
      fm = filematch.match(line)
      if mm:
        modules.append([line])
      elif fm:
        modules[-1].append(fm.group('path'))
  return modules

def cyan(string):
  return '\033[96m' + string + '\033[0m'

if __name__ == '__main__':
  start()
  # parse_manifest('data/manifest.txt')