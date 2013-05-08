import sys
import imp

# Dependecy reloader for Levels plugin
# The original idea is borrowed from
# https://github.com/wbond/sublime_package_control/blob/master/
# package_control/reloader.py

reload_mods = []
for mod in sys.modules:
    if mod.startswith('levels') and sys.modules[mod] is not None:
        reload_mods.append(mod)

mods_load_order = [
    'levels.semver',
    'levels.pyv8loader',
    'levels.pyv8delegate',
    'levels.js'
]

for mod in mods_load_order:
    if mod in reload_mods:
        imp.reload(sys.modules[mod])
