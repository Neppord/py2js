class Traverser(object):
  def run(self, ast, stream):
    stack = [ast]
    env = {}
    while stack:
      node = ast.pop()
      if isinstance(node, Token):
        stream.read(node)
      elif node.name == "Moduel":
        stack.append(Token("ADD_MODULE", module_name="__main__"))
        stack.append(Token("MODULE_END", module_name="__main__"))
        stack.extend(module.body[::-1])
        stack.append(Token("MODULE_START"))
      else:
        stack.append(Token("DEBUG",string=repr(node)))

class Forwarder(object):

  def __init__(self, *streams):
    self.streams = streams

  def write(self, *a, **k):
    self.streams[0].write(*a, **k)

  def read(self, *a, **k):
    for stream1, stream2 in zip(self.streams, self.streams[1:]):
      stream2.write(self.stream1.read(*a, **K))
    return self.streams[-1].read(*a, **k)
  
class Token():
  def __init__(self, name, **k):
    self.name = name
    self.k = k
