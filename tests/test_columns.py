import importlib
import unittest

import sublime
from SublimeLinter.lint.linter import VirtualView


Linter = importlib.import_module('SublimeLinter-tslint.linter').Tslint

# Captured TSLint 6.1.3 output, with quotemark, semicolon and no-var-keyword rules.
SOURCE = 'const a: string = "é😀"; var x = \'q\'\nconst b = \'😀\' + \'z\';\n'
OUTPUT = (
    "ERROR: (no-var-keyword) a.ts[1, 26]: Forbidden 'var' keyword, use 'let' or 'const' instead\n"
    "ERROR: (quotemark) a.ts[1, 34]: ' should be \"\n"
    "ERROR: (semicolon) a.ts[1, 37]: Missing semicolon\n"
    "ERROR: (quotemark) a.ts[2, 11]: ' should be \"\n"
    "ERROR: (quotemark) a.ts[2, 18]: ' should be \"\n"
)


class TestColumns(unittest.TestCase):
    def test_captured_unicode_diagnostics(self):
        lines = SOURCE.splitlines()
        expected = [(0, lines[0].index('var'), 'var'), (0, lines[0].index("'q'"), "'"),
                    (0, len(lines[0]), '\n'), (1, lines[1].index("'"), "'"),
                    (1, lines[1].index("'z'"), "'")]
        self.assertDiagnostics(OUTPUT, SOURCE, expected)

    def test_near_line_end_columns_are_converted_before_clamping(self):
        for source, column, text in [
            ('const s = "😀😀😀😀😀😀😀😀" + \'z\';', 32, "'"),
            ('const s = "😀😀😀😀😀😀😀😀"; var x;', 31, 'var'),
        ]:
            with self.subTest(source=source):
                output = 'ERROR: (rule) a.ts[1, {}]: problem'.format(column)
                self.assertDiagnostics(output, source, [(0, source.index(text), text)])

    def test_ascii_numeric_columns_keep_their_base(self):
        self.assertDiagnostics('ERROR: (rule) a.ts[1, 1]: problem', 'var x;', [(0, 0, 'var')])

    def assertDiagnostics(self, output, source, expected):
        linter = Linter(sublime.View(0), {})
        vv = VirtualView(source)
        matches = list(linter.find_errors(output))
        self.assertEqual(len(matches), len(expected))
        for match, (line, col, text) in zip(matches, expected):
            match['filename'] = None
            error = linter.process_match(match, vv)
            self.assertIsNotNone(error)
            begin = vv.full_line(line)[0] + col
            self.assertEqual({k: error[k] for k in ('line', 'start', 'region', 'offending_text')}, {
                'line': line, 'start': col, 'region': sublime.Region(begin, begin + len(text)),
                'offending_text': text,
            })
