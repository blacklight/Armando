#!/usr/bin/env python

import unittest
import json

from __armando__ import Armando

###
Armando.initialize()
###

from config import Config
from mpd import MPD
from mock.mpdservermock import MpdServerMock

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = Config.get_config('conf/main.test.conf')
        self.mpd_mock = MpdServerMock()
        self.mpd_mock.start()
        self.mpd = MPD()

    def test_current_song(self):
        current_track = self.mpd.get_current_track()
        self.assertEqual(current_track.get('artist'), None)

        self.mpd.server_cmd('play')

        current_track = self.mpd.get_current_track()
        self.assertEqual(current_track.get('artist'), 'Miles Davis')
        self.assertEqual(True, False)

    def tearDown(self):
        self.mpd_mock.stop()

if __name__ == "__main__":
    unittest.main()

