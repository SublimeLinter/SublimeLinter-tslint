from SublimeLinter.lint import NodeLinter


class Tslint(NodeLinter):
    cmd = 'tslint ${file}'
    npm_name = 'tslint'
    regex = (
        r'^(?:(?P<error>ERROR)|(?P<warning>WARNING))'
        r'.+?\[(?P<line>\d+), (?P<col>\d+)\]: '
        r'(?P<message>.+)'
    )
    tempfile_suffix = '-'
    defaults = {
        'selector': 'source.ts, source.tsx',
        '--config': '${folder}/tslint.json',
        '--project': '${folder}'
    }
