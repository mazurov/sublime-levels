# Levels

**SublimeText** plugin for scope context coloring.
Inspired by [Douglas Crockford idea](https://plus.google.com/u/0/113127438179392830442/posts/XjR4WmSDFAV)

By Sasha Mazurov (alexander.mazurov@gmail.com)

<img src="https://raw.github.com/mazurov/sublime-levels/master/examples/levels_demo.gif" width="600" height="375"/>

* [Web version](http://mazurov.github.io/eslevels-demo/)

## Supported languages

* **JavaScript:** Uses my [eslevels][eslevels] and V8 Python binding  &mdash; [PyV8](https://github.com/emmetio/pyv8-binaries)

## How to install

**WARNING:** this plugin may not work at all in some OSes since it written in JavaScript and uses PyV8 and Google V8 binaries to run.


* Use [Package Control](http://wbond.net/sublime_packages/package_control): ```Preferences -> Package Control -> Install Package - > Levels```

or

* Clone or download git repo into your packages folder (In SublimeText ```Preferences->Browse Packages...``` menu item to open this folder):
   - Clone: ```git clone https://github.com/mazurov/sublime-levels.git Levels```
   - Download: https://github.com/mazurov/sublime-levels/archive/master.zip and extract sublime-levels-master to the packages folder.


**WARNING:** When plugin is installed, it will automatically download required PyV8 binary so you have to wait a bit (see Loading PyV8 binary message on status bar). If you experience issues with automatic PyV8 loader, try to install it manually.

## Available commands

* Enable scope context coloring: __Levels: Update__ ```Ctrl+Shift+L```
* Restore original coloring: __Levels: Off__ ```Ctrl+Shift+O```


* The code is automatically colored after a save action.
* 

## Options

* The **live** coloring mode  is switched off by default (the current plugin version works slow for large scripts). You can enable it in settings  by ```"live": true```.

* Javascript coloring support two modes: ```"mini"``` - highligt only "important" language constructions and ```"full"``` - highlight whole scopes.
You can set this options by changing ```javascript_mode``` value in settings.


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
