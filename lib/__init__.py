import os, sys, inspect

class Armando(object):
    """
    Main class for Armando platform, which exports utility methods used either by Armando modules or custom subprojects
    @author: Fabio "BlackLight" Manganiello <blacklight86@gmail.com>
    """

    @classmethod
    def get_base_dir(cls):
        " Get the base directory of Armando project by searching for the .project.root file "
        return os.path.realpath( \
            os.path.dirname( \
                os.path.realpath(__file__) \
            ) + os.sep + '..'
        )

    @classmethod
    def get_logs_dir(cls):
        " Get logs directory "
        return os.path.realpath(cls.get_base_dir() + os.sep + 'logs')

    @classmethod
    def get_tmp_dir(cls):
        " Get tmp directory "
        return os.path.realpath(cls.get_base_dir() + os.sep + 'tmp')

    @classmethod
    def get_lib_dir(cls):
        " Get lib directory "
        return os.path.realpath(cls.get_base_dir() + os.sep + 'lib')

    @classmethod
    def get_share_dir(cls):
        " Get share directory "
        return os.path.realpath(cls.get_base_dir() + os.sep + 'share')

    @classmethod
    def get_tests_dir(cls):
        " Get tests directory "
        return os.path.realpath(cls.get_base_dir() + os.sep + 't')

    @classmethod
    def add_base_lib_dir_to_path(cls):
        """
        Add Armando platform base libdir to sys.path
        """

        libdir = cls.get_lib_dir()
        if libdir not in sys.path:
            sys.path.insert(0, libdir)

    @classmethod
    def initialize(cls):
        """
        Initialize Armando platform
        """

        cls.add_base_lib_dir_to_path()

