/*
  Copyright (C) 2013 Alexander (Sasha) Mazurov <alexander.mazurov@gmail.com>

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
  ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
  THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/
/*global escope: true, define:true, require:true, exports:true */
(function (root, factory) {
    'use strict';

    // Universal Module Definition (UMD) to support AMD, CommonJS/Node.js,
    // Rhino, and plain browser loading.
    if (typeof exports === 'object') {
        module.exports = factory(require('escope'));
    } else if (typeof define === 'function' && define.amd) {
        define(['escope'], factory);
    } else {
        root.eslevels = factory(escope);
    }
}(this, function (escope) {
    'use strict';
    var exports = {};

    // Cache names levels
    escope.Scope.prototype._cache = null;

    // Store scope level
    escope.Scope.prototype._level = null;

    // **Get scope level**
    //
    // Returns the Integer
    escope.Scope.prototype.level = function () {
        // Don't count functionExpressionScope
        if (this.functionExpressionScope) {
            return this.upper.level();
        }

        if (this._level === null) { // level not caclulated yet
            this._level = 0;
            if (this.upper !== null) {
                // ```upper``` points to parent scope
                this._level = 1 + this.upper.level();
            }
        }
        return this._level;
    };

    // **Find variable of function by name**
    //
    // Search in current or upper scopes
    //
    // Returns a level - the Integer
    escope.Scope.prototype.find = function (name) {
        var vars;
        if (this._cache === null) {
            this._cache = {};
        }
        if (this._cache[name] === undefined) {
            vars = this.variables;
            for (var i = 0; i < vars.length; ++i) {
                if (vars[i].name === name) {
                    if (vars[i].defs && vars[i].defs[0] &&
                        vars[i].defs[0].type === 'ImplicitGlobalVariable') {
                        this._cache[name] = -1;
                    } else {
                        this._cache[name] = this.level();
                    }
                }
            }

            if (this._cache[name] === undefined) {
                if (this.upper === null) {
                    this._cache[name] = -1;
                } else {
                    this._cache[name] = this.upper.find(name);
                }
            }
        }
        return this._cache[name];
    };

    var Region = function (level, first, last) {
        this.level = level;
        this.first = first;
        this.last = last;
    };

    Region.prototype.list = function () {
        return [this.level, this.first, this.last];
    };

    var RegionNode = function (region) {
        this.region = region;
        this.next = null;
    };

    var RegionList = function () {
        this.root = null;
    };

    RegionList.prototype.addRegion = function (region) {
        var regionNode, newNode, curr, prev;
        regionNode = new RegionNode(region);

        if (this.root === null) {
            this.root = regionNode;
            return this.root;
        }
        curr = this.root;
        prev = null;
        while (true) {
            if (!curr) {
                if (!prev) {
                    this.root = regionNode;
                } else {
                    prev.next = regionNode;
                }
                break;
            }

            if (region.first == curr.first && region.last==curr.last) {
                break;
            }

            if (region.first < curr.region.first) {
                regionNode.next = curr;
                if (!prev) {
                    this.root = regionNode;
                } else {
                    prev.next = regionNode;
                }
                break;
            }


            if (region.first === curr.region.first) {
                curr.region.first = region.last + 1;
                regionNode.next = curr;

                if (!prev) {
                    this.root = regionNode;
                } else {
                    prev.next = regionNode;
                }
                break;
            }

            if (region.last === curr.region.last) {
                curr.region.last = region.first - 1;
                regionNode.next = curr.next;
                curr.next = regionNode;
                break;
            }

            if ((region.first > curr.region.first) &&
                (region.last < curr.region.last)) {
                newNode = new RegionNode(
                    new Region(
                    curr.region.level,
                    curr.region.first,
                    region.first - 1));
                newNode.next = regionNode;
                regionNode.next = curr;
                curr.region.first = region.last + 1;

                if (!prev) {
                    this.root = newNode;
                } else {
                    prev.next = newNode;
                }
                break;
            }
            prev = curr;
            curr = curr.next;
        }
    };

    RegionList.prototype.list = function () {
        var result = [];
        var currNode = this.root;
        var item, last;

        var prev=null;
        var len;
        while (currNode) {
            len = result.length;
            item = currNode.region.list();
            if (len) {
                last = result[len-1];
                if ((last[0] === item[0]) && (last[2] === item[1]-1)) {
                    last[2] = item[2];
                } else {
                    result.push(item);
                }
            } else{
                result.push(item);
            }
            currNode = currNode.next;
        }
        // console.log(result);
        return result;
    };


    function addMainScopes(result, scopes) {
        for (var i = 0; i < scopes.length; i++) {
            if (!scopes[i].functionExpressionScope &&
                scopes[i].type !== 'with') {
                result.addRegion(
                    new Region(
                    scopes[i].level(),
                    scopes[i].block.range[0],
                    scopes[i].block.range[1]));
            }
        }
    }

    function addScopeVariables(result, scope, isFullMode) {
        var refs = scope.references,
            vars = scope.variables;
        var level, identifier, exists;

        switch(scope.type) {
            case 'function':
                if (!scope.functionExpressionScope) {
                    result.addRegion(new Region(scope.level(),
                        scope.block.range[0], scope.block.range[0] + 8 - 1));
                }
                break;
            case 'with':
                result.addRegion(new Region(scope.level()-1,
                        scope.block.range[0], scope.block.range[0] + 4 - 1));
                break;
            case 'catch':
                result.addRegion(new Region(scope.level(),
                        scope.block.range[0], scope.block.range[0] + 5 - 1));
                break;
            default:
                break;

        }

        for (var i = 0; i < vars.length; i++) {
            if (vars[i].defs.length &&
                vars[i].defs[0].type === 'ImplicitGlobalVariable') {
                continue;
            }

            if (vars[i].identifiers && vars[i].identifiers[0]) {
                result.addRegion(
                    new Region(
                    scope.level(),
                    vars[i].identifiers[0].range[0],
                    vars[i].identifiers[0].range[1] - 1));
            }
        }


        for (i = 0; i < refs.length; i++) {
            identifier = refs[i].identifier;
            level = scope.find(identifier.name);


            exists = false;
            if (level != -1) {
                if (scope.type === 'catch') {
                    vars = scope.upper.variables;
                }

                for (var j = 0; j < vars.length; j += 1) {
                    if (vars[j].identifiers && vars[j].identifiers[0] &&
                        vars[j].identifiers[0].range[0] === identifier.range[0])
                    {
                        exists = true;
                    }
                }
            }
            if (!exists) {
                result.addRegion(
                    new Region(
                    level,
                    identifier.range[0],
                    identifier.range[1] - 1));
            }
        }
    }


    var getScopes = function (ast) {
        if (typeof ast === 'object' && ast.type === 'Program') {
            if (typeof ast.range !== 'object' || ast.range.length !== 2) {
                throw new Error('eslevels: Context only accepts a syntax tree' +
                    'with range information');
            }
        }
        return escope.analyze(ast)
            .scopes;
    };

    var modes = {};

    modes.full = function (result, ast, scopes) {
        addMainScopes(result, scopes);
        for (var i = 0; i < scopes.length; i++) {
            addScopeVariables(result, scopes[i], true);
        }
        return result.list();
    };

    modes.mini = function (result, ast, scopes) {
        for (var i = 0; i < scopes.length; i += 1) {
            addScopeVariables(result, scopes[i], false);
        }
    };

    exports.levels = function (ast, options) {
        var opts = options || {};
        opts.mode = opts.mode || 'full';
        var result = new RegionList();
        var scopes = getScopes(ast);
        modes[opts.mode](result, ast, scopes);
        return result.list();
    };

    exports.version = '0.3.0';
    return exports;
}));