# A 5' 3d printed, glowing LED tree!

-----------------------

# Setup

## Linux
- Install pip for python 3 `sudo apt install python3-pip`
- Install pygame for python 3 `python3 -m pip install -U pygame --user`
- Create settings file. `cp src/settings.ini.sample src/settings.ini`

## OSX
- Install python3 `brew install python3`
- Install pygame `pip3 install pygame`
- Create settings file. `cp src/settings.ini.sample src/settings.ini`

## Setup for Raspberry Pi
- Install python3 `sudo apt install python3`
- clone and install this repo next to `charity_tree`. https://github.com/jgarff/rpi_ws281x.git
- Create settings file. `cp src/settings.ini.sample src/settings.ini`


# Running
It automatically detects if you are not on raspberry pi and will launch
pygame visualizer instead for pattern development and testing. 
<<<<<<< HEAD
=======
If you're running on raspberryPi, you will need to `sudo`.
>>>>>>> master

- Raspberry pi: `./python3 agent.py`
- Other: `./run.sh`


# Commands
- `fps <int>` : sets the running speed. Default 80.
- `exit` : Exit the program.
- `<pattern name>` : Entering a pattern name will launch that pattern.
- `off` : Starts the "off" pattern that turns off all leds.


# Adding new patterns
Patterns are automatically loaded from the `src/patterns/` directory.
To make a new pattern:
- `cp patterns/template.py patterns/mynewpattern.py`
- Set the class name to match the filename.
- That's it!
