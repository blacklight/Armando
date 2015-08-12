from __init__ import Armando
from config import Config

import json
import logging
import os
import threading

class Logger(object):
    """
    Interface to log Armando platform messages
    @author: Fabio "BlackLight" Manganiello <blacklight86@gmail.com>
    """

    __loggers = {}
    __loggers_lock = threading.RLock()
    __default_log_format = '[%(asctime)-15s] %(message)s'

    def __get_logfile_name(self):
        return Armando.get_logs_dir() \
            + os.sep \
            + (self.__config.get('logging.filename') or 'main.log')

    def __get_loglevel(self):
        loglevel = self.__config.get('logger.loglevel').lower()
        if loglevel == 'debug':
            return logging.DEBUG
        elif loglevel == 'info':
            return logging.INFO
        elif loglevel == 'warning':
            return logging.WARNING
        elif loglevel == 'error':
            return logging.ERROR
        else:
            raise AttributeError('Invalid log level option [%s] - valid values: [DEBUG, INFO, WARNING, ERROR]' \
                % loglevel)

    def __get_log_format(self):
        logformat = self.__config.get('logger.format')
        if not logformat:
            logformat = self.__default_log_format
        return logformat

    @classmethod
    def get_logger(cls, module_name=None):
        """
        Thread-safe singleton to access or initialize the static default logger object
        """
        if module_name is None:
            module_name = __name__

        cls.__loggers_lock.acquire()
        try:
            classname = module_name
            if not classname in cls.__loggers:
                cls.__loggers[classname] = Logger(module_name=module_name)

            return cls.__loggers[classname]
        finally:
            cls.__loggers_lock.release()

    def __init__(self, module_name=None):
        """
        Logger constructor
        module_name -- Module to be logged (default: this module. Module
            information is part of the log records)
        """
        self.__config = Config.get_config()

        self.module_name = module_name
        self.loglevel = self.__get_loglevel()
        self.logformat = self.__get_log_format()
        self.logfile = self.__get_logfile_name()

        logging.basicConfig(
            filename = self.logfile,
            level = self.loglevel,
            format = self.logformat
        )

    def log(self, msg, logfunc=logging.info):
        """
        Default log function
        msg -- Message to be logged, as a key-value dictionary. It will be logged in JSON format
        logfunc -- Function that will log msg (default: logging.info)
        """
        msg['module'] = self.module_name
        logfunc(json.dumps(msg))

    def debug(self, msg):
        " Debug logger function. msg must be a key-value dictionary, will be dumped as JSON "
        self.log(msg=msg, logfunc=logging.debug)

    def info(self, msg):
        " Info logger function. msg must be a key-value dictionary, will be dumped as JSON "
        self.log(msg=msg, logfunc=logging.info)

    def warning(self, msg):
        " Warning logger function. msg must be a key-value dictionary, will be dumped as JSON "
        self.log(msg=msg, logfunc=logging.warning)

    def error(self, msg):
        " Error logger function. msg must be a key-value dictionary, will be dumped as JSON "
        self.log(msg=msg, logfunc=logging.error)

# vim:sw=4:ts=4:et:

