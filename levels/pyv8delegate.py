import sys
import imp
import sublime
import levels.pyv8loader as pyv8loader


class SublimeLoaderDelegate(pyv8loader.LoaderDelegate):

    def __init__(self, user_settings):
        settings = {}
        for k in ['http_proxy', 'https_proxy', 'timeout']:
                if user_settings.has(k):
                    settings[k] = user_settings.get(k, None)
        pyv8loader.LoaderDelegate.__init__(self, settings)
        self.state = None
        self.message = 'Loading PyV8 binary, please wait'
        self.i = 0
        self.addend = 1
        self.size = 8

    def on_start(self, *args, **kwargs):
        self.state = 'loading'

    def on_progress(self, *args, **kwargs):
        if kwargs['progress'].is_background:
            return

        before = self.i % self.size
        after = (self.size - 1) - before
        msg = '%s [%s=%s]' % (self.message, ' ' * before, ' ' * after)
        if not after:
            self.addend = -1
        if not before:
            self.addend = 1
        self.i += self.addend

        sublime.set_timeout(lambda: sublime.status_message(msg), 0)

    def on_complete(self, *args, **kwargs):
        self.state = 'complete'

    def on_error(self, exit_code=-1, progress=None):
        self.state = 'error'
        sublime.set_timeout(lambda: show_pyv8_error(exit_code), 0)

    def setting(self, name, default=None):
        "Returns specified setting name"
        return self.settings.get(name, default)

    def log(self, message):
        print('Levels: %s' % message)


def show_pyv8_error(exit_code):
    if 'PyV8' not in sys.modules:
        sublime.error_message(
            'Error while loading PyV8 binary: exit code %s\n'
            'Try to manually install PyV8 from'
            'https://github.com/emmetio/pyv8-binaries' % exit_code)
