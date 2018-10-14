from ledlib.neopixel import *

from random import random
from random import shuffle
from threading import Thread
import sys
from time import sleep
from time import time
import signal

# from websocket_server import WebsocketServer

from patterns.off import Off
from patterns.rainbow import Rainbow
from patterns.candycane import Candycane
from patterns.classic import Classic
from patterns.wind import Wind
from patterns.tiwnkle import Twinkle
from patterns.fairy import Fairy
from patterns.water_color import WaterColor


#================================================
#
#    STATES / CONTROLS
#
#------------------------------------------------

# available catalog
patterns = [
    # event , func           , full stop ,
    [-1 , Off(300)        , 0] ,
    [1 , Rainbow(300)    , 1] ,
    [-1 , Candycane(300)  , 0] ,
    [-1 , Classic(300)    , 0] ,
    [-1 , Wind(300)       , 0] ,
    [-1 , Twinkle(300)    , 0] ,
    [-1 , Fairy(300)      , 0] ,
    [-1 , WaterColor(300) , 1] ,
]

allPats = [
    "off",
    "rainbow",
    "candycane",
    "classic",
    "wind",
    "twinkle",
    "fairy",
    "watercolor",
]


#================================================
#
#    SERVER
#
#------------------------------------------------
def start(name):
    if name in allPats:
        if patterns[allPats.index(name)][1].state != 2:
            patterns[allPats.index(name)][0] = 1


def stop(name, offMode):
    if name in allPats:
        if patterns[allPats.index(name)][1].state != 0:
            patterns[allPats.index(name)][0] = 4 if offMode else 3


def solo(name):
    offMode = patterns[allPats.index(name)][2]
    for key in allPats:
        if key == name:
            start(key)
        else:
            stop(key, offMode)


def serv_recvParser(cli, serv, msg):
    print(msg)
    solo(msg)


def signal_handler(signal, frame):
    global serv_thread
    global server
    print("Exiting...")
    server.server_close()
    serv_thread.join()
    sys.exit(0)


#================================================
#
#    MAIN / INIT
#
#------------------------------------------------


signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit')

# server = WebsocketServer(12000, host="0.0.0.0")
# server.set_fn_message_received(serv_recvParser)
# serv_thread = Thread(target=server.run_forever, args=())
# serv_thread.start()

strip = Adafruit_NeoPixel(300, 12, strip_type=ws.WS2811_STRIP_GRB)
strip.begin()
strip_order = range(strip.numPixels())
shuffle(strip_order)

while True:
    looptime = time()
    for idx in range(len(patterns)):
        if patterns[idx][1].state > 0:
            patterns[idx][1].step(strip)
        if patterns[idx][0] >= 0:
            if patterns[idx][0] == 1:  # turn on
                patterns[idx][1].state = 1
            elif patterns[idx][0] == 3:  # turn off (gentle)
                patterns[idx][1].state = 3
            elif patterns[idx][0] == 4:  # turn off (hard stop)
                patterns[idx][1].state = 0
                patterns[idx][1].clear()
            patterns[idx][0] = -1
    strip.show()

    delta = time() - looptime
    # print("%.4f"%(delta*40))
    if delta < 1.0/40:
        sleep(1.0/40 - delta)
