#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Anton Lavrenov
# Copyright (c) 2014 Anton Lavrenov
#
# License: MIT
#

"""This module exports the Tslint plugin class."""

import os

from SublimeLinter.lint import NodeLinter, util
try:
    from SublimeLinter.lint import VERSION
except ImportError:
    VERSION = 3


class Tslint(NodeLinter):
    """Provides an interface to tslint."""

    syntax = ('typescript', 'typescriptreact')
    cmd = ('tslint', '@')
    npm_name = 'tslint'
    regex = (
        r'^(?:(?P<error>ERROR)|(?P<warning>WARNING))'
        r'.+?\[(?P<line>\d+), (?P<col>\d+)\]: '
        r'(?P<message>.+)'
    )
    # tempfile_suffix = {'typescript': 'ts', 'typescriptreact': 'tsx'}
    tempfile_suffix = '-'
    
    if VERSION > 3:
        defaults = {
            '--config': '${folder}/tslint.json',
            '--project': '${folder}'
        }    

    if VERSION < 4:
        config_file = ('--config', 'tslint.json', '~')
        
        def build_args(self, settings=None):
            """Override build_args to allow setting a custom config filename."""
            backup = self.config_file
            if 'config_filename' in settings and self.filename:
                self.config_file = self.config_file[:1] + (settings['config_filename'],) + self.config_file[2:]

            out = super().build_args(settings)

            projectPath = self.__findTSConfigPath()
            if projectPath is not None:
                out.extend(['--project', projectPath])

            # Reset the value of config_file so that this can apply per-project.
            self.config_file = backup

            return out

        def __findTSConfigPath(self):
            return util.find_file(os.path.dirname(self.filename), 'tsconfig.json')
