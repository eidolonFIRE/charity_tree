from threading import Thread
from time import sleep
import configparser
import os.path
from strip import Strip
from patterns.base import State

done = False

# from websocket_server import WebsocketServer


# def serv_recvParser(cli, serv, msg):
#     print(msg)
#     solo(msg)


def render(strips):
    global done
    global frame_rate

    while not done:
        for each in strips:
            each.step()
            sleep(0.5 / frame_rate)


def cmd_solo(strips, cmd):
    for each in strips:
        each.start_pattern(cmd)


def cmd_add(strips, cmd):
    for each in strips:
        each.start_pattern(cmd, False)


def cmd_list(strips):
    print("")
    for index, strip in enumerate(strips):
        print("\n> Strip %d:" % index)
        for each in strip.active_pats:
            if each.state != State.OFF:
                print("    {:15} : {:10}".format(each.__class__.__name__, each.state.name))
    print("")


#================================================
#
#    INIT / CONFIG
#
#------------------------------------------------
config = configparser.ConfigParser()
if os.path.isfile('settings.ini'):
    config.read('settings.ini')
else:
    print("Error: no \"settings.ini\" file. Use \"settings.ini.sample\" as template.")
    exit()
frame_rate = config.getint("global", "frame_rate")
socket_mode = config.get("global", "mode")
print("Mode: %s" % socket_mode)

# server = WebsocketServer(12000, host="0.0.0.0")
# server.set_fn_message_received(serv_recvParser)
# serv_thread = Thread(target=server.run_forever, args=())
# serv_thread.start()

print("Use cmd \"exit\" to close.")

strips = [
    Strip(config.getint("strips", "strip_a_len"), 18, 10, 0),
    Strip(config.getint("strips", "strip_b_len"), 13, 11, 1),
]

auto_list = True


#================================================
#
#    MAIN
#
#------------------------------------------------

# main thread that updates patterns
jobRefresh = Thread(target=render, args=(strips,))
jobRefresh.start()

while not done:
    cmd = input("")
    words = cmd.split()
    if len(words) > 0:
        if words[0] in ["quit", "exit"]:
            done = True
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
        else:
            cmd_solo(strips, words[0])
    if auto_list:
        cmd_list(strips)

done = True
