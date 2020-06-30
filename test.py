from shell import ShellThread
import queue

shared = {
    "running": True,
    "queue": queue.Queue()
}

x = ShellThread(shared)
x.start()

while True:
    if not shared["queue"].empty():
        msg = shared["queue"].get()
        print('msg received:', msg)