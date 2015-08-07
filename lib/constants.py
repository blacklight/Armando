from __init__ import Armando
import os

class ConstantExpanders(object):
    """
    Utilities for expanding constants in value strings
    @author: Fabio "BlackLight" Manganiello <blacklight86@gmail.com>
    """

    @classmethod
    def expand_base_dir(cls):
        " Expand Armando base directory "
        return Armando.get_base_dir()

    @classmethod
    def expand_tmp_dir(cls):
        " Expand Armando temporary directory "
        return cls.expand_base_dir() + os.sep + 'tmp'

    @classmethod
    def expand_lib_dir(cls):
        " Expand Armando lib directory "
        return cls.expand_base_dir() + os.sep + 'lib'

    @classmethod
    def expand_share_dir(cls):
        " Expand Armando share directory "
        return cls.expand_base_dir() + os.sep + 'share'

    @classmethod
    def expand_log_dir(cls):
        " Expand Armando logs directory "
        return cls.expand_base_dir() + os.sep + 'logs'

class Constants(object):
    """
    Class which exports the string value constants expansion method
    @author: Fabio "BlackLight" Manganiello <blacklight86@gmail.com>
    """

    __constants_func_map = {
        '__BASEDIR__'   : ConstantExpanders.expand_base_dir,
        '__TMPDIR__'    : ConstantExpanders.expand_tmp_dir,
        '__LIBDIR__'    : ConstantExpanders.expand_lib_dir,
        '__LOGSDIR__'   : ConstantExpanders.expand_log_dir,
        '__SHAREDIR__'  : ConstantExpanders.expand_share_dir,
    }

    @classmethod
    def expand_value(cls, value):
        """
        Expand the constants contained in a certain string value
        value -- The value which contains potential constant references to be expanded
        """
        for constant, expand_func in cls.__constants_func_map.items():
            print(expand_func)
            value = value.replace(constant, expand_func())
        return value

# vim:sw=4:ts=4:et:

