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

    __config = Config.get_config()
    __loggers = {}
    __loggers_lock = threading.RLock()
    __logs_ext = '.log'
    __default_log_format = '[%(asctime)-15s] %(message)s'

    @classmethod
    def __get_logfile_name(cls):
        return Armando.get_logs_dir() \
            + os.sep \
            + (cls.__config.get('logging.filename') or 'main.log')

    @classmethod
    def __get_loglevel(cls):
        loglevel = cls.__config.get('logger.loglevel').lower()
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

    @classmethod
    def __get_log_format(cls):
        logformat = cls.__config.get('logger.format')
        if not logformat:
            logformat = cls.__default_log_format
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
                cls.__loggers[classname] = Logger(
                    module_name=module_name,
                    loglevel=cls.__get_loglevel()
                )

            return cls.__loggers[classname]
        finally:
            cls.__loggers_lock.release()

    def __init__(self, module_name=None, loglevel=logging.INFO, format=None):
        """
        Logger constructor
        module_name -- Module to be logged (default: this module. Module
            information is part of the log records)
        loglevel -- Log level (default: logging.INFO)
        format -- Log format (default: __class__.__default_log_format)
        """
        self.module_name = module_name
        self.loglevel = loglevel
        self.logfile=self.__get_logfile_name()

        logging.basicConfig(
            filename = self.logfile,
            level = self.loglevel,
            format = format if format else Logger.__get_log_format()
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

