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

from SublimeLinter.lint import NodeLinter


class Tslint(NodeLinter):
    cmd = ('tslint', '${file}')
    npm_name = 'tslint'
    regex = (
        r'^(?:(?P<error>ERROR)|(?P<warning>WARNING))'
        r'.+?\[(?P<line>\d+), (?P<col>\d+)\]: '
        r'(?P<message>.+)'
    )
    tempfile_suffix = '-'
    defaults = {
        'selector': 'source.ts',
        '--config': '${folder}/tslint.json',
        '--project': '${folder}'
    }
