# Smartish

## Connect everything to everything.

Smartish is a platform to connect custom events to custom actions, binding them together with your own Python scripts.

You can, for instance:

* Play/stop your music playback, using the MPD/Mopidy backend;
* Turn on/off the lights by using the Hue or the WeMo switch backends;
* Send a certain content to your Chromecast using the Chromecast backend.

All of this only:

* When you give a certain vocal command (see `Takk` submodule);
* When you shake your Wii controller (`Wii` submodule going to be imported soon);
* When you perform a certain hand gesture on your Leap Motion sensor (submodule Hu(g)eLeap going to be imported soon).

Each submodule is independent from the others and may require different dependencies,  but they all rely on the same backend and the same way to interact with events and actions, the same APIs, and the same way to manage, store and log data.

