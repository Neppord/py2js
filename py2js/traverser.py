INDENT = 0
DEDENT = 1
class Traverser(object):
  def __init__(self, lib, formater):
    self.lib = lib
    self.formater = formater
  def run(self, node):
    stack = [node]
    env = {}
    while stack:
      node = stack.pop()
      if isinstance(node, Token):
        self.lib.write(node)
        self.formater.write(self.lib.read())
      elif node == INDENT:
        self.formater.indent()
      elif node == DEDENT:
        self.formater.dedent()
      elif node.__class__.__name__ == "Module":
        stack.append(Token("ADD_MODULE", module_name="__main__"))
        stack.append(Token("MODULE_END"))
        stack.append(DEDENT)
        stack.extend(node.body[::-1])
        stack.append(INDENT)
        stack.append(Token("MODULE_START", module_name="__main__"))
      else:
        stack.append(Token("DEBUG",string=repr(node)))
  
class Token():
  def __init__(self, name, **k):
    self.name = name
    self.k = k


if __name__ == "__main__":
  import sys
  import ast
  import formater
  import library
  formater = formater.Formater()
  lib = library.LibraryStream()
  traverser = Traverser(lib, formater)
  traverser.run(ast.parse("def helloworld():pass"))
  print formater.read()

