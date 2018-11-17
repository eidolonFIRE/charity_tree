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


def git_pull():
    # run the git update
    pull = Popen(["git", "pull"])
    (output, err) = pull.communicate()
    if err:
        print("Error during git pull.")
    pull.wait()


def git_check():
    # check if HEAD is behind remote master
    git = Popen(["git", "rev-list", "HEAD...origin/master", "--count"], stdout=PIPE)
    (output, err) = git.communicate()
    if err:
        print("Error checking git for updates.")
    git.wait()
    return int(output)


def thread_run_target():
    global global_done
    global force_restart

    while not global_done:
        main = Popen(["python3", "main.py"], cwd="src/", stdout=PIPE)
        alive = True
        while alive:
            # check if target is alive every 10 seconds
            sleep(10)
            (output, err) = main.communicate()
            if err:
                print("Target crashed!")
                alive = False

            # watch for restart flag
            if force_restart:
                # request target shutdown
                print("Restart requested.")
                (output, err) = main.communicate("exit", 10)
                if err:
                    print("Timeout waiting on \"exit\" command. Proceeding.")
                alive = False

        main.wait()

        if force_restart:
            git_pull()
            force_restart = False


def signal_handler(signal, frame):
    global global_done
    global_done = True


jobRefresh = Thread(target=thread_run_target)  # args=(x,)
jobRefresh.start()

signal.signal(signal.SIGINT, signal_handler)
print('Press (Ctrl+C, Enter) to exit or use cmd \"exit\"')

while not global_done:
    if git_check():
        force_restart = True

    # wait 1 minute
    sleep(30)

force_restart = True
global_done = True
