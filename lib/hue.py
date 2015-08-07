import re

from logger import Logger
from phue import Bridge

class Hue():
    """
    Plugin to interact with Philips Hue devices
    @author: Fabio "BlackLight" Manganiello <blacklight86@gmail.com>
    """

    def __init__(self, bridge, lightbulb=None):
        """
        bridge -- Name or IP address of the Philips Hue bridge host
        lightbulb -- Lightbulbs to act on - single lightbulb name or comma separated list.
            In case nothing is passed, the plugin will act on all the lightbulbs connected to the bridge
        """
        self.bridge_address = bridge
        self.lights_map = {}
        self.connected = False

        if lightbulb:
            m = re.split('\s*,\s*', lightbulb)
            self.lightbulbs = m if m else [lightbulb]

        Logger.get_logger().info({
            'msg_type': 'Hue bridge started',
            'bridge': self.bridge_address,
            'module': self.__class__.__name__,
            'lightbulbs': self.lightbulbs if lightbulb else None,
        })

    def connect(self):
        " Connect to the Philips Hue bridge "

        if self.connected:
            return

        Logger.get_logger().info({
            'msg_type': 'Connecting to the Hue bridge',
            'module': self.__class__.__name__,
        })

        self.bridge = Bridge(self.bridge_address)
        self.bridge.connect()
        self.bridge.get_api()

        Logger.get_logger().info({
            'msg_type': 'Connected to the Hue bridge',
            'module': self.__class__.__name__,
        })

        for light in self.bridge.lights:
            self.lights_map[light.name] = light

        if not hasattr(self, 'lightbulbs'):
            self.lightbulbs = []
            for light in self.bridge.lights:
                self.lightbulbs.append(light.name)

        self.connected = True

    def is_connected(self):
        " Return true if we are connected to the bridge "
        return self.connected

    def set_on(self, on):
        """
        Set the lightbulbs on status
        on -- If False, turn the lights off, otherwise turn them on
        """

        Logger.get_logger().info({
            'msg_type': 'Set lightbulbs on',
            'module': self.__class__.__name__,
            'on': on,
        })

        for light in self.lightbulbs:
            self.bridge.set_light(light, 'on', on)
            if on:
                self.bridge.set_light(light, 'bri', 255)

    def set_bri(self, bri):
        """
        Set the lightbulbs brightness
        bri -- Brightness value, in range [0-255]
        """

        Logger.get_logger().info({
            'msg_type': 'Set lightbulbs brightness',
            'module': self.__class__.__name__,
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

    def set_sat(self, sat):
        """
        Set the lightbulbs saturation
        sat -- Saturation value, in range [0-500]
        """

        Logger.get_logger().info({
            'msg_type': 'Set lightbulbs saturation',
            'module': self.__class__.__name__,
            'saturation': sat,
        })

        self.bridge.set_light(self.lightbulbs, 'sat', sat)

    def set_hue(self, hue):
        """
        Set the lightbulbs hue
        hue -- Hue/tint value, in range [0-65535]
        """

        Logger.get_logger().info({
            'msg_type': 'Set lightbulbs hue',
            'module': self.__class__.__name__,
            'saturation': hue,
        })

        self.bridge.set_light(self.lightbulbs, 'hue', hue)

