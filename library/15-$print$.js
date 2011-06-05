/*
requires: $defined$
contains: $print$
 */

py_builtins.print = function(s) {
    if (typeof(console) != "undefined" && defined(console.log)) {
        console.log(s);
    } else {
        if (arguments.length <= 1) {
            if (defined(s)) {
                print(__py2js_str.__call__(s));
            } else {
                print("");
            }
        } else {
            var args = tuple.__call__(Array.prototype.slice.call(arguments, 0));
            print(__py2js_str.__call__(" ").join(args));
        }
    }
};
