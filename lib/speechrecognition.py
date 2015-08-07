from __future__ import print_function
from logger import Logger

import json
import os
import re
import requests

try:
    from urllib.parse import urlencode
except ImportError as e:
    from urllib import urlencode

class SpeechRecognitionError(Exception):
    pass

class SpeechRecognition():
    """
    @author: Fabio "BlackLight" Manganiello <blacklight86@gmail.com>
    """

    def __init__(self, api_key=None, languages=['en-us']):
        if not api_key:
            raise Exception('No Google speech recognition API key found in your configuration or GOOGLE_SPEECH_API_KEY environment variable')

        self.api_key = api_key
        self.languages = languages

        Logger.get_logger().info({
            'msg_type': 'Initializing speech recognition backend',
            'module': self.__class__.__name__,
            'api_key': '******',
            'languages': languages,
        })

    def recognize_speech_from_file(self, filename):
        Logger.get_logger().info({
            'msg_type': 'Google Speech Recognition API request',
            'module': self.__class__.__name__,
            'api_key': '******',
            'language': self.languages[0],
        })

        r = requests.post( \
            'http://www.google.com/speech-api/v2/recognize?' + urlencode({
                'lang': self.languages[0],
                'key': self.api_key,
                'output': 'json',
            }),

            data = open(filename, 'rb').read(),
            headers = {
                'Content-type': 'audio/x-flac; rate=44100',
            },
        )

        if not r.ok:
            raise Exception('Got an unexpected HTTP response %d from the server' % r.status_code)

        Logger.get_logger().info({
            'msg_type': 'Google Speech Recognition API response',
            'module': self.__class__.__name__,
            'response': r.text,
        })

        response = []
        for line in re.split('\r?\n', r.text):
            if re.match('^\s*$', line):
                continue
            response.append(json.loads(line))

        for item in response:
            if 'result' in item and len(item['result']):
                for _ in item['result']:
                    if 'final' in _:
                        if 'alternative' in _ and len(_['alternative']):
                            return _['alternative'][0]['transcript'], \
                                _['alternative'][0]['confidence'] if 'confidence' in _['alternative'][0] else 1

        raise SpeechRecognitionError('Speech not recognized')

# vim:sw=4:ts=4:et:

