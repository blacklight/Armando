# Armando

## Connect everything to everything.

Armando is a platform to connect custom events to custom actions, binding them together with your own Python scripts.

You can, for instance:

* Play/stop your music playback, using the MPD/Mopidy backend;
* Turn on/off the lights by using the Hue or the WeMo switch backends;
* Send a certain content to your Chromecast using the Chromecast backend.

All of this only:

* When you give a certain vocal command (see `Takk` project);
* When you shake your Wii controller (`Wii` project going to be imported soon);
* When you perform a certain hand gesture on your Leap Motion sensor (project Hu(g)eLeap going to be imported soon).

Each project is independent from the others and may require different dependencies,  but they all rely on the same backend and the same way to interact with events and actions, the same APIs, and the same way to manage, store and log data.

## Installation

* `git clone git@github.com:/BlackLight/Armando.git`
* `cd Armando`
* `git submodule init`
* `git submodule update`

All the projects are under `share/`. Each project may require different dependencies or a different configuration. Please rely on the `README.md` file inside of each folder.

## Configuration

All the configuration of the modules under `lib/` goes to `main.conf`. Copy `main.conf.example` to `main.conf` and modify it according to your needs.
Global `main.conf` configuration can be overridden by defining your own `main.conf` under `share/YourProject`.
Remember that the section name of the plugin in `main.conf` must be the same one of the module under `lib/` without the `.py` extension.

## Contribute

You can contribute with your own projects (folders under `share/` and executables under `bin/`, i.e. scripts which react on events performing actions defined by plugins) or plugins (under `lib/`, modules which allow you to interact with some specific Python-controllable device, e.g. Hue lightbulbs, music servers, SSH sessions, Chromecast devices, etc.).

* Do you wish to customize `Takk` to cast your favourite movie on the Chromecast when you say its name?

	* Add a Chromecast plugin named `chromecast.py` to `lib/`
	* Modify `Takk` configuration to invoke some of the public methods under its `Chromecast` class when a certain pattern in the vocal command is recognized.

* Do you wish to create a new script which performs some of the supported actions when your bluetooth smartphone pairs with your computer?

	* `git clone https://github.com/BlackLight/Armando.git`
	* `cd ./Armando/share`
	* `git submodule add https://github.com/yourname/YourProject.git`
	* Remember to use a `README.md` file to explain how to configure and use your script.
	* If needed, place an executable for running your script under `bin/`.

In both the cases, submit me a pull request and I'll be glad to include your code.

