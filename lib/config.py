try:
    from configparser import ConfigParser
except ImportError as e:
    from ConfigParser import SafeConfigParser as ConfigParser

from __init__ import Armando
from constants import Constants

import json
import os
import threading

class ConfigError(Exception):
    pass

class Config(object):
    """
    Configuration parser for Armando main.conf format
    @author: Fabio "BlackLight" Manganiello <blacklight86@gmail.com>
    """

    __config = None
    __config_lock = threading.RLock()

    ######
    # Private methods
    ######

    def __parse_rc_file(self, rcfile):
        parser = ConfigParser()
        with open(rcfile) as fp:
            parser.read_file(fp)

        for section in parser.sections():
            # Ignore sections having enabled = False
            if parser.has_option(section, 'enabled') and parser.getboolean(section, 'enabled') is False:
                continue

            # Case insensitive mapping - [logger]\nlevel=INFO in config becomes
            # self.config['logger.level'] = 'INFO'
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
        rcfile_found = False

        # If no rcfile is provided, we read __BASEDIR__/main.conf,
        # which can be overriden by your local share/YourProject/main.conf
        if rcfile is None:
            try:
                self.__parse_rc_file(Armando.get_base_dir() + os.sep + 'main.conf')
                rcfile_found = True
                self.__parse_rc_file(os.getcwd() + os.sep + 'main.conf')
            except EnvironmentError as e:
                # Ok guys, it can't be true that Python 3 supports
                # FileNotFoundError and Python 2 does not, and I have to use
                # EnvironmentError to be compatible with both. You guys have
                # COMPLETELY smashed the back compatibility and killed a great
                # programming language. I hate you from the bottom of my heart.
                if rcfile_found is False:
                    raise e
        else:
            self.__parse_rc_file(rcfile)

        if len(self.config.items()) == 0:
            raise RuntimeError( \
                'No configuration has been loaded - both %s/main.conf and ./main.conf files' \
                'were not found or are invalid' % (Armando.get_base_dir()))

    ######
    # Public methods
    ######

    @classmethod
    def get_config(cls):
        """
        Thread-safe singleton to access or initialize the static default configuration object
        """
        cls.__config_lock.acquire()
        try:
            if cls.__config is None:
                cls.__config = Config()
        finally:
            cls.__config_lock.release()
        return cls.__config

    def get(self, attr):
        """
        Configuration getter
        attr -- Attribute name - note that we are case insensitive when it comes to attribute names
        """
        attr = attr.lower()
        return self.config[attr] if attr in self.config else None

    def dump(self):
        " Dump the configuration object in JSON format "
        return json.dumps(self.config)

# vim:sw=4:ts=4:et:

