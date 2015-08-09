from __future__ import print_function
from config import Config
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
    Plugin to interact with speech recognition by using Google Speech Recognition API
    @depend: requests [pip install requests]
    @author: Fabio "BlackLight" Manganiello <blacklight86@gmail.com>
    """

    __config = Config.get_config()
    __logger = Logger.get_logger(__name__)
    __default_languages = ['en-us']

    def __init__(self):
        """
        self.api_key -- Google Speech Recognition API key, from config[speech.api_key]
            Instructions on how to get one: http://www.chromium.org/developers/how-tos/api-keys
        self.languages -- From config[speech.languages], comma-separated list of languages
        to use for speech detection. So far only the first language is supported, but @TODO
        use of secondary language(s) in case the confidence score reported by the API is below a certain threshold
        """

        self.api_key = SpeechRecognition.__config.get('speech.api_key')
        self.languages = SpeechRecognition.__config.get('speech.languages')

        if self.languages:
            self.languages = self.languages.split('\s*,\s*')
        else:
            self.languages = SpeechRecognition.__default_languages

        if not self.api_key:
            raise AttributeError('No Google speech recognition API key in ' \
                + 'your configuration on config[speech.api_key]. Instructions ' \
                + 'on how to get one: http://www.chromium.org/developers/how-tos/api-keys')


        SpeechRecognition.__logger.info({
            'msg_type': 'Initializing speech recognition backend',
            'api_key': '******',
            'languages': self.languages,
        })

    def recognize_speech_from_file(self):
        """
        Recognizes the speech contained in a FLAC audio file
        self.filename -- From config[audio.flac_file]
        """

        filename = SpeechRecognition.__config.get('audio.flac_file')
        if not filename:
            raise AttributeError('No audio.flac_file configuration option specified')

        SpeechRecognition.__logger.info({
            'msg_type': 'Google Speech Recognition API request',
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
            raise RuntimeError('Got an unexpected HTTP response %d from the server' % r.status_code)

        SpeechRecognition.__logger.info({
            'msg_type': 'Google Speech Recognition API response',
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

