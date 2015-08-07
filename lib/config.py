try:
    from configparser import SafeConfigParser
except ImportError as e:
    from ConfigParser import SafeConfigParser

from __init__ import Armando
from constants import Constants

import json
import os
import re
import sys

class ConfigError(Exception):
    pass

class Config(object):
    """
    Configuration parser for Armando main.conf format
    @author: Fabio "BlackLight" Manganiello <blacklight86@gmail.com>
    """

    ######
    # Private methods
    ######

    def __parse_rc_file(self, rcfile):
        parser = SafeConfigParser()

        try:
            parser.readfp(open(rcfile))
        except Exception as e:
            raise e

        for section in parser.sections():
            if parser.has_option(section, 'enabled') and parser.getboolean(section, 'enabled') is False:
                continue

            for key, value in parser.items(section):
                key = ('%s.%s' % (section, key)).lower()
                value = Constants.expand_value(value)
                self.config[key] = value

    def __init__(self, rcfile=None):
        """
        Configuration constructor taking as argument:
        rcfile -- Path string to the configuration file (default: __BASEDIR__/main.conf,
            which can be locally overridden by __PWD__/main.conf)
        """

        self.config = {}

        if rcfile is None:
            try:
                self.__parse_rc_file(Armando.get_base_dir() + os.sep + 'main.conf')
                self.__parse_rc_file(os.getcwd() + os.sep + 'main.conf')
            except FileNotFoundError as e:
                pass
        else:
            self.__parse_rc_file(rcfile)

        if len(self.config.items()) == 0:
            raise RuntimeError('No configuration has been loaded - both %s/main.conf and ./main.conf file were not found or are invalid' % Armando.get_base_dir())

    def get(self, attr):
        """
        Configuration getter
        attr -- Attribute name - note that we are case insensitive when it comes to attribute names
        """

        attr = attr.lower()
        if attr == 'speech.google_speech_api_key':
            return self.config[attr] if attr in self.config else os.getenv('GOOGLE_SPEECH_API_KEY')

        if attr not in self.config:
            return None

        return self.config[attr] if attr in self.config else None

    def dump(self):
        " Dump the configuration object in JSON format "
        return json.dumps(self.config)

# vim:sw=4:ts=4:et:

