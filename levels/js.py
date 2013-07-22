import os
import sys
import imp
import codecs

import sublime

JS = None
V8CONTEXT = None

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
PACKAGE_PATH = os.path.abspath(os.path.dirname(BASE_PATH))



def import_pyv8():
    # Importing non-existing modules is a bit tricky in Python:
    # if we simply call `import PyV8` and module doesn't exists,
    # Python will cache this failed import and will always
    # throw exception even if this module appear in PYTHONPATH.
    # To prevent this, we have to manually test if
    # PyV8.py(c) exists in PYTHONPATH before importing PyV8
    if 'PyV8' in sys.modules and 'PyV8' not in globals():
        # PyV8 was loaded by ST2, create global alias
        globals()['PyV8'] = __import__('PyV8')
        return

    loaded = False
    f, pathname, description = imp.find_module('PyV8')
    bin_f, bin_pathname, bin_description = imp.find_module('_PyV8')
    if f:
        try:
            imp.acquire_lock()
            globals()['_PyV8'] = imp.load_module('_PyV8', bin_f, bin_pathname,
                                                 bin_description)
            globals()['PyV8'] = imp.load_module('PyV8', f, pathname,
                                                description)
            imp.release_lock()
            loaded = True
        finally:
            # Since we may exit via an exception, close fp explicitly.
            if f:
                f.close()
            if bin_f:
                bin_f.close()

    if not loaded:
        raise ImportError('No PyV8 module found')


def js_file_reader(file_path, use_unicode=True):
    if hasattr(sublime, 'load_resource'):
        rel_path = file_path
        for prefix in [sublime.packages_path(), sublime.installed_packages_path()]:
            if rel_path.startswith(prefix):
                rel_path = os.path.join('Packages', rel_path[len(prefix) + 1:])
                break

        rel_path = rel_path.replace('.sublime-package', '')
        # for Windows we have to replace slashes
        rel_path = rel_path.replace('\\', '/')

        return sublime.load_resource(rel_path)

    if use_unicode:
        f = codecs.open(file_path, 'r', 'utf-8')
    else:
        f = open(file_path, 'r')

    content = f.read()
    f.close()

    return content


def js():
    global V8CONTEXT, JS
    if not JS:
        import_pyv8()
        files = [
            "esprima.js",
            "estraverse.js",
            "escope.js",
            "eslevels.js",
            "colorize.js"]

        V8CONTEXT = PyV8.JSContext()  # noqa
        V8CONTEXT.enter()
        for f in files:
            src_path = os.path.join(PACKAGE_PATH, "js", f)
            code = js_file_reader(src_path)
            V8CONTEXT.eval(code)
        JS = V8CONTEXT.eval("levels")
    return JS


def run(source, options):
    color = js()(source, options)
    result = []
    for k in color:
        level, x1, x2 = (int(k[0]),
                         int(k[1]),
                         int(k[2]))
        result.append((level, x1, x2))
    return result
