import re

class Question(object):
  """Returns a Question object given a dictionary containing valid keys"""

  def __init__(self, qa):
    super(Question, self).__init__()
    self.id = qa['id']
    self.task = qa['task']
    self.test = qa['test']
    self.i = re.compile(eval(qa['input'])) if 'input' in qa else None
    self.o = re.compile(eval(qa['output'])) if 'output' in qa else None


class Teacher(object):
  """
  Accepts a question_filename, parses the file, and returns a Teacher, which
  acts similarly to a generator object, returning questions through calls to Teacher.next()
  """

  def __init__(self, q_fname):
    self.questions = [Question(q) for q in self._read_questions(q_fname)]
    self.is_on = 0
  
  ###
  # Core Methods
  ###
  def q(self, index):
    """Return a question by index"""
    try:
      return self.questions[index]
    except IndexError:
      return None
  
  def next(self):
    """Return current question and increment location (is_on)"""
    self.is_on += 1
    return self.q(self.is_on - 1)
  
  ###
  # Private Methods
  ###
  def _read_questions(self, q_fname):
    """Reads a question module composed of tasks, input and output
    validation, and testing considerations. Returns a list of dictionaries."""

    read = re.compile(r"""
                      \-\->\s*          # Match an indicator
                      (?P<type>         # Allow access by .group('type')
                      ((T|t)ask\s*\d+)| # Match "Task 12", upper/lower case, or
                      ((I|i)nput)|      # Match "Input", or
                      ((O|o)utput)|     # Match "Output", upper/lower case, or
                      ((T|t)est))       # Match "Test"
                      """, re.VERBOSE)
    
    # igNore, Question, Input, Output read states
    N, Q, I, O = range(4)
    Questions = []
    
    try:
      with open(q_fname) as file:
        state = N
        qdict = {}
        for line in file:
          line = line.strip()
          tag = self._get_tag(line, read)

          if state == N:
            if tag == "Q":
              Questions.append(qdict) if qdict else None
              qdict = {'id': line.split()[-1]}
              question = []
              state = Q
            elif tag == "I":
              state = I
            elif tag == "O":
              state = O

          elif state == Q:
            if tag == "N":
              question.append(line)
            elif tag == "I":
              qdict['task'] = question
              state = I
            elif tag == "O":
              qdict['task'] = question
              state = O
            elif tag == "Q":
              question = []
          
          elif state == I:
            if tag == "N":
              qdict['input'] = line
              qdict['test'] = qdict.get('test', '') + 'i'
              state = N
            elif tag == "O":
              state = O
          
          else: # state is O
            if tag == "N":
              qdict['output'] = line
              qdict['test'] = qdict.get('test', '') + 'o'
              state = N
            elif tag == I:
              state = I
      
      Questions.append(qdict) # Append final dict
      
    except IOError:
      print("No such file as '{0}'.".format(q_fname))
    return Questions
  
  def _get_tag(self, line, regex):
    linematch = regex.match(line)
    if line.startswith('#'):
      tag = "C"
    elif linematch:
      type = linematch.group('type').lower()
      if 'task' in type:
        tag = "Q"
      elif 'input' in type:
        tag = "I"
      elif 'output' in type:
        tag = "O"
    else:
      tag = "N"
    return tag


if __name__ == '__main__':
  teach = Teacher('data/begtut.txt')
  q = teach.next()
  print(q.id, q.task, q.i, q.o, q.test)