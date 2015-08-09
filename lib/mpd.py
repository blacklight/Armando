from config import Config
from logger import Logger
from music import Track

import re
import socket

class MPD(object):
    """
    Plugin for managing the connection to MPD/Mopidy music server
    @author: Fabio "BlackLight" Manganiello <blacklight86@gmail.com>
    """

    __config = Config.get_config()
    __logger = Logger.get_logger(__name__)

    def __init__(self):
        """
        Class constructor.
        Reads mpd.host and mpd.port parameters from config
        """
        self.host = MPD.__config.get('mpd.host')
        self.port = int(MPD.__config.get('mpd.port'))

    def server_cmd(self, cmd):
        """
        Send a command to the server and return the response as an array of splitted lines
        """
        MPD.__logger.info({
            'msg_type': 'Sending command to MPD server',
            'cmd': cmd,
        })

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))

        try:
            sock.sendall(("%s\n" % cmd).encode())
            response = sock.recv(4096)

            if type(response).__name__ != 'str':
                # Broken compatibility between Python 2 and Python 3 :(
                response = response.decode()

            # End-of-message protocol for MPD
            while not re.search('\r?\nOK\r?\n\s*$', response):
                next_chunck = sock.recv(4096)
                if type(next_chunck).__name__ != 'str':
                    next_chunck = next_chunck.decode()
                response += next_chunck
        finally:
            sock.close()

        MPD.__logger.info({
            'msg_type': 'Received response from MPD server',
            'cmd': cmd,
            'response': response,
        })

        return response.split("\n")

    def get_current_track(self):
        """
        Get the current currently playing on MPD server, if any, as a Track object
        """
        currentsong = self.server_cmd('currentsong')
        status = self.server_cmd('status')
        track_info = {}

        for line in currentsong:
            m = re.match('^file:\s*(.*)$', line)
            if m:
                track_info['file'] = m.group(1) if len(m.group(1)) > 0 else None

            m = re.match('^Time:\s*(.*)$', line)
            if m:
                track_info['time'] = int(m.group(1)) if len(m.group(1)) > 0 else None

            m = re.match('^Artist:\s*(.*)$', line)
            if m:
                track_info['artist'] = m.group(1) if len(m.group(1)) > 0 else None

            m = re.match('^Title:\s*(.*)$', line)
            if m:
                track_info['title'] = m.group(1) if len(m.group(1)) > 0 else None

            m = re.match('^Album:\s*(.*)$', line)
            if m:
                track_info['album'] = m.group(1) if len(m.group(1)) > 0 else None

        for line in status:
            m = re.match('^state:\s*(.*)$', line)
            if m:
                track_info['state'] = m.group(1) if len(m.group(1)) > 0 else None

            m = re.match('^elapsed:\s*(.*)$', line)
            if m:
                track_info['elapsed'] = float(m.group(1)) if len(m.group(1)) > 0 else None

        if track_info['artist'] is None and track_info['title'] is not None:
            m = re.match('^(.+?) - (.+?)$', track_info['title'])
            if m:
                track_info['artist'] = m.group(1) if len(m.group(1)) > 0 else None
                track_info['title'] = m.group(2) if len(m.group(2)) > 0 else track_info['title']

        return Track(track_info)

