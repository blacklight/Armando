import re
import threading

from config import Config
from logger import Logger
from phue import Bridge

class Hue(object):
    """
    Plugin to interact with Philips Hue devices
    @author: Fabio "BlackLight" Manganiello <blacklight86@gmail.com>
    @depend: Philips Hue phue Python bridge [pip install phue]
    """

    __hue = None
    __hue_lock = threading.RLock()

    def __init__(self, lightbulbs=None):
        """
        bridge -- Name or IP address of the Philips Hue bridge host
        lightbulbs -- Lightbulbs to act on - single lightbulb name or comma separated list.
            In case nothing is passed, the plugin will act on all the lightbulbs connected to the bridge
        """
        self.__config = Config.get_config()
        self.__logger = Logger.get_logger(__name__)

        self.bridge_address = self.__config.get('hue.bridge')
        self.lightbulbs = self.__config.get('hue.lightbulbs')
        self.connected = False

        if self.lightbulbs:
            m = re.split('\s*,\s*', self.lightbulbs)
            self.lightbulbs = m or [self.lightbulbs]

        self.__logger.info({
            'msg_type': 'Hue bridge started',
            'bridge': self.bridge_address,
            'lightbulbs': self.lightbulbs or None,
        })

    @classmethod
    def get_hue(cls):
        """
        Static helper used for rules.xml <action> tags of type Python, which are run through eval().
        Thread-safe singleton to access or initialize the static default hue object
        """
        cls.__hue_lock.acquire()
        try:
            if cls.__hue is None:
                cls.__hue = Hue()
        finally:
            cls.__hue_lock.release()
        return cls.__hue

    def connect(self):
        " Connect to the Philips Hue bridge "

        if self.connected:
            return

        self.__logger.info({
            'msg_type': 'Connecting to the Hue bridge',
        })

        self.bridge = Bridge(self.bridge_address)
        self.bridge.connect()
        self.bridge.get_api()

        if not self.lightbulbs:
            self.lightbulbs = []
            for light in self.bridge.lights:
                self.lightbulbs.append(light.name)

        self.__logger.info({
            'msg_type': 'Connected to the Hue bridge',
            'lightbulbs': self.lightbulbs,
        })

        self.connected = True
        return self

    def is_connected(self):
        " Return true if we are connected to the bridge "
        return self.connected

    def set_on(self, on):
        """
        Set the lightbulbs on status
        on -- If False, turn the lights off, otherwise turn them on
        """

        self.__logger.info({
            'msg_type': 'Set lightbulbs on',
            'on': on,
        })

        for light in self.lightbulbs:
            self.bridge.set_light(light, 'on', on)
            if on:
                self.bridge.set_light(light, 'bri', 255)
        return self

    def set_bri(self, bri):
        """
        Set the lightbulbs brightness
        bri -- Brightness value, in range [0-255]
        """

        self.__logger.info({
            'msg_type': 'Set lightbulbs brightness',
            'brightness': bri,
        })

        if bri == 0:
            for light in self.lightbulbs:
                self.bridge.set_light(light, 'on', False)
        else:
            for light in self.lightbulbs:
                if not self.bridge.get_light(light, 'on'):
                    self.bridge.set_light(light, 'on', True)

        self.bridge.set_light(self.lightbulbs, 'bri', bri)
        return self

    def set_sat(self, sat):
        """
        Set the lightbulbs saturation
        sat -- Saturation value, in range [0-500]
        """

        self.__logger.info({
            'msg_type': 'Set lightbulbs saturation',
            'saturation': sat,
        })

        self.bridge.set_light(self.lightbulbs, 'sat', sat)
        return self

    def set_hue(self, hue):
        """
        Set the lightbulbs hue
        hue -- Hue/tint value, in range [0-65535]
        """

        self.__logger.info({
            'msg_type': 'Set lightbulbs hue',
            'saturation': hue,
        })

        self.bridge.set_light(self.lightbulbs, 'hue', hue)
        return self

# vim:sw=4:ts=4:et:

