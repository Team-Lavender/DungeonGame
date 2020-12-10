## Config

`config.py` holds, amongst other things, constant variables, denoted by capitals. For example, we can see `GAME_HEIGHT = 720` and `GAME_WIDTH = 1280`, these are the current game window values and can be changed, but we advise maintaining the same aspect ratio. 

### Getting Player Sprite
This file also deals with the retrieval of the required sprites for players, enemies, projectiles, weapons, etc. They function in the same way as one another, and the player is show below:

```python
def get_player_sprite(name, gender):  
	    return {"idle": [pygame.image.load("assets/frames/" + name + "_" + gender + "_idle_anim_f0.png"),  
						 pygame.image.load("assets/frames/" + name + "_" + gender + "_idle_anim_f1.png"),  
						 pygame.image.load("assets/frames/" + name + "_" + gender + "_idle_anim_f2.png"),  
						 pygame.image.load("assets/frames/" + name + "_" + gender + "_idle_anim_f3.png")],  
			    "run": [pygame.image.load("assets/frames/" + name + "_" + gender + "_run_anim_f0.png"),  
						 pygame.image.load("assets/frames/" + name + "_" + gender + "_run_anim_f1.png"),  
						 pygame.image.load("assets/frames/" + name + "_" + gender + "_run_anim_f2.png"),  
						 pygame.image.load("assets/frames/" + name + "_" + gender + "_run_anim_f3.png")],  
			    "hit": [(colorize(pygame.image.load("assets/frames/" + name + "_" + gender + "_hit_anim_f0.png"), WHITE))]}
```

The adding of new sprites should follow the same naming conventions for .png file names. 

### Colours
A number of colour constants are also held in `config.py` and are shown below. They can be altered by changing the RGB values, or entirely new colours could be added.

```python
BLACK = (0, 0, 0)  
WHITE = (255, 255, 255)  
RED = (255, 0, 0)  
LIGHT_RED = (161, 0, 0)  
GREEN = (71, 209, 51)  
GOLD = (250, 203, 62)  
FOV_COLOR = (255, 255, 255)  
DARK = (65, 65, 90)  
PINK = (255, 0, 127)  
BLUE = (0, 172, 238)
```