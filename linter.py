import logging
import re
from SublimeLinter.lint import NodeLinter

logger = logging.getLogger('SublimeLinter.plugin.tslint')


def utf16_offset_to_index(text, offset):
    """Return the index in `text` of the character at UTF-16 code unit `offset`."""
    units = 0
    for index, char in enumerate(text):
        if units >= offset:
            return index
        units += 2 if ord(char) > 0xFFFF else 1

    return len(text)


class Tslint(NodeLinter):
    cmd = 'tslint --format verbose ${file}'
    regex = (
        r'^(?:'
        r'(ERROR:\s+\((?P<error>.*)\))|'
        r'(WARNING:\s+\((?P<warning>.*)\))'
        r')?'
        r'\s+(?P<filename>.+?)'
        r'\[(?P<line>\d+), (?P<col>\d+)\]: '
        r'(?P<message>.+)'
    )
    tempfile_suffix = '-'
    defaults = {
        'selector': 'source.ts, source.tsx'
    }

    def reposition_match(self, line, col, m, vv):
        if col is not None:
            # TSLint reports the column in UTF-16 code units (as TypeScript
            # does), a character outside the Basic Multilingual Plane, e.g. an
            # emoji, counts as two. Sublime counts characters.
            col = utf16_offset_to_index(vv.select_line(line), col)

        return super().reposition_match(line, col, m, vv)

    def on_stderr(self, stderr):
        # suppress warnings like "rule requires type information"

        stderr = re.sub(
            'Warning: .+\n', '', stderr)

        if stderr:
            self.notify_failure()
            logger.error(stderr)
