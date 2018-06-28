import logging
import re
from SublimeLinter.lint import NodeLinter

logger = logging.getLogger('SublimeLinter.plugin.tslint')


class Tslint(NodeLinter):
    cmd = 'tslint ${file}'
    npm_name = 'tslint'
    regex = (
        r'^(?:(?P<error>ERROR)|(?P<warning>WARNING))?'
        r'.+?\[(?P<line>\d+), (?P<col>\d+)\]: '
        r'(?P<message>.+)'
    )
    tempfile_suffix = '-'
    defaults = {
        'selector': 'source.ts, source.tsx'
    }

    def on_stderr(self, stderr):
        # suppress warnings like "rule requires type information"

        stderr = re.sub(
            'Warning: .+\n', '', stderr)

        if stderr:
            self.notify_failure()
            logger.error(stderr)
