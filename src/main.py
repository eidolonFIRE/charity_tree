from threading import Thread
from time import sleep
import signal

from strip import Strip

# from websocket_server import WebsocketServer



#================================================
#
#    SERVER
#
#------------------------------------------------

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


#================================================
#
#    MAIN / INIT
#
#------------------------------------------------
done = False
frame_rate = 120

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

signal.signal(signal.SIGINT, signal_handler)
print('Press (Ctrl+C, Enter) to exit or use cmd \"exit\"')

# server = WebsocketServer(12000, host="0.0.0.0")
# server.set_fn_message_received(serv_recvParser)
# serv_thread = Thread(target=server.run_forever, args=())
# serv_thread.start()

strips = [
    Strip(300, 18, 10, 0),
    Strip(300, 13, 11, 1),
]

jobRefresh = Thread(target=render, args=(strips,))
jobRefresh.start()


while not done:
    cmd = input(">")
    words = cmd.split()
    if len(words) > 0:
        if words[0] in ["quit", "exit"]:
            break
        if len(words) > 1:
        #     if words[0] == "start":
        #         start(words[1])
        #     if words[0] == "stop":
        #         stop(words[1])
            if words[0] == "solo":
                cmd_solo(strips, words[1])
            if words[0] == "fps":
                frame_rate = int(words[1])

done = True
