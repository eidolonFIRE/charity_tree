from subprocess import Popen, PIPE
from threading import Thread
from time import sleep
import signal
import configparser
import os

'''
    Agent that detects if git changes are needed and
    relaunches the code.
'''

config = configparser.ConfigParser()
if os.path.isfile('config/settings.ini'):
    config.read('config/settings.ini')
else:
    print("Error: no \"config/settings.ini\" file. Use \"config/settings.ini.sample\" as template.")
    exit()
is_master = config.get("global", "mode").lower() == "master"
if is_master:
    print("--- MASTER ---")


# detect OS
is_rpi = False
os_type = " ".join(os.uname())
print("Current OS: %s" % os_type)
if "raspberrypi" in os_type:
    print("Loading on Raspberry pi")
    is_rpi = True


global_alive = True
force_restart_main = False
force_restart_master = False


def git_pull():
    # run the git update
    print("Pulling updates.")
    pull = Popen(["git", "pull"], stdout=PIPE, stderr=PIPE)
    pull.wait()


def git_check():
    # check if HEAD is behind remote master... git rev-list HEAD...origin/master --count
    print("Checking git for updates...")
    git = Popen(["git", "fetch", "--dry-run"], stdout=PIPE, stderr=PIPE)
    (output, err) = git.communicate()
    git.wait()
    return True if len(err) > 2 else False


def thread_run_main():
    global global_alive
    global force_restart_main
    global is_rpi

    while global_alive:
        main = Popen((["sudo"] if is_rpi else []) + ["python3", "main.py"], cwd="src/", stdin=PIPE)
        sleep(1)

        # starting command here...
        # main.stdin.write(b'twinkle\n')
        # main.stdin.flush()

        alive = True
        while alive:
            # check if target is alive every 10 seconds
            sleep(5)

            # watch for restart flag
            if force_restart_main or not global_alive or main.poll() is not None:
                # request target shutdown
                print("Main stop requested.")
                main.stdin.write(b'fade_off\n')
                main.stdin.flush()

                sleep(5)

                main.stdin.write(b'exit\n')
                main.stdin.flush()
                # main.stdin.close()
                alive = False

        main.wait()

        if force_restart_main:
            force_restart_main = False


def thread_run_master():
    global global_alive
    global force_restart_master

    while global_alive:
        main = Popen(["sudo", "python3", "master.py"], cwd="src/", stdin=PIPE)
        sleep(1)

        # starting command here...
        # main.stdin.write(b'rainbow\n')
        # main.stdin.flush()

        alive = True
        while alive:
            # check if target is alive every 10 seconds
            sleep(5)

            # watch for restart flag
            if force_restart_master or not global_alive or main.poll() is not None:
                # request target shutdown
                print("Master stop requested.")
                main.stdin.write(b'exit\n')
                main.stdin.flush()
                # main.stdin.close()
                alive = False
                sleep(10)

        main.wait()

        if force_restart_master:
            force_restart_master = False


def signal_handler(signal, frame):
    global global_alive
    print("- INTERUPT - HALTING -")
    global_alive = False


thread_main = Thread(target=thread_run_main)  # args=(x,)
thread_main.start()

sleep(10)

if is_master:
    thread_master = Thread(target=thread_run_master)  # args=(x,)
    thread_master.start()

signal.signal(signal.SIGINT, signal_handler)
print('Press (Ctrl+C, Enter) to exit or use cmd \"exit\"')

while global_alive:
    if git_check():
        print("Update needed.")
        git_pull()
        force_restart_main = True
        force_restart_master = True
        sleep(120)

    # wait 1 minute
    sleep(60)

global_alive = False
