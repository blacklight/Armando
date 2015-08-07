import json
import logging

class Logger():
    """
    Interface to log Armando platform messages
    @author: Fabio "BlackLight" Manganiello <blacklight86@gmail.com>
    """

    __logger = None

    @classmethod
    def create_static_logger(cls, logfile=None, loglevel='INFO'):
        """
        Method to initialize the class static logger
        logfile -- Path to the log file
        loglevel -- Log level string (default: INFO)
        """
        cls.__logger = Logger(logfile=logfile, loglevel=loglevel)
        return cls.__logger

    @classmethod
    def get_logger(cls):
        " Get the class static logger "
        return cls.__logger

    def __init__(self, logfile=None, loglevel='INFO'):
        if logfile is not None:
            self.logfile = logfile
        else:
            self.logfile = 'takk.log'

        if loglevel and loglevel.lower() == 'debug':
            self.loglevel = logging.DEBUG
        elif loglevel and loglevel.lower() == 'info':
            self.loglevel = logging.INFO
        elif loglevel and loglevel.lower() == 'warning':
            self.loglevel = logging.WARNING
        elif loglevel and loglevel.lower() == 'error':
            self.loglevel = logging.ERROR
        else:
            self.loglevel = logging.INFO

        logging.basicConfig(
            filename = self.logfile,
            level = self.loglevel,
            format = '[%(asctime)-15s] %(message)s'
        )

    def debug(self, msg):
        logging.debug(json.dumps(msg))

    def info(self, msg):
        logging.info(json.dumps(msg))

    def warning(self, msg):
        logging.warning(json.dumps(msg))

    def error(self, msg):
        logging.error(json.dumps(msg))

# vim:sw=4:ts=4:et:

