import ast
INDENT = 1
DEDENT = -1
class Traverser(ast.NodeTransformer):

  def visit_Module(self, node):
    return [
        ("CREATE_MODULE", dict(module_name="__main__")),
        ("ADD_MODULE", dict(module_name="__main__")),
        ("MODULE_START", dict(module_name="__main__")),
        INDENT,
        ]+[x for x in (self.visit(stmt) for stmt in node.body) if x != None]+[
        DEDENT,
        ("MODULE_END",),
        ]

  def visit_FunctionDef(self, node):
   return [
        ("FUNCTION_DEFENITION_HEAD_START", dict(function_name=node.name)),
        self.visit(node.args),
        ("FUNCTION_DEFENITION_HEAD_END",),
        INDENT,
        ]+[stmt for stmt in (self.visit(stmt) for stmt in node.body) if stmt != None]+[
        DEDENT,
        ("FUNCTION_DEFENITION_END",),
        ]+[decerator for decorator in (self.visit(decorator) for decorator in node.decorator_list) if decerator != None]

  def generic_visit(self, node):
    return ("DEBUG", dict(string=ast.dump(node)))
      
def debug(node):
  import ast
  return [Token("DEBUG",string=ast.dump(node))]
  
class Token():
  def __init__(self, name, **k):
    self.name = name
    self.k = k


if __name__ == "__main__":
  import sys
  import ast
  import formater
  import library
  traverser = Traverser()
  node = ast.parse("def helloworld():pass")
  print traverser.visit(node)

