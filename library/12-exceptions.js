/* Python built-in exceptions */

var Exception = __inherit(object, "Exception");

Exception.prototype.__init__ = function() {
    if (arguments.length > 0) {
        this.message = arguments[0];
    } else {
        this.message = "";
    }
}

Exception.prototype.__str__ = function() {
    return str.__call__(this.message);
};

Exception.prototype.toString = function() {
    return js(this.__str__());
};
/*
contains: __builtin__.NotImplementedError
contains: __builtin__.ZeroDivisionError
contains: __builtin__.AssertionError
contains: __builtin__.AttributeError
contains: __builtin__.TypeError
contains: __builtin__.ValueError
contains: __builtin__.NameError
contains: __builtin__.IndexError
contains: __builtin__.KeyError
contains: __builtin__.StopIteration
*/
py_builtins.__exceptions__ = [
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
    'StopIteration'
];

for (var i in py_builtins.__exceptions__) {
    var name = py_builtins.__exceptions__[i];
    py_builtins[name] = __inherit(Exception, name);
};
