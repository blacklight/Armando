import hashlib
import json
import time
import traceback
import urllib
import xml.dom.minidom

from config import Config
from logger import Logger

class LastFM(object):
    """
    Plugin for managing Last.FM interaction
    @author: Fabio "BlackLight" Manganiello <blacklight86@gmail.com>
    """

    __default_max_attempts = 5

    def __init__(self):
        """
        self.api_key -- From config[lastfm.api_key]
        self.api_secret -- From config[lastfm.api_secret]
        self.session_key -- From config[lastfm.session_key]
        self.max_attempts -- From config[lastfm.max_attempts] or 5
        """
        self.__config = Config.get_config()
        self.__logger = Logger.get_logger(__name__)

        self.api_key = self.__config.get('lastfm.api_key')
        self.api_secret = self.__config.get('lastfm.api_secret')
        self.session_key = self.__config.get('lastfm.secret_key')
        self.max_attempts = self.__config.get('lastfm.max_attempts') or self.__default_max_attempts

        (self.api_key and self.api_secret and self.sessionKey) \
            or raise AttributeError('[lastfm.api_key], [lastfm.api_secret] and' \
            '[lastfm.secret_key] must all be specified in your configuration')

    def __get_api_signature(self, method, args = {}) :
        signature = ('api_key%s' % self.api_key)
        args['method'] = method

        for name in sorted(args.iterkeys()):
            signature += '%s%s' % (name, args[name])
        signature += self.api_secret
        return hashlib.md5(signature).hexdigest()

    def api_call(self, method, args = {}):
        args['sk'] = self.session_key
        args['api_sig'] = self.__get_api_signature(method, args)
        args['api_key'] = self.api_key
        args['method'] = method
        stop_trying = False
        attempts = 0

        while stop_trying is False:
            www = urllib.urlopen('http://ws.audioscrobbler.com/2.0/', data = urllib.urlencode(args))
            response = www.read()
            attempts += 1

            try:
                document = xml.dom.minidom.parseString(response)
                errors = document.getElementsByTagName('error')

                if len(errors) > 0:
                    code = int(errors[0].getAttribute('code'))
                    self.__logger.error({
                        'msg_type'  : 'Error while invoking Last.FM API',
                        'method'   : method,
                        'args'     : json.dumps(args),
                        'code'     : code,
                        'response' : response
                    })

                    if code == 16: # Try again
                        time.sleep(1)
                        continue
                    else:
                        stop_trying = True
                else:
                    self.__logger..info({
                        'msg_type'  : 'API call succeeded',
                        'method'   : method,
                        'args'     : json.dumps(args),
                        'attempts' : attempts,
                    })

                    stop_trying = True
                    break
            except Exception as e:
                tb = traceback.format_exc()
                self.__logger..error({
                    'msg_type'   : 'Error while parsing server response',
                    'method'    : method,
                    'args'      : args,
                    'response'  : response,
                    'exception' : str(e),
                    'traceback' : tb,
                })

                if attempts < self.max_attempts:
                    time.sleep(1)
                    continue
                else:
                    stop_trying = True
            finally:
                if stop_trying and attempts >= self.max_attempts:
                    self.__logger..info({
                        'msg_type'  : 'Giving up API call',
                        'attempts' : attempts,
                        'method'   : method,
                        'args'     : json.dumps(args),
                    })

