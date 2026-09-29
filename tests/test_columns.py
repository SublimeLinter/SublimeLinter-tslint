import importlib
import unittest

import sublime
from SublimeLinter.lint.linter import VirtualView


LinterModule = importlib.import_module('SublimeLinter-tslint.linter')
Linter = LinterModule.Tslint


# Real output of `tslint --format verbose a.ts` (tslint 6.1.3) for this source, with the
# rules quotemark (double), semicolon (always) and no-var-keyword. TSLint counts columns in
# UTF-16 code units, so the emoji (U+1F600) before the errors counts as two.
SOURCE = (
    'const a: string = "é\U0001f600"; var x = \'q\'\n'
    'const b = \'\U0001f600\' + \'z\';\n'
)
OUTPUT = (
    "ERROR: (no-var-keyword) a.ts[1, 26]: Forbidden 'var' keyword, use 'let' or 'const' instead\n"
    "ERROR: (quotemark) a.ts[1, 34]: ' should be \"\n"
    "ERROR: (semicolon) a.ts[1, 37]: Missing semicolon\n"
    "ERROR: (quotemark) a.ts[2, 11]: ' should be \"\n"
    "ERROR: (quotemark) a.ts[2, 18]: ' should be \"\n"
)


class TestColumns(unittest.TestCase):
    def resolve(self):
        linter = Linter(sublime.View(0), {})
        vv = VirtualView(SOURCE)
        return [
            (m['line'],) + linter.reposition_match(m['line'], m['col'], m, vv)[1:2]
            for m in linter.find_errors(OUTPUT)
        ]

    def test_columns_after_an_emoji_are_characters(self):
        line1, line2 = SOURCE.split('\n')[:2]
        self.assertEqual(
            self.resolve(),
            [
                (0, line1.index('var')),
                (0, line1.index("'q'")),
                (0, len(line1)),
                (1, line2.index("'")),
                (1, line2.index("'z'")),
            ],
        )

    def test_offsets_before_any_emoji_are_unchanged(self):
        f = LinterModule.utf16_offset_to_index
        self.assertEqual(f('abc', 0), 0)
        self.assertEqual(f('abc', 2), 2)
        self.assertEqual(f('ééx', 2), 2)

    def test_emoji_counts_as_two_units(self):
        f = LinterModule.utf16_offset_to_index
        text = 'a\U0001f600b'
        self.assertEqual(f(text, 1), 1)  # the emoji itself
        self.assertEqual(f(text, 3), 2)  # `b`, after the two units of the emoji
        self.assertEqual(f(text, 4), 3)  # end of line

    def test_offset_past_the_end_is_the_end_of_the_line(self):
        f = LinterModule.utf16_offset_to_index
        self.assertEqual(f('ab', 5), 2)
        self.assertEqual(f('', 0), 0)
