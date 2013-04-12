import sys
import os
import sublime
import sublime_plugin
import imp

from collections import defaultdict

__author__ = 'Sasha Mazurov (alexander.mazurov@gmail.com)'
__version__ = '0.1'

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
PACKAGES_PATH = sublime.packages_path() or os.path.dirname(BASE_PATH)
sys.path += [BASE_PATH]

# Make sure all dependencies are reloaded on upgrade
if 'levels.reloader' in sys.modules:
    imp.reload(sys.modules['levels.reloader'])

import levels.reloader
import levels.pyv8loader as pyv8loader
import levels.pyv8delegate as pyv8delegate
import levels.jslint


# Views session storage
SESSION = defaultdict(dict)

# Default ST settings
USER_SETTINGS = None


def is_st3():
    return sublime.version()[0] == '3'


def user_settings():
    return globals()['USER_SETTINGS']


def session():
    return globals()['SESSION']


def in_session(view):
    return view.id() in session()


def remove_from_session(view):
    del session()[view.id()]


def settings():
    return sublime.load_settings("Levels.sublime-settings")


def settings_get(key, default=None):
    return settings().get(key) if settings().has(key) else default


def mode_settings(syntax):
    if settings().has("modes"):
        modes = settings().get("modes")
        for mode in modes:
            if syntax.find(mode["syntax"]) > -1:
                return mode
    return None


def init():
    globals()['USER_SETTINGS'] = sublime.load_settings(
        'Preferences.sublime-settings'
    )

    # setup environment for PyV8 loading
    pyv8_paths = [
        os.path.join(PACKAGES_PATH, 'PyV8'),
        os.path.join(PACKAGES_PATH, 'PyV8', pyv8loader.get_arch()),
        os.path.join(PACKAGES_PATH, 'PyV8', 'pyv8-%s' % pyv8loader.get_arch())
    ]

    for p in pyv8_paths:
        if p not in sys.path:
            sys.path += [p]

    # unpack recently loaded binary, is exists
    for p in pyv8_paths:
        pyv8loader.unpack_pyv8(p)

    delegate = pyv8delegate.SublimeLoaderDelegate(settings=user_settings())
    pyv8loader.load(pyv8_paths[1], delegate)


def find_engine(mode_settings):
    engine = sys.modules["levels.%s" % mode_settings["engine"]]
    return engine


def colorize(view, result):
    levels = defaultdict(list)
    # group levels
    for level, line, x1, x2 in result:
        vx1, vx2 = (view.text_point(line - 1, x1 - 1),
                    view.text_point(line - 1, x2 - 1))
        levels[level].append(sublime.Region(vx1, vx2))

    options = sublime.PERSISTENT
   
    for l in levels.keys():
        name = "level%d" % l
        view.add_regions(name, levels[l], name, "",options)
    return max(levels.keys()) + 1


def update_view(view):
    view_id = view.id()
    engine = session()[view_id]["engine"]
    result = engine.run(
        view.substr(sublime.Region(0, view.size())), {}
    )
    if result is None:
        return
    nlevels = colorize(view, result)
    session()[view_id]["nlevels"] = nlevels


def reset_view(view):
    view_session = session()[view.id()]
    for l in range(view_session["nlevels"]):
        view.erase_regions("level%d" % l)
    view.settings().set("color_scheme", view_session["color_scheme"])
    remove_from_session(view)


class LevelsUpdateCommand(sublime_plugin.TextCommand):

    def run(self, edit, command=None, output='', begin=0, region=None):
        if not in_session(self.view):
            mode = mode_settings(self.view.settings().get("syntax"))
            engine = find_engine(mode)

            old_color_scheme = self.view.settings().get("color_scheme")
            self.view.settings().set(
                "color_scheme",
                settings().get(
                    "color_scheme",
                    "Packages/sublime-levels/Levels-light.hidden-tmTheme"
                )
            )

            session()[self.view.id()]["engine"] = engine
            session()[self.view.id()]["color_scheme"] = old_color_scheme

            update_view(self.view)
        else:
            update_view(self.view)


class LevelsOffCommand(sublime_plugin.TextCommand):

    def run(self, edit, command=None, output='', begin=0, region=None):
        if self.is_enabled():
            reset_view(self.view)

    def is_enabled(self):
        return in_session(self.view)


class LevelsListener(sublime_plugin.EventListener):

    def on_modified(self, view):
        if in_session(view) and settings().get("live", False):
            update_view(view)

    def on_post_save(self, view):
        if in_session(view):
            update_view(view)


def plugin_loaded():
    init()

if not is_st3():
    sublime.set_timeout(init, 200)
