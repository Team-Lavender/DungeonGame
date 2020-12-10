## Game

`game.py` handles the current state of the game and shouldn't be modified unless a new module is added to the game. In the `__init__` function, the game state is initialised along with all modules. Hence, any newly created modules that must interact with the game on a tick basis should be added here as well. 

It also checks for events in `check_events` and this behaves the same way as checking of events in any [PyGame](https://www.pygame.org/) game. 

`game_loop` is also self explanatory, this runs every game tick and does the calls to check if damage has been taken, what keys are being pressed, and whether the game has been paused. Care should be taken when editing this file especially, as careful consideration has gone into the ordering of function calls, so that everything functions as expected. If new modules are created that must interact with game state, add them into the game loop. 