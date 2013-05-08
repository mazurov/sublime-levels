# Levels

**SublimeText** plugin for scope context coloring.
Inspired by [Douglas Crockford idea](https://plus.google.com/u/0/113127438179392830442/posts/XjR4WmSDFAV)

By Sasha Mazurov (alexander.mazurov@gmail.com)

<img src="https://raw.github.com/mazurov/sublime-levels/master/examples/levels_demo.gif" width="600" height="375"/>

## Supported languages

* **JavaScript:** Uses my [eslevels][eslevels] and V8 Python binding  &mdash; [PyV8](https://github.com/emmetio/pyv8-binaries)

## How to install

**WARNING:** this plugin may not work at all in some OSes since it written in JavaScript and uses PyV8 and Google V8 binaries to run.



* Clone or download git repo into your packages folder (In SublimeText ```Preferences->Browse Packages...``` menu item to open this folder):
   - Clone: ```git clone https://github.com/mazurov/sublime-levels.git Levels```
   or
   - Download: https://github.com/mazurov/sublime-levels/archive/master.zip and extract sublime-levels-master to the packages folder.

or

*  Use Package Control in **SublimeText2** (until it's officially added to the [community packages list](http://wbond.net/sublime_packages/community) of ST plugins.) :
    * Preferences
    * Package Control
    * Add Repository
    * Insert the repository Url (should be `https://github.com/mazurov/sublime-levels.git`)
    * Then install it normally via Package Control by doing `Ctrl` + `Shift` + `P` -> `Install Package` -> `sublime-levels`

**WARNING:** Installation with Package Control is currently supported only in SublimeText2. For SublimeText3 use **manual installation**.


**WARNING:** When plugin is installed, it will automatically download required PyV8 binary so you have to wait a bit (see Loading PyV8 binary message on status bar). If you experience issues with automatic PyV8 loader, try to install it manually.

## Available commands

* Enable scope context coloring: __Levels: Update__ ```Ctrl+Shift+L```
* Restore original coloring: __Levels: Off__ ```Ctrl+Shift+O```

* The **live** coloring mode  is not switched on by default (the current plugin version works slow for large scripts). You can enable it in settings  by```"live": true```.
* The code is automatically colored after a save action.




## Theme customization

By default the plugin use a modified version of the default theme ```Solarized (Light)```. If you want to use your favorite theme, you need to add new scope coloring rules like in plugin's ```Levels-light.hidden-tmTheme```:

```xml
    <dict>
            <key>name</key>
            <string>Level0</string>
            <key>scope</key>
            <string>level0</string>
            <key>settings</key>
            <dict>
                <key>foreground</key>
                <string>#FDF6E3</string>
            </dict>
        </dict>
    ...
        <dict>
            <key>name</key>
            <string>Level9</string>
            <key>scope</key>
            <string>level9</string>
            <key>settings</key>
            <dict>
                <key>foreground</key>
                <string>#cf9369</string>
            </dict>
        </dict>
```

, and update ```color_scheme``` value in plugin settings (applied only for
scope coloring mode) or in default user settings.


## Known issues.

### Eslevels library

If you would like to be sure that your coloring problem is in [eslevels][eslevels] and not in
this plugin you can check your code on [this page](http://mazurov.github.io/eslevels-demo). 
If you have the same problems there then it means that the problem is in Eslevels library (or in your code)

## Credits

* Thanks to [Sergey Chikuyonok](https://github.com/sergeche) for the nice
idea of using PyV8.


[eslevels]: https://github.com/mazurov/eslevels
