import PyV8
import os

JSLINT = None

def jslint():
    global JSLINT
    if not JSLINT:
        src_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "jslint.js")
        ctxt = PyV8.JSContext()
        ctxt.enter()
        src_file = open(src_path, "r")
        ctxt.eval(src_file.read())
        JSLINT = ctxt.eval("JSLINT")
    return JSLINT


def run(source, options):
    # self.view.substr(sublime.Region(0, self.view.size()))
    jslint()(source, {"maxerr": 1e+5})
    color = jslint().jslint.color(jslint().data())
    result = []
    for k in color.keys():
        level, line, x1, x2 = (int(color[k].level),
                               int(color[k].line),
                               int(color[k]["from"]),
                               int(color[k]["thru"]))
        result.append((level, line, x1, x2))
    return result
