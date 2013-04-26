function levels(code) {
    var ast = esprima.parse(code, {range:true});
    return eslevels.levels(ast);
}