from threading import Thread
from time import sleep
import configparser
import os.path
from strip import Strip
from patterns.base import State
from websocket_server import WebsocketServer

#================================================
#
#    INIT / CONFIG
#
#------------------------------------------------
config = configparser.ConfigParser()
if os.path.isfile('../config/settings.ini'):
    config.read('../config/settings.ini')
else:
    print("Error: no \"config/settings.ini\" file. Use \"config/settings.ini.sample\" as template.")
    exit()
frame_rate = config.getint("global", "frame_rate")
auto_list = config.getboolean("global", "auto_list", fallback=True)
strips = [
    Strip(config.getint("strips", "strip_a_len"), 18, 10, 0),
    Strip(config.getint("strips", "strip_b_len"), 13, 11, 1),
]
global_alive = True


def render(strips):
    global global_alive
    global frame_rate

    while global_alive:
        for each in strips:
            each.step()
            sleep(0.5 / frame_rate)


def cmd_solo(strips, cmd):
    for each in strips:
        each.start_pattern(cmd)


def cmd_add(strips, cmd):
    for each in strips:
        each.start_pattern(cmd, False)


def cmd_stop(strip, cmd):
    for each in strips:
        for pat in each.active_pats:
            if pat.__class__.__name__ == cmd:
                pat.state = State.STOP
                break


def cmd_list(strips):
    print("")
    for index, strip in enumerate(strips):
        print("\n> Strip %d:" % index)
        for each in strip.active_pats:
            print("    {:15} : {:10}".format(each.__class__.__name__, each.state.name))
    print("")


def run_command(cmd):
    global strips
    global auto_list
    global frame_rate
    global global_alive

    words = cmd.split()
    if len(words) > 0:
        if words[0] in ["quit", "exit"]:
            global_alive = False
        elif words[0] == "fps":
            if len(words) > 1:
                frame_rate = int(words[1])
            else:
                print("Please provide a frame rate.\n    Example: \">fps 120\"")
        elif words[0] == "list":
            if len(words) > 1 and words[1] == "auto":
                if auto_list:
                    auto_list = False
                else:
                    auto_list = True
            cmd_list(strips)
        elif words[0] == "add":
            if len(words) > 1:
                cmd_add(strips, words[1])
        elif words[0] == "stop":
            if len(words) > 1:
                cmd_stop(strips, words[1])
        else:
            cmd_solo(strips, words[0])
    if auto_list:
        cmd_list(strips)


def serv_recvParser(client, server, msg):
    print(msg)
    run_command(msg)

#================================================
#
#    MAIN
#
#------------------------------------------------
print("Main: Use cmd \"exit\" to close.")

# main thread that updates patterns
jobRefresh = Thread(target=render, args=(strips,))
jobRefresh.start()

server = WebsocketServer(12000, host="0.0.0.0")
server.set_fn_message_received(serv_recvParser)
serv_thread = Thread(target=server.run_forever, args=())
serv_thread.start()

while global_alive:
    cmd = input("")
    run_command(cmd)

# kill everything
global_alive = False
server.shutdown()
