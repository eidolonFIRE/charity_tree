from subprocess import Popen, PIPE
from threading import Thread
from time import sleep
import signal

'''
    Agent that detects if git changes are needed and
    relaunches the code.
'''

global_done = False
force_restart = False
force_shutdown = False


def git_pull():
    # run the git update
    print("Git Pull!")
    pull = Popen(["git", "pull"], stdout=PIPE)
    pull.wait()


def git_check():
    # check if HEAD is behind remote master
    #     git rev-list HEAD...origin/master --count
    print("Checking git for updates...")
    git = Popen(["git", "fetch", "--dry-run"], stdout=PIPE, stderr=PIPE)
    (output, err) = git.communicate()
    # print("\t Result: ", output, err)
    git.wait()
    return True if len(err) > 2 else False


def thread_run_target():
    global global_done
    global force_restart
    global force_shutdown

    while not global_done:
        main = Popen(["python3", "main.py"], cwd="src/", stdout=PIPE, stdin=PIPE, stderr=PIPE)
        sleep(2)
        main.stdin.write(b'rainbow\n')
        alive = True
        while alive:
            # check if target is alive every 10 seconds
            sleep(5)

            # watch for restart flag
            if force_restart or force_shutdown:
                # request target shutdown
                print("Target stop requested.")
                main.stdin.write(b'exit\n')
                alive = False

        main.wait()

        if force_restart:
            git_pull()
            force_restart = False


def signal_handler(signal, frame):
    global global_done
    print("- INTERUPT - HALTING -")
    global_done = True


jobRefresh = Thread(target=thread_run_target)  # args=(x,)
jobRefresh.start()

signal.signal(signal.SIGINT, signal_handler)
print('Press (Ctrl+C, Enter) to exit or use cmd \"exit\"')

while not global_done:
    if git_check():
        print("Update needed.")
        force_restart = True

    # wait 1 minute
    sleep(20)

force_shutdown = True
global_done = True
