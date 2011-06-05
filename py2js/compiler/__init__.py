import ast
import inspect

class JSError(Exception):
    pass

class BaseCompiler(object):

    name_map = {
        'self'  : 'this',
        'int'   : '_int',
        'float' : '_float',
        'super' : '__super',
        'py_builtins' : '__py_builtins'
    }

    builtin = set([
        'NotImplementedError',
        'ZeroDivisionError',
        'AssertionError',
        'AttributeError',
        'RuntimeError',
        'ImportError',
        'TypeError',
        'ValueError',
        'NameError',
        'IndexError',
        'KeyError',
        'StopIteration',

        '_int',
        '_float',
        'max',
        'min',
        'sum',
        'filter',
        'reduce'
    ])

    def __init__(self):
        # Required field for the linker

        self.index_var = 0
        
        # This is the name of the classes that we are currently in:
        self._class_name = []

        # This lists all variables in the local scope:
        self._scope = []
        self._classes = {}
        self._exceptions = []
    
    def get_requires(self):
        raise NotImplementedError()

    def add_requires(self, req):
        raise NotImplementedError()

    def alloc_var(self):
        self.index_var += 1
        return "$v%d" % self.index_var

    def visit(self, node):
        try:
            visitor = getattr(self, 'visit_' + self.name(node))
        except AttributeError:
            raise JSError("syntax not supported (%s: %s)" % (node.__class__.__name__, node))

        return visitor(node)

    @staticmethod
    def indent(stmts):
        return [ "    " + stmt for stmt in stmts ]

    ## Shared code

    @staticmethod
    def name(node):
        return node.__class__.__name__

    ## Shared visit functions

    def visit_AssignSimple(self, target, value):
        raise NotImplementedError()

    def visit_Assign(self, node):
        if len(node.targets) > 1:
            tmp = self.alloc_var()
            q = ["var %s = %s" % (tmp, self.visit(node.value))]
            for t in node.targets:
                q.extend(self.visit_AssignSimple(t, tmp))
            return q
        else:
            return self.visit_AssignSimple(node.targets[0], self.visit(node.value))

    def _visit_Exec(self, node):
        pass

    def visit_Print(self, node):
        assert node.dest is None
        assert node.nl
        values = [self.visit(v) for v in node.values]
        values = ", ".join(values)
        self.add_requires("$print$")
        return ["py_builtins.print(%s);" % values]

    def visit_Module(self, node):
        module = []

        for stmt in node.body:
            module.extend(self.visit(stmt))

        return module

    def visit_Assert(self, node):
        test = self.visit(node.test)

        if node.msg is not None:
            return ["assert(%s, %s);" % (test, self.visit(node.msg))]
        else:
            return ["assert(%s);" % test]

    def visit_Return(self, node):
        if node.value is not None:
            return ["return %s;" % self.visit(node.value)]
        else:
            return ["return;"]

    def visit_Expr(self, node):
        return [self.visit(node.value) + ";"]

    def visit_Pass(self, node):
        return ["/* pass */"]

    def visit_Break(self, node):
        return ["break;"]

    def visit_Continue(self, node):
        return ["continue;"]

    def visit_arguments(self, node):
        return ", ".join([self.visit(arg) for arg in node.args])
