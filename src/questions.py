import re

class Question(object):
  """Returns a Question object given a dictionary containing valid keys"""

  def __init__(self, qa):
    super(Question, self).__init__()
    self.id   = qa['id']
    self.task = qa['task']
    self.i    = re.compile(eval(qa['input']))
    self.o    = re.compile(eval(qa['output']))
    self.test = qa['test']


class Teacher(object):
  """Accepts a question_filename, parses the file, and returns a Teacher, which
  acts similarly to a generator object, returning questions through calls to .next()"""

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

    questions = []
    matchdict = {}
    key = None

    file = open(q_fname, 'r', encoding='utf-8')

    for line in file:

      # If the read pattern matches, linematch will have a group('type')
      # that dicates the current element of the question
      linematch = read.search(line)

      if linematch:

        # If the type is 'task', we've accessed a new question
        if 'task' in linematch.group('type').lower():

          # Indicate that we're about to receive the task
          key = 'task'

          # Append to our questions list the previous question dict,
          # if it exists, and instantiate a new one
          questions.append(matchdict) if matchdict else None
          matchdict = {'id':linematch.group('type')}
        
        # The type is something other than 'task', so indicate
        # the part of the question we're about to access
        else:
          key = linematch.group('type').lower()
      
      else:
        if key == 'task':

          # 'task' lines are stored in a list
          matchdict[key] = matchdict.get(key, [])
          matchdict[key].append(line.strip()) if line.strip() != '' else None
        
        # key is something other than 'task', and the line is not empty or 
        # a comment (begins with #). Value will be a single-line string.
        elif not re.match(r"\n|^#.*", line):
          matchdict[key] = line.strip()
    
    # Reached end of file, append final question dict
    questions.append(matchdict) if matchdict else None
    file.close()

    return questions

