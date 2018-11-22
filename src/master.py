import slack_bot
from threading import Thread
import websockets
import asyncio
import os.path
from time import sleep

# load slaves from config
slaves = []
if os.path.isfile("../config/slaves.config"):
    print("Slaves:")
    for line in open("../config/slaves.config", "r"):
        if len(line):
            slaves.append(line)
            print("  %s" % line)
    print("")
else:
    print("Error: Please put slave IP's in \"config/slaves.config\"")
    exit()
print("Ready! Input your commands... \"exit\" to close.")


# send command to all slaves
async def send_cmd(cmd):
    for each in slaves:
        async with websockets.connect('ws://%s:12000' % each) as websocket:
            await websocket.send(cmd)


# callbacks from bots
def slack_callback(message, channel):
    print("slack mention..." + message)
    try:
        asyncio.new_event_loop().run_until_complete(send_cmd("pulse"))
    except:
        pass


# start all the workers
slack_thread = Thread(target=slack_bot.thread_run, args=(slack_callback,))
slack_thread.start()


# start default pattern
try:
    sleep(2)
    asyncio.get_event_loop().run_until_complete(send_cmd("twinkle"))
except:
    pass


# main holding loop
while True:
    cmd = input("")
    if cmd == "exit":
        break


# Kill everything
slack_bot.global_alive = False
