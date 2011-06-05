/* Python 'int' type */
/*
requires: __builtin__.TypeError
requires: __builtin__.ZeroDivisionError
requires: __builtin__.float

contains: __builtin__.int
*/

var _int = __inherit(number, "int");

var __py2js_int = _int;

_int.prototype.__init__ = function(i) {
    if (arguments.length == 2) {
        this._obj = parseInt(i, arguments[1]);
    } else {
        this._obj = parseInt(i);
    }
};

_int.prototype._isnumeric_float = false;

_int.prototype.__int__ = function () {
    return this;
};

_int.prototype.__str__ = function () {
    return str.__call__(this._obj);
};

_int.prototype.__repr__ = _int.prototype.__str__;

_int.prototype.__hash__ = function () {
    return this._obj;
};

_int.prototype.__invert__ = function() {
    return _int.__call__(~this._obj);
};

_int.prototype.__div__ = function(x) {
    if (!x._isnumeric_)
        throw py_builtins.TypeError.__call__("Cannot divide int and non-int");
    if (x._obj === 0)
        throw py_builtins.ZeroDivisionError.__call__("integer division or modulo by zero");
    return _float.__call__(this._obj / x._obj);
};

_int.prototype.__floordiv__ = function(x) {
    if (!x._isnumeric_)
        throw py_builtins.TypeError.__call__("Cannot operate on int and non-int");
    if (x._obj === 0)
        throw py_builtins.ZeroDivisionError.__call__("integer division or modulo by zero");
    return _int.__call__(Math.floor(this._obj / x._obj));
};

_int.prototype.__mod__ = function(x) {
    if (!x._isnumeric_)
        throw py_builtins.TypeError.__call__("Cannot find remainder of int and non-int");
    return _int.__call__(this._obj % x._obj);
};

_int.prototype.__pow__ = function(x) {
    if (!x._isnumeric_)
        throw py_builtins.TypeError.__call__("Cannot exponentiate int and non-int");
    return _int.__call__(Math.pow(this._obj, x._obj));
};

_int.prototype.__bitand__ = function(x) {
    if (!x._isnumeric_)
        throw py_builtins.TypeError.__call__("Cannot operate on int and non-int");
    return _int.__call__(this._obj & x._obj);
};

_int.prototype.__bitor__ = function(x) {
    if (!x._isnumeric_)
        throw py_builtins.TypeError.__call__("Cannot operate on int and non-int");
    return _int.__call__(this._obj | x._obj);
};

_int.prototype.__bitxor__ = function(x) {
    if (!x._isnumeric_)
        throw py_builtins.TypeError.__call__("Cannot operate on int and non-int");
    return _int.__call__(this._obj ^ x._obj);
};

_int.prototype.__lshift__ = function(x) {
    if (!x._isnumeric_)
        throw py_builtins.TypeError.__call__("Cannot operate on int and non-int");
    return _int.__call__(this._obj << x._obj);
};

_int.prototype.__rshift__ = function(x) {
    if (!x._isnumeric_)
        throw py_builtins.TypeError.__call__("Cannot operate on int and non-int");
    return _int.__call__(this._obj >> x._obj);
};

_int.prototype.__div__ = function(x) {
    if (!x._isnumeric_)
        throw py_builtins.TypeError.__call__("Cannot exponentiate number and number-int");
    return _float.__call__(this._obj / x._obj);
};

_int.prototype.__idiv__      = _int.prototype.__div__;

_int.prototype.__ilshift__   = _int.prototype.__lshift__;
_int.prototype.__irshift__   = _int.prototype.__rshift__;
_int.prototype.__ibitand__   = _int.prototype.__bitand__;
_int.prototype.__ibitor__    = _int.prototype.__bitor__;
_int.prototype.__ibitxor__   = _int.prototype.__bitxor__;
_int.prototype.__ifloordiv__ = _int.prototype.__floordiv__;

var $c0 = _int.__call__(0);
var $c1 = _int.__call__(1);
var $c2 = _int.__call__(2);
var $c3 = _int.__call__(3);
var $c4 = _int.__call__(4);
var $c5 = _int.__call__(5);
var $c6 = _int.__call__(6);
var $c7 = _int.__call__(7);
var $c8 = _int.__call__(8);
var $c9 = _int.__call__(9);
