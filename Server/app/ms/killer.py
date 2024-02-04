import os
import signal

def kill_process(pid):
    os.kill(pid, signal.SIGTERM)
    exit()

