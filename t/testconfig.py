#!/usr/bin/env python

import unittest
import json

from __armando__ import Armando

###
Armando.initialize()
###

from config import Config

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = Config(rcfile='main.test.conf')

    def test_config_init(self):
        self.assertTrue(self.config is not None)

    def test_read_value(self):
        self.assertEqual(self.config.get('section_1.foo'), 'bar')
        self.assertEqual(self.config.get('section_1.not_exists'), None)

    def test_read_value_case_insensitive(self):
        self.assertEqual(self.config.get('section_1.FOO'), 'bar')
        self.assertEqual(self.config.get('SECTION_1.FOO'), 'bar')

    def test_dump(self):
        c = json.loads(self.config.dump())
        self.assertTrue(c is not None)
        self.assertEqual(c['section_1.foo'], 'bar')

    def test_envvar_expansion(self):
        self.assertEqual(self.config.get('section_4.basedir'), Armando.get_base_dir())
        self.assertEqual(self.config.get('section_4.tmpdir'), Armando.get_tmp_dir())
        self.assertEqual(self.config.get('section_4.logsdir'), Armando.get_logs_dir())
        self.assertEqual(self.config.get('section_4.libdir'), Armando.get_lib_dir())
        self.assertEqual(self.config.get('section_4.sharedir'), Armando.get_share_dir())

if __name__ == "__main__":
    unittest.main()

