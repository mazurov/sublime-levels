import sys
import os
import sublime
import sublime_plugin
import importlib
import imp

from collections import defaultdict

SESSION = defaultdict(dict)


def session():
    return SESSION


def in_session(view):
    return view.id() in session()


def log(severity, msg):
    print("%s (Levels plugin): " + msg)


def err(msg):
    log("ERROR", msg)


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


def find_engine(mode_settings):
    engine = importlib.import_module("levels.%s" % mode_settings["engine"])
    return engine


def plugin_loaded():
    sys.path.insert(0, os.path.join(os.path.dirname(__file__)))


def colorize(view, result):
    levels = defaultdict(list)
    # group levels
    for level, line, x1, x2 in result:
        vx1, vx2 = (view.text_point(line - 1, x1 - 1),
                    view.text_point(line - 1, x2 - 1))
        levels[level].append(sublime.Region(vx1, vx2))

    for l in levels.keys():
        name = "level%d" % l
        view.add_regions(name, levels[l], name, "",
                         sublime.DRAW_NO_OUTLINE
                         )
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
    del session()[view.id()]


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
                    "Packages/levels-sublime/Levels-light.hidden-tmTheme"
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
