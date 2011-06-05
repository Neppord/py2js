/* Python 'str' type */
/*
requires: $defined$
requires: $function$
requires: $class$
requires: $js$
requires: $vsprintf$

requires: __builtin__.int
requires: __builtin__.iter
requires: __builtin__.tuple
requires: __builtin__.bool
requires: __builtin__.isinstance
requires: __builtin__.IndexError
requires: __builtin__.TypeError
requires: __builtin__.ValueError
requires: __builtin__.list
requires: __builtin__.slice

contains: __builtin__.str
*/

var str = __inherit(object, "str");

var __py2js_str = str;

str.prototype.__init__ = function(s) {
    if (!defined(s)) {
        this._obj = '';
    } else {
        if (typeof(s) === "string") {
            this._obj = s;
        } else if (defined(s.__str__)) {
            this._obj = js(s.__str__());
        } else if (defined(s.toString)) {
            this._obj = s.toString();
        } else
            this._obj = js(s);
    }
};

str.prototype.__str__ = function () {
    return this;
};

str.prototype.__repr__ = function () {
    return "'" + this + "'";
};

str.prototype._js_ = function () {
    return this._obj;
};

str.prototype.__hash__ = function () {
    var value = 0x345678;
    var length = this.__len__();

    for (var index in this._obj) {
        value = ((1000003*value) & 0xFFFFFFFF) ^ this._obj[index];
        value = value ^ length;
    }

    if (value == -1) {
        value = -2;
    }

    return value;
};

str.prototype.__len__ = function() {
    return _int.__call__(this._obj.length);
};

str.prototype.__iter__ = function() {
    return iter.__call__(this._obj);
};

str.prototype.__mod__ = function() {
    return str.__call__(sprintf.apply(null, Array.prototype.concat([this._obj], arguments)));
};

str.prototype.__bool__ = function() {
    return py_builtins.bool(this._obj);
};

str.prototype.__eq__ = function(s) {
    if (typeof(s) === "string")
        return bool.__call__(this._obj == s);
    else if (isinstance.__call__(s, str))
        return bool.__call__(this._obj == s._obj);
    else
        return False;
};

str.prototype.__gt__ = function(s) {
    if (typeof(s) === "string")
        return bool.__call__(this._obj > s);
    else if (isinstance.__call__(s, str))
        return bool.__call__(this._obj > s._obj);
    else
        return False;
};

str.prototype.__lt__ = function(s) {
    if (typeof(s) === "string")
        return bool.__call__(this._obj < s);
    else if (isinstance.__call__(s, str))
        return bool.__call__(this._obj < s._obj);
    else
        return False;
};

str.prototype.__contains__ = function(item) {
    for (var index in this._obj) {
        if (item == this._obj[index]) {
            return True;
        }
    }

    return False;
};

str.prototype.__getitem__ = function(index) {
    var seq;
    if (isinstance.__call__(index, slice)) {
        var s = index;
        var inds = js(s.indices(len(this)));
        var start = inds[0];
        var stop = inds[1];
        var step = inds[2];
        seq = "";
        for (var i = start; i < stop; i += step) {
            seq = seq + js(this.__getitem__(i));
        }
        return this.__class__.__call__(seq);
    } else if ((index >= 0) && (index < js(len(this))))
        return this._obj[index];
    else if ((index < 0) && (index >= -js(len(this))))
        return this._obj[index+js(len(this))];
    else
        throw py_builtins.IndexError.__call__("string index out of range");
};

str.prototype.__setitem__ = function(index, value) {
    throw py_builtins.TypeError.__call__("'str' object doesn't support item assignment");
};

str.prototype.__delitem__ = function(index) {
    throw py_builtins.TypeError.__call__("'str' object doesn't support item deletion");
};

str.prototype.__add__ = function(c) {
    return str.__call__(this._obj + c._obj);
};

str.prototype.__iadd__ = str.prototype.__add__;

str.prototype.count = Function(function(str, start, end) {
    if (!defined(start))
        start = 0;
    if (!defined(end))
        end = null;
    var count = 0;
    var s = this.__getitem__(slice.__call__(start, end));
    var idx = s.find(str);
    while (idx != -1) {
        count += 1;
        s = s.__getitem__(slice.__call__(idx+1, null));
        idx = s.find(str);
    }
    return count;
});

str.prototype.index = Function(function(value, start, end) {
    if (!defined(start)) {
        start = 0;
    }

    for (var i = start; !defined(end) || (start < end); i++) {
        var _value = this._obj[i];

        if (!defined(_value)) {
            break;
        }

        if (_value == value) {
            return i;
        }
    }

    throw py_builtins.ValueError.__call__("substring not found");
});

str.prototype.find = Function(function(s) {
    return this._obj.search(s);
});

str.prototype.rfind = Function(function(s) {
    rev = function(s) {
        var a = list.__call__(__py2js_str.__call__(s));
        a.reverse();
        a = __py2js_str.__call__("").join(a);
        return a;
    }
    var a = rev(this);
    var b = rev(s);
    var r = a.find(b);
    if (r == -1)
        return r;
    return len(this)-len(b)-r
});

str.prototype.join = Function(function(s) {
    return __py2js_str.__call__(js(s).join(js(this)));
});

str.prototype.replace = Function(function(old, _new, count) {
    old = js(old);
    _new = js(_new);
    var old_s;
    var new_s;

    if (defined(count))
        count = js(count);
    else
        count = -1;
    old_s = "";
    new_s = this._obj;
    while ((count != 0) && (new_s != old_s)) {
        old_s = new_s;
        new_s = new_s.replace(old, _new);
        count -= 1;
    }
    return __py2js_str.__call__(new_s);
});

str.prototype.lstrip = Function(function(chars) {
    if (js(len(this)) == 0)
        return this;
    if (defined(chars))
        chars = tuple.__call__(chars);
    else
        chars = tuple.__call__(["\n", "\t", " "]);
    var i = 0;
    while ((i < js(len(this))) && (js(chars.__contains__(this.__getitem__(i))))) {
        i += 1;
    }
    return this.__getitem__(slice.__call__(i, null));
});

str.prototype.rstrip = Function(function(chars) {
    if (len(this) == 0)
        return this;
    if (defined(chars))
        chars = tuple.__call__(chars);
    else
        chars = tuple.__call__(["\n", "\t", " "]);
    var i = js(len(this))-1;
    while ((i >= 0) && (js(chars.__contains__(this.__getitem__(i))))) {
        i -= 1;
    }
    return this.__getitem__(slice.__call__(i+1));
});

str.prototype.strip = Function(function(chars) {
    return this.lstrip(chars).rstrip(chars);
});

str.prototype.split = Function(function(sep) {
    if (defined(sep)) {
        var r = list.__call__(this._obj.split(sep));
        var r_new = list.__call__([]);
        iterate(iter.__call__(r), function(item) {
                r_new.append(str.__call__(item));
        });
        return r_new;
    }
    else {
        var r_new = list.__call__([]);
        iterate(iter.__call__(this.split(" ")), function(item) {
                if (len(item) > 0)
                    r_new.append(item);
        });
        return r_new;
    }
});

str.prototype.splitlines = Function(function() {
    return this.split("\n");
});

str.prototype.lower = Function(function() {
    return __py2js_str.__call__(this._obj.toLowerCase());
});

str.prototype.upper = Function(function() {
    return __py2js_str.__call__(this._obj.toUpperCase());
});

