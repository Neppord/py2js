import collections

class LibraryStream(object):
  def __init__(self):
    self.__buffer = collections.deque()

  def write(self, token):
    self.__buffer.append(lookup(token.name)%token.k)

  def read(self):
    return self.__buffer.popleft()

def lookup(node):
	return _lib[node]

_lib={
      "ADD_MODULE":"$sysmodules = [%(module_name)s]",
      "MODULE_START":"var %(module_name)s = {",
      "MODULE_END":"}",
      "DEBUG":"/*COMPILER_DEBUG:%(string)s*/",
			"PYTHON_ATTRIBUTE":"%(object)s.__getattr__(%(attribute)s)",
		}
