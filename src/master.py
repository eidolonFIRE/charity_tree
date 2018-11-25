import slack_bot
from threading import Thread
import websockets
import asyncio
import os.path
from time import sleep, time
from random import choice, uniform

# load slaves from config
slaves = []
if os.path.isfile("../config/slaves.config"):
    print("Slaves:")
    for line in open("../config/slaves.config", "r"):
        line = line.strip()
        if len(line) > 4:
            slaves.append(line)
            print("  %s" % line)
    print("")
else:
    print("Error: Please put slave IP's in \"config/slaves.config\"")
    exit()
print("Ready! Input your commands... \"exit\" to close.")

global_alive = True

pats_mild = [
    "twinkle",
    "wind",
    "water",
    "watercolor",
    "seasonal",
]

pats_medium = [
    "rainbow",
    "fairy",
    "candycane",
    "fire",
    "pixie",
]

pats_hot = [
    "rainbow2",
    "burst",
]

pats_one_off = [
    "bubbles",
    "pulse",
]

pats_kill = [
    "off",
    "fade_off",
]

pats_all = pats_mild + pats_medium + pats_hot



class Job():
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.start = None

job_stack = []


# send command to all slaves
async def _send_cmd(cmd):
    for each in slaves:
        async with websockets.connect('ws://%s:12000' % each) as websocket:
            await websocket.send(cmd)


def send_cmd(cmd):
    asyncio.new_event_loop().run_until_complete(_send_cmd(cmd))


# callbacks from bots
def slack_callback(message, channel):
    print("slack mention:" + message)
    try:
        asyncio.new_event_loop().run_until_complete(_send_cmd(choice(pats_one_off)))
    except:
        pass


def background_patterns():
    global global_alive
    global job_stack

    while global_alive:
        if len(job_stack) == 0:
            # nothing queued up!
            job_stack.append(Job(choice(pats_mild + pats_medium), uniform(10, 120)))

        top = job_stack[-1]

        if top.start == None:
            # start the next pattern
            top.start = time()
            send_cmd(top.name)
        else:
            if time() > top.start + top.duration:
                # pattern completed
                job_stack.pop()







# start all the workers
background_thread = Thread(target=background_patterns)
background_thread.start()

slack_thread = Thread(target=slack_bot.thread_run, args=(slack_callback,))
slack_thread.start()



# main holding loop
while global_alive:
    cmd = input("")
    if cmd == "exit":
        print("Master: HALT REQUESTED!")
        break

# Kill everything
global_alive = False
slack_bot.global_alive = False
