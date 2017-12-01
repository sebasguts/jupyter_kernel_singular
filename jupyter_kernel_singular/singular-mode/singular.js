define([
    'codemirror/lib/codemirror',
    'codemirror/addon/mode/simple'
], function (CodeMirror) {
    'use strict';

    var keyword = RegExp(['(?:apply|break|breakpoint|continue|else|export|exportto|for|if|importfrom|',
        'keepring|load|quit|return|while)\\b'].join(''))
    var type = RegExp(['(?:bigint|bigintmat|def|ideal|int|intmat|intvec|link|list|map|matrix|module|',
        'number|package|poly|proc|resolution|ring|string|vector|User|cone|fan|polytope|',
        'pyobject|reference|shared)\\b'].join(''))
    var builtin = RegExp(['(?:align|attrib|bareiss|betti|char|char_series|charstr|chinrem|cleardenom|close|coef|coeffs|',
        'contract|datetime|dbprint|defined|deg|degree|delete|denominator|det|diff|dim|division|dump|eliminate|eval|',
        'ERROR|example|execute|extgcd|facstd|factmodd|factorize|farey|fetch|fglm|fglmquot|files|find|finduni|',
        'fprintf|freemodule|frwalk|gcd|gen|getdump|groebner|help|highcorner|hilb|homog|hres|imap|impart|indepSet|',
        'insert|interpolation|interred|intersect|jacob|janet|jet|kbase|kernel|kill|killattrib|koszul|laguerre|lead|',
        'leadcoef|leadexp|leadmonom|LIB|lift|liftstd|listvar|lres|ludecomp|luinverse|lusolve|max|maxideal|memory|',
        'min|minbase|minor|minres|modulo|monitor|monomial|mpresmat|mres|mstd|mult|nameof|names|ncols|npars|nres|',
        'nrows|numerator|nvars|open|option|ord|ordstr|par|pardeg|parstr|preimage|prime|primefactors|print|printf|',
        'prune|qhweight|qrds|quit|quote|quotient|random|rank|read|reduce|regularity|repart|res|reservedName|',
        'resultant|ringlist|ring_list|rvar|sba|setring|simplex|simplify|size|slimgb|sortvec|sqrfree|sprintf|sres|',
        'status|std|stdfglm|stdhilb|subst|system|syz|trace|transpose|type|typeof|univariate|uressolve|vandermonde|',
        'var|variables|varstr|vdim|waitall|waitfirst|wedge|weight|weightKB|write)\\b'].join(''))

    CodeMirror.defineSimpleMode("singular", {
        // The start state contains the rules that are intially used
        start: [
            {regex: /"(?:[^\\]|\\.)*?(?:"|$)/, token: "string"},
            {regex: keyword, token: "keyword"},
            {regex: type, token: "qualifier"},
            {regex: builtin, token: "builtin"},
            {regex: /0x[a-f\d]+|[-+]?(?:\.\d+|\d+\.?\d*)(?:e[-+]?\d+)?/i, token: "number"},
            {regex: /\/\/.*/, token: "comment"},
            {regex: /\/(?:[^\\]|\\.)*?\//, token: "variable-3"},
            // A next property will cause the mode to move to a different state
            {regex: /\/\*/, token: "comment", next: "comment"},
            {regex: /[-+\/*=<>!]+/, token: "operator"},
            // indent and dedent properties guide autoindentation
            {regex: /[\{\[\(]/, indent: true},
            {regex: /[\}\]\)]/, dedent: true},
            {regex: /[a-z$][\w$]*/, token: "variable"}
        ],
        // The multi-line comment state.
        comment: [
            {regex: /.*?\*\//, token: "comment", next: "start"},
            {regex: /.*/, token: "comment"}
        ],
        // The meta property contains global information about the mode. It
        // can contain properties like lineComment, which are supported by
        // all modes, and also directives like dontIndentStates, which are
        // specific to simple modes.
        meta: {
            dontIndentStates: ["comment"],
            lineComment: "//"
        }
    });
    CodeMirror.defineMIME('text/x-singular', 'singular');
});
