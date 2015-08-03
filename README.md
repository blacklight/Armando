# Smartish

## Connect everything to everything.

Smartish is a platform to connect custom events to custom actions, binding them together with your own Python scripts.

You can, for instance:

* Play/stop your music playback, using the MPD/Mopidy backend;
* Turn on/off the lights by using the Hue or the WeMo switch backends;
* Send a certain content to your Chromecast using the Chromecast backend.

All of this only:

* When you give a certain vocal command (see `Takk` project);
* When you shake your Wii controller (`Wii` project going to be imported soon);
* When you perform a certain hand gesture on your Leap Motion sensor (project Hu(g)eLeap going to be imported soon).

Each script is independent from the others and may require different dependencies,  but they all rely on the same backend and the same way to interact with events and actions, the same APIs, and the same way to manage, store and log data.

## Installation

* `git clone git@github.com:/BlackLight/Smartish.git`
* `cd Smartish`
* `git submodule init`
* `git submodule update`

All the scripts are under `share/`. Each script may require different dependencies or a different configuration. Please rely on the `README.md` file inside of each folder.

## Contribute

You can contribute with your own scripts (under `share/` and `bin/`, scripts react on events performing actions) or action sets (under `lib/`, modules which allow you to interact with some specific Python-controllable device, e.g. Hue lightbulbs, music servers, SSH sessions, Chromecast devices, etc.).

* Do you wish to customize Takk to cast your favourite movie on the Chromecast when you say its name? Add a Chromecast action set named `chromecast.py` to `lib/` and modify Takk configuration to invoke some of its methods when a certain pattern in the vocal command is recognized.

* Do you wish to create a new script which performs some of the supported actions when your bluetooth smartphone pairs with your computer? Clone this project. Clone your own script GitHub project into `share/` as a script (e.g. `git submodule add https://github.com/yourname/Yourscript`). Remember to use a `README.md` file to explain how to configure and use your script or script. Use the actions sets under `lib/` or add your own. Remember to place an executable for running your script under `bin/`.

In both the cases, submit me a pull request and I'll be glad to include your code.

