function levels(code, options) {
    var ast = esprima.parse(code, {range:true});
    return eslevels.levels(ast, options);
}