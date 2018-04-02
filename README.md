SublimeLinter-tslint
================================

[![Build Status](https://travis-ci.org/SublimeLinter/SublimeLinter-tslint.svg?branch=master)](https://travis-ci.org/SublimeLinter/SublimeLinter-tslint)

This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter) provides an interface to [tslint](https://github.com/palantir/tslint).
It will be used with files that have the "typescript" syntax.


## Installation

SublimeLinter must be installed in order to use this plugin. 

Please use [Package Control](https://packagecontrol.io) to install the linter plugin.

Before installing this plugin, ensure that `tslint` (2.4.0 or later) is installed on your system.
To install `tslint`, do the following:

1. Install [Node.js](http://nodejs.org) (and [npm](https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager) on Linux).

1. Install `tslint` by typing the following in a terminal:
   ```
   npm install -g tslint
   ```

1. If you are using `nvm` and `zsh`, ensure that the line to load `nvm` is in `.zshenv` and not `.zshrc`.


## Settings

- SublimeLinter settings: http://sublimelinter.com/en/latest/settings.html
- Linter settings: http://sublimelinter.com/en/latest/linter_settings.html

You can configure `tslint` options in the way you would from the command line, with `tslint.json` files. For more information, see the [tslint docs](https://github.com/palantir/tslint). The linter plugin does this by searching for a `tslint.json` file itself, just as `tslint` does from the command line. 

You may provide a custom config file by setting the linter’s `"args"` setting to `["--config", "/path/to/file"]`. On Windows, be sure to double the backslashes in the path, for example `["--config", "C:\\Users\\Aparajita\\tslint.json"]`.

Also, remember to set your project `tsconfig.json` accordingly, so that it includes paths used by SublimeLinter *working copies*. For example:

```json
    "include": [
        "/var/folders/**/*.tsx",
        "/var/folders/**/*.ts",
        "./src/**/*.tsx",
        "./src/**/*.ts"
    ],
```
