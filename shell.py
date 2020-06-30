
from threading import Thread

class ShellThread(Thread): 
    def __init__(self, shared):
        super().__init__(daemon=True)
        self.shared = shared

    def run(self):
        shell_running = True
        while shell_running:
            user_input = input('> ')
            if user_input == 'exit':
                shell_running = False
                self.shared["running"] = False
            else:
                self.shared["queue"].put(user_input)