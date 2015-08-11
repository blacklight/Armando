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
        self.config = Config(rcfile='conf/main.test.conf')

    def test_config_init(self):
        self.assertTrue(self.config is not None)

    def test_read_value(self):
        self.assertEqual(self.config.get('logger.loglevel'), 'DEBUG')
        self.assertEqual(self.config.get('logger.not_exists'), None)

    def test_read_value_case_insensitive(self):
        self.assertEqual(self.config.get('LOGGER.loglevel'), 'DEBUG')
        self.assertEqual(self.config.get('LOGGER.LOGLEVEL'), 'DEBUG')

    def test_dump(self):
        c = json.loads(self.config.dump())
        self.assertTrue(c is not None)
        self.assertEqual(c['mpd.host'], 'localhost')

    def test_envvar_expansion(self):
        self.assertEqual(self.config.get('dirs.basedir'), Armando.get_base_dir())
        self.assertEqual(self.config.get('dirs.tmpdir'), Armando.get_tmp_dir())
        self.assertEqual(self.config.get('dirs.logsdir'), Armando.get_logs_dir())
        self.assertEqual(self.config.get('dirs.libdir'), Armando.get_lib_dir())
        self.assertEqual(self.config.get('dirs.sharedir'), Armando.get_share_dir())

if __name__ == "__main__":
    unittest.main()

