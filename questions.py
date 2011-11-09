import re

class Question(object):
  """Returns a Question object given a dict qa"""

  def __init__(self, qa):
    super(Question, self).__init__()
    self.id   = qa['id']
    self.task = qa['task']
    self.i    = re.compile(eval(qa['input']))
    self.o    = re.compile(eval(qa['output']))
    self.test = qa['test']


class Teacher(object):
  """Manages Question objects."""

  def __init__(self, q_fname):
    qs = self._read_questions(q_fname)
    self.questions = self._gen_questions(qs)
    self.ison = 0

  def q(self, index):
    try:
      return self.questions[index]
    except IndexError:
      return None
  
  def next(self):
    self.ison += 1
    return self.q(self.ison - 1)

  def _read_questions(self, q_fname):
    """Reads a file composed of Tasks with Answers and Hints, and returns a dictionary."""
    read = re.compile(r"""
                      \-\->\s*          # Match an indicator
                      (?P<type>         # Allow access by .group('type')
                      ((T|t)ask\s*\d+)| # Match "Task 12", upper/lower case, or
                      ((I|i)nput)|      # Match "Input", or
                      ((O|o)utput)|     # Match "Output", upper/lower case, or
                      ((T|t)est))       # Match "Test"
                      """, re.VERBOSE)
    file = open(q_fname, 'r', encoding='utf-8')
    questions = []
    matchdict = {}
    status = None

    for line in file:
      linematch = read.search(line)
      if linematch:
        if 'task' in linematch.group('type').lower():
          questions.append(matchdict) if matchdict else None
          matchdict = {'id':linematch.group('type')}
          status = 'task'
        else:
          status = linematch.group('type').lower().split()[0]
      else:
        if status == 'task':
          matchdict[status] = matchdict.get(status, [])
          matchdict[status].append(line.strip()) if line.strip() != '' else None
        elif line.strip() != '\n':
          matchdict[status] = line.strip()

    questions.append(matchdict) if matchdict else None
    file.close()
    return questions

  def _gen_questions(self, qs):
    return [Question(q) for q in qs]
