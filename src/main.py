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
# def start(name):
#     if name in allPats:
#         if patterns[allPats.index(name)][1].state != 2:
#             patterns[allPats.index(name)][0] = 1


# def stop(name, offMode):
#     if name in allPats:
#         if patterns[allPats.index(name)][1].state != 0:
#             patterns[allPats.index(name)][0] = 4 if offMode else 3


# def solo(name):
#     offMode = patterns[allPats.index(name)][1].full_stop
#     for key in allPats:
#         if key == name:
#             start(key)
#         else:
#             stop(key, offMode)


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
def render():
    global done

    strips = [
            Strip(300, 18, 10, 0),
            Strip(300, 13, 11, 1),
        ]
    while not done:
        for each in strips:
            each.step()
            sleep(1.0 / 200)


signal.signal(signal.SIGINT, signal_handler)
print('Press (Ctrl+C, Enter) to exit or use cmd \"exit\"')

# server = WebsocketServer(12000, host="0.0.0.0")
# server.set_fn_message_received(serv_recvParser)
# serv_thread = Thread(target=server.run_forever, args=())
# serv_thread.start()

jobRefresh = Thread(target=render, args=())
jobRefresh.start()


while not done:
    cmd = input(">")
    words = cmd.split()
    if len(words) > 0:
        if words[0] in ["quit", "exit"]:
            break
        # if len(words) > 1:
        #     if words[0] == "start":
        #         start(words[1])
        #     if words[0] == "stop":
        #         stop(words[1])
        #     if words[0] == "solo":
        #         solo(words[1])

done = True
