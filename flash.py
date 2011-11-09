import sys
import re
import code

from questions import Teacher
from watchman import Watchman
from countedconsole import CountedConsole

# Assumes a folder called data/ in current dir
teacher = Teacher('data/flashq.txt')
# Assumes a folder called log/ in current dir
sys.stdout = sys.stderr = sys.stdin = Watchman('log/flashlog.dat', teacher)

# FlashCode banner
welcome = "Welcome to FlashCode (FC), the interactive Python learning environment."
banner  = "{0}\n{1}\n{2}\n".format('='*len(welcome), welcome, '='*len(welcome))

if __name__ == '__main__':
  console = CountedConsole()
  console.interact(banner)