import slack_bot
from threading import Thread
import websockets
import asyncio
import os.path
from time import sleep, time
from random import choice, uniform, randint
import donations

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
global_enabled = True
disabled_timestamp = 0
job_stack = []

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
    "fire",
]

pats_hot = [
    "pixie",
    "rainbow2",
    "burst",
    "candycane",
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

    def remaining(self):
        return (self.start + self.duration) - time()


# send command to all slaves
async def _send_cmd(cmd):
    for each in slaves:
        async with websockets.connect('ws://%s:12000' % each) as websocket:
            await websocket.send(cmd)
    # send command again just to be sure
    sleep(0.1)
    for each in slaves:
        async with websockets.connect('ws://%s:12000' % each) as websocket:
            await websocket.send(cmd)


def send_cmd(cmd):
    asyncio.new_event_loop().run_until_complete(_send_cmd(cmd))


def set_enabled(state):
    global global_enabled
    global_enabled = state


# callbacks from bots
def slack_callback(message, channel):
    global job_stack
    print("slack mention:" + message)

    # remote admin controll
    if "caleb says disable" in message:
        if any(x in message for x in ["half hour", "30min", "30 min", "1/2hr"]):
            disabled_timestamp = time() + 60 * 30
        else:
            disabled_timestamp = time() + 60 * 60
        set_enabled(False)
        sleep(1)
        try:
            asyncio.new_event_loop().run_until_complete(_send_cmd(choice(pats_kill)))
        except:
            pass
    elif "caleb says enable" in message:
        set_enabled(True)

    elif global_enabled:
        try:
            asyncio.new_event_loop().run_until_complete(_send_cmd(choice(pats_one_off)))
        except:
            pass


def email_callback(person, amount):
    print("{} made a donation of {}".format(person, amount))
    add_pattern(choice(pats_hot), 30)
    slack_bot.money_raised += float(amount.replace("$", ""))

    # save back to file
    file = open("../config/donations.save", "w")
    file.write("{:2.2f}               ".format(slack_bot.money_raised))
    file.close()


def add_pattern(name, duration):
    global job_stack
    # stop current job
    if len(job_stack) > 0 and job_stack[-1].start:
        # don't add duplicate
        if job_stack[-1].name == name:
            job_stack[-1].duration += duration
            return

        # see if job was close to done anyway
        if job_stack[-1].remaining() < 10:
            job_stack.pop()
        else:
            job_stack[-1].start = None

    # add new pattern
    job_stack.append(Job(name, duration))


def background_patterns():
    global global_alive
    global global_enabled
    global job_stack
    global last_pattern

    while global_alive:
        if global_enabled:
            if len(job_stack) == 0:
                # nothing queued up!
                add_pattern(choice(pats_mild + pats_medium), randint(60, 120))
            else:
                top = job_stack[-1]

                if top.start == None:
                    # start the next pattern
                    top.start = time()
                    send_cmd(top.name)
                else:
                    if top.remaining() <= 0:
                        # pattern completed
                        job_stack.pop()
        else:
            if time() > disabled_timestamp:
                global_enabled = True
                # jump start
                if len(job_stack):
                    job_stack[-1].start = None
        sleep(1)





# start all the workers
background_thread = Thread(target=background_patterns)
background_thread.start()

slack_thread = Thread(target=slack_bot.thread_run, args=(slack_callback,))
slack_thread.start()

email_thread = Thread(target=donations.thread_donations, args=(email_callback,))
email_thread.start()

# main holding loop
while global_alive:
    cmd = input("")
    if cmd == "exit":
        print("Master: HALT REQUESTED!")
        break

# Kill everything
global_alive = False
slack_bot.global_alive = False
donations.global_alive = False

sleep(1)
