#!/usr/bin/env python

import unittest
import os

from __armando__ import Armando

###
Armando.initialize()
###

from config import Config

class TestTakkRules(unittest.TestCase):
    __dummy_file = 'test_action_dummy_file'

    def setUp(self):
        Config.get_config('conf/main.test.conf')
        from rules import Rules
        self.rules = Rules('conf/speech.test.xml')

    def test_pattern_matched(self):
        patterns = self.rules.pattern_match('play some music artist Led Zeppelin')
        self.assertGreater(len(patterns), 0)
        self.assertEqual(patterns[0]['id'], 'play-music')
        self.assertEqual(patterns[0]['attributes']['artist'], 'Led Zeppelin')

    def test_pattern_not_matched(self):
        patterns = self.rules.pattern_match('this will never be matched by any of my rules')
        self.assertEqual(len(patterns), 0)

    def test_non_existing_action(self):
        self.assertRaises(KeyError, self.rules.run_action, 'non-existing-action')

    def test_get_rules_by_pattern(self):
        rules = self.rules.get_rules_by_patterns(['create-file'])
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0], 'create-test-file-shell-on-create-file')

    def test_get_rules_by_multiple_patterns(self):
        rules = self.rules.get_rules_by_patterns(['create-file', 'remove-file'])
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0], 'create-and-remove-test-file-shell-on-double-command')

    def test_get_rules_by_non_existing_pattern(self):
        rules = self.rules.get_rules_by_patterns(['i-dont-exist'])
        self.assertEqual(len(rules), 0)

    def test_shell_action(self):
        self.rules.run_action('create-test-file-shell',
            {'filename': self.__dummy_file }
        )

        self.assertTrue(os.path.isfile(self.__dummy_file))

        self.rules.run_action('remove-test-file-shell',
            {'filename': self.__dummy_file }
        )

        self.assertFalse(os.path.isfile(self.__dummy_file))

    def test_python_action(self):
        self.rules.run_action('create-test-file-python',
            {'filename': self.__dummy_file }
        )

        self.assertTrue(os.path.isfile(self.__dummy_file))

        self.rules.run_action('remove-test-file-python',
            {'filename': self.__dummy_file }
        )

        self.assertFalse(os.path.isfile(self.__dummy_file))

    def tearDown(self):
        if os.path.isfile(self.__dummy_file):
            os.remove(self.__dummy_file)

if __name__ == "__main__":
    unittest.main()

