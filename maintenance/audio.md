## Audio
This handles the creation of music tracks and sound effects, from walking and attacking to menu select and navigation noises.

### Music Mixer
This `class` handles the creation of background music used throughout the game in:
- Menu
- Combat
- Out of Combat
- Boss Battles

It has a function for each as follows: 
```python
def play_battle_theme(self):  
    self.battle_theme.set_volume(self.max_volume * self.volume / 100)  
    self.underworld_theme.set_volume(0)  
    self.menu_theme.set_volume(0)  
    self.boss_theme.set_volume(0)
```
When the function is called it sets the volume of the required song to be a percentage of the player's chosen music volume level. And then sets all other songs to be silent. New songs could therefore be added in the same way.

The remainder of the file is filled with noises for animations, which can easily be altered or extended to have new sound effects.

For example, the following deals with the moving of the cursor in the menu.
```python
def menu_move():  
    sound = pygame.mixer.Sound('./assets/audio/soundfx/weapon_sounds/sheathe_weapon.ogg')  
    sound.set_volume(0.3)  
    sound.play()
```

The footsteps function works slightly differently as it generates a random number, so that different footstep noises can be played. This is shown below:
```python
def play_footstep():  
    # play random footstep sound  
  rand_number = random.randint(0, 9)  
    footstep = pygame.mixer.Sound('./assets/audio/soundfx/footsteps/footstep0' + str(rand_number) + '.ogg')  
    footstep.set_volume(0.01)  
    footstep.play()
```