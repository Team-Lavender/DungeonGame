# pygame menu
# Docs: https://pygame-menu.readthedocs.io/en/latest/
# State machine: https://python-forum.io/Thread-PyGame-Creating-a-state-machine
# Pygame cheatsheet
# Pygame with states example: https://github.com/iminurnamez/pyroller/tree/master/data/states
# UIs: Main menu, pause menu, HUD?, Shop menu
from control import Control

class State(Control):
    # data which persist between all states
    # Example state vars: health, gold etc

    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None

    def switch_state(self):
        self.done = True
