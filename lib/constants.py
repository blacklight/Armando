from __init__ import Armando
import os

class Constants(object):
    """
    Class which exports the string value constants expansion method
    @author: Fabio "BlackLight" Manganiello <blacklight86@gmail.com>
    """

    __constants_func_map = {
        '__BASEDIR__'   : Armando.get_base_dir,
        '__TMPDIR__'    : Armando.get_tmp_dir,
        '__LIBDIR__'    : Armando.get_lib_dir,
        '__LOGSDIR__'   : Armando.get_logs_dir,
        '__SHAREDIR__'  : Armando.get_share_dir,
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

