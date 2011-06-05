/*
requires: $function$
requires: $iterate$

requires: __builtin__.list
requires: __builtin__.iter
requires: __builtin__.bool

contains: __builtin__.filter
 */

py_builtins.filter = Function(function(f, l) {
   res = list.__call__();
   iterate(iter.__call__(l), function(item) {
     if (py_builtins.bool(f(item))) {
       res.append(item);
     };
   });
   return res;
});

/*
requires: $function$
contains: __builtin__.reduce
 */

py_builtins.reduce = Function(function(func, seq) {
    var initial;
    if (arguments.length == 3) {
        initial = arguments[2];
    } else {
        initial = null;
    }
    if (len(seq) < 2) {
        return initial;
    }
    if (arguments.length == 3) {
        var accum = initial;
        var start = 0;
    } else {
        var accum = func(seq.__getitem__(0), seq.__getitem__(1));
        var start = 2;
    }
    for (var i = start; i < len(seq); i++) {
        accum = func(accum, seq.__getitem__(i));
    }
    return accum;
});
