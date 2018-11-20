"""
Sends commands to the LED strips.
Usage:
    python3 send_message.py '<command>'
"""


import websockets
import asyncio
import sys

async def send_message(uri, message):
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)

if __name__ == '__main__':
    message = sys.argv[1]
    asyncio.get_event_loop().run_until_complete(
        send_message('ws://localhost:12000', message)
    )
