import os, socket, sys, threading, time
from __init__ import Armando

sys.path = [Armando.get_lib_dir()] + sys.path

from config import Config

class MpdServerMock(threading.Thread):
    """
    Mocks an MPD server for the predefined calls performed by unit tests
    @author: Fabio "BlackLight" Manganiello <blacklight86@gmail.com>
    """

    __header_str = 'OK MPD 0.19.0\n'
    __footer_str = 'OK\n\n'
    __track = {
        'file': 'spotify:track:79kQqGkJheGjmieG0qOhpu',
        'Time': '342',
        'Artist': 'Miles Davis',
        'Album': 'Amandla',
        'Title': 'Mr. Pastorius',
        'Date': '1989',
        'Track': '8',
        'Pos': '41',
        'Id': '84',
        'AlbumArtist': 'Miles Davis',
        'X-AlbumUri': 'spotify:album:0fabOosWong8kopy57JitO',
    }

    __status = {
        'volume': '100',
        'repeat': '0',
        'random': '0',
        'single': '0',
        'consume': '0',
        'playlist': '5',
        'playlistlength': '44',
        'xfade': '0',
        'song': '3',
        'songid': '90',
        'time': '82:286',
        'elapsed': '82.579',
        'bitrate': '160',
    }

    def __init__(self, rcfile=None):
        """
        Initialize the mock by using the MPD port specified in:
        rcfile -- Configuration file containing mpd.port (default: __TESTS_DIR__/conf/main.test.conf)
        """
        super(MpdServerMock, self).__init__()

        if rcfile is None:
            rcfile = Armando.get_tests_dir() \
                     + os.sep + 'conf' \
                     + os.sep + 'main.test.conf'

        self.__config = Config(rcfile)
        if self.__config.get('mpd.port') is not None:
            self.__port = int(self.__config.get('mpd.port'))
        else:
            raise AttributeError('The configuration file %s has no mpd.port setting' % rcfile)

        self.__state = 'stop'

    def __format_msg(self, msg):
        return self.__header_str + msg + self.__footer_str

    def __serve(self, sock, addr):
        request = sock.recv(1024).decode('utf-8').strip()
        if request == 'currentsong':
            sock.send(self.get_current_song().encode())
        elif request == 'status':
            sock.send(self.get_status().encode())
        elif request == 'play':
            self.__state = 'play'
            sock.send(self.__format_msg("").encode())
        elif request == 'pause':
            self.__state = 'pause'
            sock.send(self.__format_msg("").encode())
        elif request == 'stop':
            self.__state = 'stop'
            sock.send(self.__format_msg("").encode())
        elif request == 'quit':
            self.__state = 'quit'

        else:
            sock.send(self.__get_invalid_command_string(cmd=request))

    def __get_invalid_command_string(self, cmd):
        return u'%sACK [5@0] {} unknown command "%s"\n' % (self.__header_str, cmd)

    def get_current_song(self):
        response = ""
        if self.__state != 'stop':
            for key, value in self.__track.items():
                response += '%s: %s\n' % (key, value)
        # return ""
        return self.__format_msg(response)

    def get_status(self):
        response = ""
        self.__status['state'] = self.__state
        for key, value in self.__status.items():
            response += '%s: %s\n'
        return self.__format_msg(response)

    def run(self):
        self.__ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__ssock.bind(('127.0.0.1', self.__port))
        self.__ssock.listen(5)
        self.__ssock.settimeout(1)
        self.__sock_pool = []

        while True:
            try:
                (sock, addr) = self.__ssock.accept()
            except (socket.timeout, OSError) as e:
                self.stop()
                break

            self.__sock_pool.append(sock)
            server = threading.Thread(target=self.__serve, args=(sock, addr))
            server.start()

    def stop(self):
        if hasattr(self, '__sock_pool'):
            for s in self.__sock_pool:
                try:
                    s.close()
                except:
                    pass

        self.__ssock.close()

