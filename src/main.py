from threading import Thread
from time import sleep
import signal
import configparser

from strip import Strip

# from websocket_server import WebsocketServer


# def serv_recvParser(cli, serv, msg):
#     print(msg)
#     solo(msg)


def signal_handler(signal, frame):
    # global serv_thread
    # global server
    # print("Exiting...")
    # server.server_close()
    # serv_thread.join()
    # sys.exit(0)
    global done
    done = True


def render(strips):
    global done
    global frame_rate

    while not done:
        for each in strips:
            each.step()
            sleep(1.0 / frame_rate)


def cmd_solo(strips, cmd):
    for each in strips:
        each.solo(cmd)


#================================================
#
#    INIT / CONFIG
#
#------------------------------------------------
config = configparser.ConfigParser()
config.read('settings.ini')
frame_rate = config.getint("global", "frame_rate")
socket_mode = config.get("global", "mode")
print("Mode: %s" % socket_mode)

signal.signal(signal.SIGINT, signal_handler)
print('Press (Ctrl+C, Enter) to exit or use cmd \"exit\"')

# server = WebsocketServer(12000, host="0.0.0.0")
# server.set_fn_message_received(serv_recvParser)
# serv_thread = Thread(target=server.run_forever, args=())
# serv_thread.start()

strips = [
    Strip(config.get("strips", "strip_a_len"), 18, 10, 0),
    Strip(config.get("strips", "strip_b_len"), 13, 11, 1),
]


#================================================
#
#    MAIN
#
#------------------------------------------------

# main thread that updates patterns
jobRefresh = Thread(target=render, args=(strips,))
jobRefresh.start()

done = False
while not done:
    cmd = input(">")
    words = cmd.split()
    if len(words) > 0:
        if words[0] in ["quit", "exit"]:
            done = True
        elif words[0] == "fps":
            if len(words) > 1:
                frame_rate = int(words[1])
            else:
                print("Please provide a frame rate.\n    Example: \">fps 120\"")
        else:
            cmd_solo(strips, words[0])

done = True
