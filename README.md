# 5' 3d printed, glowing LED tree!

---------------------

# Setup

## Linux
- `sudo apt install python3-pip`
- `python3 -m pip install numpy`
- `python3 -m pip install -U pygame --user`
- Create settings file. `cp src/settings.ini.sample src/settings.ini`

## OSX
- `brew install python3`
- `pip3 install pygame`
- Create settings file. `cp src/settings.ini.sample src/settings.ini`

## Setup for Raspberry Pi
- `sudo apt install python3`
- clone and install this repo next to `charity_tree`. https://github.com/jgarff/rpi_ws281x.git
- Create settings file. `cp config/settings.ini.sample config/settings.ini`
- Put slave IP's in `nano config/slaves.config`
- `pip3 install slackclient`

## All
- `pip3 install git+https://github.com/Pithikos/python-websocket-server`
- `pip3 install websocket-server`
- `pip3 install websockets`


# Running
It automatically detects if you are not on raspberry pi and will launch
pygame visualizer instead for pattern development and testing...

- Raspberry pi: `./python3 agent.py`
- Run on-off instance during dev: `./run.sh`
- Send messages directly: `python3 tools/send_message.py`


# Commands
- `fps <int>` : sets the running speed. Default 80.
- `exit` : Exit the program.
- `<pattern name>` : Entering a pattern name will launch that pattern.
- `off` : Starts the "off" pattern that turns off all leds.
- `add <pattern>` : Add a pattern to stack of active patterns.
- `stop <pattern>` : Trigger a pattern to stop.
- `list` : List all active_patterns.
- `list auto` : Toggle list being printed by default after every command. (default on)


# Adding new patterns
Patterns are automatically loaded from the `src/patterns/` directory.
To make a new pattern:
- `cp patterns/template.py patterns/mynewpattern.py`
- Set the class name to match the filename.
- That's it!
