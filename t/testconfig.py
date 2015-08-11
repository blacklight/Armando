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
        self.assertTrue(self.config is not None, "The configuration object was not created")

    def test_read_value(self):
        self.assertEqual(self.config.get('logger.loglevel'), 'DEBUG', "logger.loglevel is not readable")
        self.assertEqual(self.config.get('logger.not_exists'), None, "logger.not_exists should not exist")

    def test_read_value_case_insensitive(self):
        self.assertEqual(self.config.get('LOGGER.loglevel'), 'DEBUG', "LOGGER.loglevel (case-insensitive) is not readable")
        self.assertEqual(self.config.get('LOGGER.LOGLEVEL'), 'DEBUG', "LOGGER.LOGLEVEL (case-insensitive) is not readable")

    def test_dump(self):
        c = json.loads(self.config.dump())
        self.assertTrue(c is not None, "The config dump failed")
        self.assertEqual(c['mpd.host'], 'localhost', 'mpd.host is not in the config dump')

    def test_envvar_expansion(self):
        self.assertEqual(self.config.get('dirs.basedir'), Armando.get_base_dir(), 'dirs.basedir incorrectly set')
        self.assertEqual(self.config.get('dirs.tmpdir'), Armando.get_tmp_dir(), 'dirs.basedir incorrectly set')
        self.assertEqual(self.config.get('dirs.logsdir'), Armando.get_logs_dir(), 'dirs.basedir incorrectly set')
        self.assertEqual(self.config.get('dirs.libdir'), Armando.get_lib_dir(), 'dirs.basedir incorrectly set')
        self.assertEqual(self.config.get('dirs.sharedir'), Armando.get_share_dir(), 'dirs.basedir incorrectly set')

if __name__ == "__main__":
    unittest.main()

