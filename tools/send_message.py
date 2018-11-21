import websockets
import asyncio
import os.path

# load slaves from config
slaves = []
if os.path.isfile("../slaves.config"):
    print("Slaves:")
    for line in open("../slaves.config", "r"):
        slaves.append(line)
        print("  %s" % line)
    print("")
else:
    print("Error: Please put slave IP's in \"slaves.config\"")
    exit()


print("Ready! Input your commands... \"exit\" to close.")


async def send_cmd(uri, cmd):
    async with websockets.connect(uri) as websocket:
        await websocket.send(cmd)

while True:
    cmd = input("")
    if cmd == "exit":
        break
    # send message to all slaves
    for each in slaves:
        asyncio.get_event_loop().run_until_complete(send_cmd('ws://%s:12000' % each, cmd))
