import sys
import re
import code

from questions import Teacher
from watchman import Watchman
from countedconsole import CountedConsole

# Assumes a folder called data/ in current dir
teacher = Teacher('data/flashq.txt')
# Assumes a folder called log/ in current dir
sys.stdout = sys.stderr = sys.stdin = Watchman('flashlog.dat', teacher)

# FlashCode banner and initial prompt
welcome = "Welcome to FlashCode (FC), the interactive Python learning environment."
first_q = teacher.q(0)
first_task = '\n{0}(FC){1} '.format('\033[96m', '\033[0m') + '\n'.join(first_q.task)
banner  = "{0}\n{1}\n{2}\n{3}\n".format('='*len(welcome), welcome, '='*len(welcome), first_task)

if __name__ == '__main__':
  console = CountedConsole()
  console.interact(banner)