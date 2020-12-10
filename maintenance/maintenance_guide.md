# Maintenance Guide

<h1 align="center">
  <br>
  <a href="https://github.com/Team-Lavender/DungeonGame"><img src="https://github.com/Team-Lavender/DungeonGame/blob/Revisions/assets/frames/title.png" alt="DungeonGame" width="500"></a>
</h1>

<h4 align="center">A challenging 2D roguelike game with a variety of enemies and exciting boss battles made entirely in <a href="https://www.pygame.org/" target="_blank">Pygame</a>.</h4>

<p align="center">
  <a href="https://docs.python.org/3.8/">
      <img src="https://img.shields.io/badge/python-3.8-blue.svg">
  </a>
</p>

<p align="center">
  <a href="#actor">Actor</a> •
  <a href="#audio">Audio</a> •
  <a href="#boss">Boss</a> •
  <a href="#boss-lookup">Boss Lookup</a> •
  <a href="#config">Config</a> •
  <a href="#consumable">Consumable</a> •
  <a href="#cutscene-and-cutscene-lookup">Cutscenes</a> •
  <a href="#dialogue">Dialogue</a> •
  <a href="#elemental-effects">Elemental Effects</a> •
  <a href="#enemy-and-enemy-lookup">Enemy and Enemy Lookup</a> •
  <a href="#entities">Entities</a> •
  <a href="#equipment-list">Equipment List</a> •
  <a href="#game">Game</a> •
  <a href="#item">Item</a> •
  <a href="#levelling">Levelling</a> •
  <a href="#magic">Magic</a> •
  <a href="#map">Map</a> •
  <a href="#menu">Menu</a> •
  <a href="#mob-drops">Mob Drops</a> •
  <a href="#npc-and-npc-lookup">NPC and NPC Lookup</a> •
  <a href="#projectile">Projectile</a> •
  <a href="#saving-and-loading">Saving and Loading</a> •
  <a href="#setup">Setup</a> •
  <a href="#shop">Shop</a> •
  <a href="#ui">Ui</a> •
  <a href="#weapon">Weapon</a>
</p>

## Actor
The `Actor` class is a super class for `Entity`, `Item`, `Projectile`, and `Magic` classes. It is extended to provide each of them with common attributes, such as sprites and a position. The `__init__` can be seen below:
```python
def __init__(self, game, pos_x, pos_y, sprite, state="idle"):  
    self.game = game  
    self.pos_x = pos_x  
    self.pos_y = pos_y  
    self.sprite = sprite  
    self.state = state  
    self.frame = 0  
	self.update_frame = 0  
    self.game.curr_actors.append(self)  
    self.flip_sprite = False  
  
  # makes actor untargetable by ai an changes sprite to transparent  
  self.invisible = False
```

There are two other functions, the first being `render` shown below, that renders an Actor's sprite at a given position. The second simply checks if an Actor can move in a given direction (whether the tile you're trying to walk though is a wall or other impassable object).
```python
def render(self):  
    frame_set = self.sprite[self.state]  
    anim_length = len(frame_set)  
    self.frame %= anim_length  
  
    if self.invisible:  
        curr_frame = config.colorize(frame_set[self.frame], config.DARK)  
    else:  
        curr_frame = frame_set[self.frame]  
    if self.update_frame == 0:  
        self.frame = (self.frame + 1) % anim_length  
    self.update_frame = (self.update_frame + 1) % 6  
  frame_rect = curr_frame.get_rect()  
    frame_rect.midbottom = (self.pos_x, self.pos_y)  
    if self.flip_sprite:  
        curr_frame = pygame.transform.flip(curr_frame, True, False)  
  
    if config.is_in_window(frame_rect[0], frame_rect[1]):  
        self.game.display.blit(curr_frame, frame_rect)
```
There should be no need to change this class.

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


## Boss
To extend/modify the current boss system either by changing the boss mechanics or adding new bosses the `boss.py` and  `boss_lookup.py` files must be accessed as follow:
- [Adding/modifying boss types.](#adding-modifying-boss-types)
-  [Adding new attack mechanics](#adding-new-attack-mechanics)
-  [Modifying the boss movement patterns and pattern finding algorithms.](#modifying-the-boss-movement-patterns-and-path-finding-algorithms)

### Adding modifying boss types
Each boss is structured as a separate class that inherits from the entity super class, each new boss must then be added in the `boss_lookup.py file` in the bosses dictionary, the modifiable attributes are as follows:
```python
bosses = {"boss":{'new_boss_name': [health, shield, level, move_speed, combat_style, ai_type, vision_radius, attack_radius, attack_damage, cooldown, drops{item_name: drop chance}]}}
```
Then in the class definition the entity super class is called as follows with the 'get_new_boss_sprite' replaced with the new boss sprite:
```python
super(GhostBoss, self).__init__(game, pos_x, pos_y, config.get_new_boss_sprite(boss_name), self.lookup[0], self.lookup[1], True, self.lookup[2], "alive", self.lookup[3])
```


### Adding new attack mechanics

After creating the function that handles the new attack, it must be added to the current_attack method so that the boss can call it when the turn for the attack comes up.
```python
elif self.curr_attack == new_attack_number:  
    self.state = "new_attack_name"  
	self.new_attack_method()  
    self.last_attack = pygame.time.get_ticks()
 `````` 
 
 If the added attack method is replacing an older method, then no further modifications are necessary, if the added method is on top of older methods then in the change_attack method the divider must be incremented  by the number of the added attack methods:
 ```python
 def change_attack(self):  
    if (self.curr_attack + 1) % 4 == 0:  # for example the number 4 must be incremented
        self.curr_attack = 1  
  else:  
        self.curr_attack += 1
 ```
If the added attack uses projectiles then a projectile object must be instantiated with the desired characteristics and attributes, the projectile sprite must be placed in the config file and follow the template as shown here:

```python
missile = projectile.Projectile(self.game, self.pos_x, self.pos_y,config.get_new_projectile_sprite(), self.special_damage, direction, projectile_type, True, 8):
```

### Modifying the boss movement patterns and path finding algorithms

Currently the boss file contains two movement behaviours, patrol and linear path. If new movement behaviours are to be added they need to be called from within the ai method and replace the `new_movement_pattern` function as such:


```python
def ai(self):  
      ......
        if self.ai_type == "patrol":  
            player = self.game.curr_actors[0]  
            if pygame.time.get_ticks() - self.last_attack >= self.cooldown and not player.invisible:  
                self.current_attack()   
            self.new_movement_pattern(direction)  
 ```

## Boss Lookup

This file contains all information about the bosses. This is shown below and the comment lays out the order of attributes. 


```python
# each boss has a list of attributes:  
# [health, shield, level, move_speed, combat_style, ai_type, vision_radius, attack_radius, attack_damage, cooldown, drops{item_name: drop chance}]  
bosses = {"boss": {"big_wizard": [3500, 0, 20, 1, "melee", "patrol", 500, 10, 15, 1500, {"coins": 70}],  
  
  "super_mage": [5000, 0, 30, 1, "melee", "patrol", 1000, 15, 15, 1000, {"coins": 100}],  
  
  "greenhead": [2000, 0, 10, 1, "melee", "patrol", 1000, 10, 15, 1000, {"coins": 150}]}}
```

If a new boss is to be added, they should be added the same way as the bosses above, this will ensure they exhibit the expected behaviour. Stats of current bosses can also be altered.

## Config

`config.py` holds, amongst other things, constant variables, denoted by capitals. For example, we can see `GAME_HEIGHT = 720` and `GAME_WIDTH = 1280`, these are the current game window values and can be changed, but we advise maintaining the same 16:9 aspect ratio. 

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

## Consumable

The `Consumable` class inherits from `Item` and handles the use of our three consumable potions, being health, shield and special bar boosts.

Below we can see the `__init__`, which deals with the type of potion, its name, stats from `equipment_list.py`, size, and visual effects.

```python
def __init__(self, game, name):  
    self.player = game.curr_actors[0]  
    self.name = name  
    self.stats = equipment_list.potions_list[name]  
    self.type = self.stats["type"]  
    self.size = self.stats["size"]  
    self.size *= (1 + self.player.entity_level // 5)  
    # get the sprite for the potion use animation  
    if self.type == "shield":  
        self.fx_sprite = config.get_potion_fx_sprite("shield_up")  
    elif self.type == "heal":  
        self.fx_sprite = config.get_potion_fx_sprite("heal_up")  
    elif self.type == "super":  
        self.fx_sprite = config.get_potion_fx_sprite("super_up")  
    self.fx_frame = 0  
    self.fx_update_frame = True  
    self.render_fx_on = False  
    self.used = False  
    self.consumed = False  
    self.is_throwable = False  
  
    super(Consumable, self).__init__(game, 0, 0,  
  config.get_potion_sprite(self.stats["sprite_name"]), self.stats["level"],  
  self.stats["cost"], "none")
```

This also handles the usage of these potions in the below function:
```python
def use(self):  
    if not self.used:  
        self.used = True  
	    # render fx, set fx_frame to start of animation  
  	    self.render_fx_on = True  
	    self.fx_frame = 0  
	    # play drink sound  
	    audio.drink_potion()  
        if self.type == "heal":  
            self.heal_up()  
            audio.heal_up()  
        elif self.type == "shield":  
            self.shield_up()  
            audio.shield_up()  
        elif self.type == "super":  
            self.super_up()  
            audio.super_up()
```
If a new consumable is added to the game, an `elif` statement should be added for its type to apply its related in-game effect, visual effects and audio on usage.

There should be no need to alter any other functions, but if adding new consumables a `'consumable_name'_up` function should be added, applying the required effects.


## Cutscene and Cutscene Lookup
The `CutSceneManager` class handles the actors' movements, dialogue and keeps track of the completed cutscenes to avoid the accidental triggering of the same cutscene multiple times . The cutscene triggers are stored as a map tile in  `map.py` and `mapframe.txt` while handling trigger points is done within the game loop in `game.py`. The exact waypoints and their accompanying dialogue are stored as a dictionary of dictionaries in `cutscene_lookup.py`. Extending or modifying cutscenes is a multistep process that requires navigating multiple files and functions as shown below:
- [The Cutscene update method](#cutscene-update)
-  [ Initializing the cutscene set in the map file ](#initializing-the-cutscene-set-in-the-map-file-and-map-frame)
-  [Adding the new cutscene scenario to the cutscene lookup.](#adding-the-cutscene-scenario-to-the-cutscene-lookup)
-  [Adding the cutscene to the game loop.](#adding-the-cutscene-to-the-game-loop)

### Cutscene update
The update function of the `CutSceneManager` class handles the cutscene execution steps. It is called when a cutscene has been triggered, with the cutscene number passed as an argument, the first thing that the update function does is to store the specific cutscene details from the cutscene_lookup dictionary as shown here:
```python
cutscene = cutscene_lookup_dict[cutscene_number]  
actors = self.game.curr_actors[self.game.get_npc_index()]  
waypoints = cutscene[self.scenario_index][1]  
i = self.game.get_npc_index()  
dialogue = cutscene[self.scenario_index][2]  
target = waypoints[self.waypoint_index]  
current_dialogue = dialogue[self.dialogue_index]
```
It then  computes the acceleration based on the position vector and the waypoint coordinates. As shown here:
```python
self.acc = (target - pos).normalize() * 0.5
```
and sets the actor's new position: 
```python
self.vel += self.acc  
if self.vel.length() > self.MAX_SPEED:  
    self.vel.scale_to_length(self.MAX_SPEED)  
pos += self.vel  
self.game.curr_actors[i].pos_x = pos[0]  
self.game.curr_actors[i].pos_y = pos[1]
```

 In order to synchronize the dialogue with the movement, the distance from the  actor to the next target is calculated, based on that the current dialogue index is incremented and the actor starts displaying the strings stored in the dialogue array of the `cutscene_lookup` file. It is worth mentioning that when the current scenario does not contain any dialogue the actor's speed does not slow down to make the sequence smoother. 
```python
if distance_vector_length < 100 :   
    if current_dialogue != '':  
        self.MAX_SPEED = 0.8  
  text = StaticText(self.game, WHITE)  
        text.display_text_dialogue(actors, current_dialogue)  
        pygame.display.update()  
    if distance_vector_length < 20:  
        self.MAX_SPEED = 2.5  
  self.waypoint_index += 1  
  self.dialogue_index += 1  
  target = waypoints[self.waypoint_index]
```

### Initializing the cutscene set in the map file and map frame
To add a new cutscene a set needs to be created where the coordinates of the specific cutscene flag are stored. Below is a subset of the current cutscene sets already in the game
```python
self.cutscene_1 = set()  
self.cutscene_2 = set()  
self.cutscene_3 = set()  
self.cutscene_4 = set()
```
Following that a `patch` that hasn't been used before must be selected, this will work as the trigger for the cutscene. After the selection and inclusion of the patch to the `mapframe.txt` file it will need to be added to its specific set. Here's an example from the existing cutscenes:
```python
elif patch == '+':  
    self.cutscene_1.add((x + self.map_offset[0], y + self.map_offset[1]))  
    self.cutscenes.add((x + self.map_offset[0], y + self.map_offset[1]))  
elif patch == '*':  
    self.cutscene_2.add((x + self.map_offset[0], y + self.map_offset[1]))  
    self.cutscenes.add((x + self.map_offset[0], y + self.map_offset[1]))
```


### Adding the cutscene scenario to the cutscene lookup

The cutscene lookup stores cutscene details,  the new cutscene details must then have the following format:
```python
cutscene_lookup_dict = {  
    cutscene_number: {cutscene_sequence: [[actor_index], [waypoints], [dialogye]]}
    }  
	  
 ```
 
### Adding the cutscene to the game loop
Within `game.py` the function  `get_cutscene()` is being called in the game loop to check if the player's current position matches a cutscene's coordinates in the map, if so it sets the cutscene number to its appropriate value and changes the cutscene trigger to true, any new cutscene will need to be added here as follows:

```python
elif player_pos in self.curr_map.cutscene_2:  
    if 2 not in completed:  
        self.current_cutscene = 2  
  self.cutscene_trigger = True
 ```

## Dialogue

The `StaticText` class handles the rendering of all text displayed by the actors from the player to enemies and NPCs. The text font is retrieved from the `game.py` file for consistency. There should be no need to change other functionality in this class as the text, colour, and targeted actor parameters are set when the `StaticText` object is created and through the `display_text_dialogue` method.

The text colour is set when the class is instantiated as shown here in the class constructor with a fixed offset 
```python
def __init__(self, game, color)  
    self.game = game  
    self.offset_x = -14    
	self.offset_y = -45  
	self.color = color  
    self.font = pygame.font.Font(self.game.font_name, 25)  
    self.coordinates = (0, 0)
```

 The displayed text and target actor are passed to the `display_text_dialogue`.

```python
def display_text_dialogue(self, actor, text)  
    self.coordinates = (actor.pos_x + self.offset_x, actor.pos_y + self.offset_y)  
    screen_text = self.font.render(text, True, self.color)  
    pos = screen_text.get_rect(center=(actor.pos_x, actor.pos_y - 34))  
    self.game.window.blit(screen_text, pos)
```

## Elemental Effects
`elemental_effects.py` contains classes for the elemental effects in the game, such as acid pools and explosions. This allows for easy creation of hazardous surfaces and the like. These effects are added when their constructor is called and removed from the game when their time limit expires. This allows for flexible usage, such as in throwables and projectile on hit effects.

### Adding new elements
To create a new elemental effect, a new elemental class must be created with its own render method called when it activates. This method should be called when the effect is instantiated in its `__init__` function and the effect added to the games list of elemental effects in the game. The `render` method provides the functionality to remove the effect after its animation plays out.
 ```python
class Explosion:
    def __init__(self, game, damage, size, pos_x, pos_y):
        self.game = game
        self.damage = damage
        self.size = size
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.sprite = config.get_magic_sprite("explosion")["idle"]
        # height is size times 2 times a cell width
        self.height = self.size * 16 * 2
        self.width = self.height * 114 / 64 # aspect ratio of explosion
        self.frame = 0
        self.update_frame = 0
        self.rendering = True
        self.explosion()
        self.game.elemental_surfaces.append(self)

    def explosion(self):
        for actor in self.game.curr_actors:
            if isinstance(actor, Entity):
                if abs(actor.pos_x - self.pos_x) <= self.width / 2 and abs(
                        actor.pos_y - self.pos_y) <= self.height / 2:
                    actor.take_damage(self.damage)
        audio.explosion()

    def render(self):

        frames = self.sprite
        anim_length = len(frames)

        # render animation if it exists
        if frames is not None:
            curr_frame = frames[self.frame]
            curr_height = curr_frame.get_height()
            curr_frame = pygame.transform.scale(curr_frame, (round(curr_frame.get_width() * self.height / curr_height), round(self.height)))
            frame_rect = curr_frame.get_rect()
            frame_rect.center = (self.pos_x, self.pos_y)
            self.game.display.blit(curr_frame, frame_rect)

        if self.update_frame == 0:
            self.frame = (self.frame + 1) % anim_length
        if self.frame == anim_length - 1:
            self.game.elemental_surfaces.remove(self)
```

## Enemy and Enemy Lookup
The `enemy` class deals with creation of hostile NPCs in the game. Creation of new enemy types should be performed by adding to the `enemy_lookup.py` file, where each enemy has a list of attributes: `[health, shield, level, move_speed, combat_style, ai_type, vision_radius, attack_radius, attack_damage, cooldown, drops{item_name: drop chance}, projectile]`

```python
enemies = {"demon": {"big_demon": [20, 20, 7, 0.7, "melee", "dumb", 200, 5, 3, 1000, {"coins": 3, "shield_large": 50}],
                     "imp": [5, 5, 3, 0.8, "melee", "dumb", 300, 16, 1, 1000, {"coins": 1, "heal_small": 70}],
                     "wogol": [10, 10, 5, 0.7, "ranged", "dumb", 300, 16, 2, 2000, {"coins": 1, "heal_small": 70}, "fireball"],
                     "chort": [10, 5, 3, 0.7, "ranged", "dumb", 300, 16, 1, 1000, {"coins": 1, "heal_small": 70}, "fireball"],
                     "chort_boss": [10, 5, 3, 0.7, "ranged", "dumb", 300, 16, 1, 1000, {}, "fireball"],
                     "dumb_chort": [1, 3, 3, 0.7, "melee", "tutorial", 200, 5, 1, 500, {"katana": 100 , "coins": 50, "heal_small": 100}, "fireball"],
                     "minionhead": [5, 5, 1, 0.8, "tentacles", "dumb", 1000, 16, 1, 1000, {"coins": 1, "acid_small": 70}, "tenticles"],
                     "minionhead_boss": [5, 5, 1, 0.8, "tentacles", "dumb", 1000, 16, 1, 1000, {}, "tenticles"]},
           "undead": {"big_zombie": [100, 100, 15, 0.7, "melee", "dumb", 200, 32, 10, 750, {"coins": 30, "shield_large": 50}],
                     "zombie": [50, 50, 1, 0.8, "melee", "dumb", 300, 16, 5, 1000, {"coins": 10, "shield_small": 70}],
                     "ice_zombie": [30, 10, 3, 0.7, "ranged", "dumb", 300, 16, 3, 3000, {"coins": 15, "heal_small": 70}, "split_arrow"],
                     "skelet": [10, 0, 2, 0.7, "ranged", "dumb", 300, 16, 5, 2000, {"coins": 10, "heal_small": 70}, "standard_arrow"]},
           "orc": {"ogre": [200, 200, 25, 0.7, "melee", "dumb", 200, 32, 15, 750, {"coins": 35, "shield_large": 50}],
                     "swampy": [50, 50, 20, 0.8, "melee", "dumb", 300, 16, 7, 1000, {"coins": 15, "heal_small": 70}],
                     "orc_shaman": [50, 10, 22, 0.7, "ranged", "dumb", 300, 16, 5, 3000, {"coins": 15, "heal_large": 70}, "acid"],
                     "orc_warrior": [30, 5, 20, 0.7, "ranged", "dumb", 300, 16, 3, 2000, {"coins": 15, "heal_small": 70}, "ricochet_arrow"]}}

```
adding a new enemy is as simple as filling in a new entry in this dictionary, specifying enemy type and name, where the name should be consistent with sprite name.

New enemy types should also be added to the `spawn_enemies` function in `game.py` file so they can be instantiated in the game.

There should be no need to change other functionality in this class as all enemy creation is handled through reference to `enemy_lookup`, to provide easy enemy generation.

## Entities

The main class in the file `Entity` inherits from `Actor` so as to inherit game positions and sprites. This can be seen in the `super` call. In the `__init__`, health, shields, level, and move speed, amongst other things, are initialised, as seen below:

```python
def __init__(self, game, pos_x, pos_y, sprite, health, shield, has_ai, entity_level, entity_status, move_speed):  
    super(Entity, self).__init__(game, pos_x, pos_y, sprite)  
    self.max_health = health  
    self.max_shield = shield  
    self.health = health  
    self.shield = shield  
    self.has_ai = has_ai  
    self.entity_level = entity_level  
    self.entity_status = entity_status  
    self.move_speed = move_speed  
    self.flip_sprite = False  
    self.is_hit = False  
    self.hit_damage = 0  
    self.last_hit = pygame.time.get_ticks()
```
If a new attribute, for example "invulnerable to poison", is required, it should be added here.

The `move` function handles movement of character and change of sprite direction. This should not be modified. 

`print_damage_numbers` also doesn't require further modification.

## Equipment List

Contains all information for weapons, potions, throwables and armour. At present, armour is assigned to a character from game start and cannot be bought or sold. 

```python
# AC is the amount of shielding provided. weight provides a movement penalty if strength is too low  
armor_list = {"chainmail": {"AC": 5, "weight": 5},  
			  "leather": {"AC": 2, "weight": 2},  
			  "none": {"AC": 0, "weight": 0}}
```

If a new weapon, armour, potion or throwable is to be added to the game, it should be added to the respective list. An example of the `weapons_list` is show. The same naming conventions should be followed so that UI and other aspects of the game can correctly render weapons. 

```python
# main stat: attribute must be 13 or greater to use this weapon, attribute adds bonus damage  
# dmg is base damage per hit  
# speed is number of attacks per second, gets bonus from dex  
# range is attack range in cells  
# crit_chance is percentage to do double damage, gets bonus from wis  
# type is the weapon type  
# cost is amount of gold to buy / sell  
  
# Part of the weapons list
weapons_list = {  
    "regular_sword": {"main_stat": "str", "dmg": 5, "speed": 1, "range": 2, "crit_chance": 15, "type": "melee",  
					  "cost": 5, "name": "Basic Sword"},  
  "knight_sword": {"main_stat": "str", "dmg": 10, "speed": 1, "range": 2, "crit_chance": 15, "type": "melee",  
				   "cost": 150, "name": "Knight Sword"},

# Part of the potions list
# potion_type: {sprite name, size, type, level, cost, name}  
potions_list = {"heal_small": {"sprite_name": "flask_red", "size": 2, "type": "heal", "level": 1, "cost": 5,  
			    "name": "Small Healing Potion"},
 
# Part of the potions list 
throwables_list = {  
    "explosive_small": {"sprite_name": "bomb_small", "element_size": 2, "damage": 20, "type": "explosive", "level": 1,  
					    "cost": 20, "name": "Small Bomb"},
```

Adding a new weapon, potion, armour or throwable is simple, but if you want to add a new class of items, an entirely new list should be created with the same naming conventions.

## Game

`game.py` handles the current state of the game and shouldn't be modified unless a new module is added to the game. In the `__init__` function, the game state is initialised along with all modules. Hence, any newly created modules that must interact with the game on a tick basis should be added here as well. 

It also checks for events in `check_events` and this behaves the same way as checking of events in any [PyGame](https://www.pygame.org/) game. 

`game_loop` is also self explanatory, this runs every game tick and does the calls to check if damage has been taken, what keys are being pressed, and whether the game has been paused. Care should be taken when editing this file especially, as careful consideration has gone into the ordering of function calls, so that everything functions as expected. If new modules are created that must interact with game state, add them into the game loop. 

## Item 

Item is a basic superclass which itself inherits from `Actor`. It simply provides items with a `level`, `cost` and `combat_style`. New attributes specific to items should be added here.

## Levelling
`levelling.py` contains the methods for levelling up the player character as well as applying the consequences for player death. `level_up` increases the player's level, incrementing their next xp target as well as increasing all of their stats by 1 level. The player health and shield are then recalculated along with their weapon damage for all of the items in their hotbar.
```python
def level_up(player, amount):
    if amount > 0:
        audio.level_up()
    player.xp = 0
    player.max_xp *= 1.05
    player.entity_level += amount
    player.strength += amount
    player.dexterity += amount
    player.constitution += amount * 2
    player.intellect += amount
    player.wisdom += amount
    player.charisma += amount

    bonuses = {"str": (player.strength - 10) // 2,
               "dex": (player.dexterity - 10) // 2,
               "con": (player.constitution - 10) // 2,
               "int": (player.intellect - 10) // 2,
               "wis": (player.wisdom - 10) // 2,
               "cha": (player.charisma - 10) // 2}

    player.max_health = 5 + player.entity_level + bonuses["con"]
    overshield = max(player.shield - player.max_shield, 0)
    player.max_shield = round(player.armor["AC"] * (1.005 * player.entity_level))
    player.health = player.max_health
    player.shield = player.max_shield + overshield
    if player.shield > 0:
        player.has_shield = True

    player.special_damage += amount * 5

    # update player weapon stats
    for weapon in player.items:
        if weapon is not None:
            weapon.attack_damage = equipment_list.weapons_list[weapon.name]["dmg"] + bonuses[
                equipment_list.weapons_list[weapon.name]["main_stat"]] + player.entity_level // 2
            weapon.attack_speed = 1 / max((equipment_list.weapons_list[weapon.name]["speed"] + (bonuses["dex"] / 2)),
                                          0.01)
            weapon.crit_chance = equipment_list.weapons_list[weapon.name]["crit_chance"] + (bonuses["wis"] * 2)
```

The death function sets the player back to the starting room, and they lose some of their gold and items as well as all their potions. They also lose a number of levels up to a maxiumum of 5, as long as this is not greater than their current level.

```python
# death has chance to lose player levels up to amount given,
# and items may be dropped based on chance to drop. all potions and throwables are lost.
def death(player, chance_to_drop, max_levels_lost):
    player.game.level = 1
    player.game.curr_map.current_map = 0
    player.game.change_map(1)
    player.xp //= (100 // chance_to_drop)
    player.money //= (100 // chance_to_drop)
    level_loss = random.randint(0, max_levels_lost)
    if level_loss >= player.entity_level:
        level_loss = 0
    level_up(player, -level_loss)
    for idx, item in enumerate(player.inventory):
        if item is not None:
            if item[-1] == "potion" or item[-1] == "throwable":
                # lose all potions
                player.inventory[idx] = None
            else:
                # chance to lose weapons
                roll_to_drop = random.randint(0, 101)
                if chance_to_drop >= roll_to_drop:
                    player.inventory[idx] = None
    # lose held potions
    player.potion_1 = []
    player.potion_2 = []
```

## Magic
The `magic.py` file contains classes for each spell that is not a projectile. currently this is just the lightning bolt spell. magic classes should contain a render method as well as a method to implement their functionality. for example for lighting, there is a `zap` method that makes the lightning jump between enemies:
```python
lass LightningBolt(Actor):
    def __init__(self, game, pos_x, pos_y, forks, damage, attack_range, direction, time):
        super(LightningBolt, self).__init__(game, pos_x, pos_y, config.get_magic_sprite("lightning"), state="idle")
        self.forks = forks
        self.damage = damage
        self.direction = direction
        self.direction.scale_to_length(attack_range)
        self.attack_range = attack_range
        self.time = time
        self.last_used = pygame.time.get_ticks()
        self.zap()

    def zap(self):
        if self.forks <= 0:
            return

        for actor in self.game.curr_actors:
            if isinstance(actor, Enemy):
                target_vector = pygame.Vector2(actor.pos_x - self.pos_x, actor.pos_y - actor.height // 2 - self.pos_y)
                if 0 < target_vector.length() <= self.attack_range:
                    angle = self.direction.angle_to(target_vector)
                    angle = angle % 360
                    angle = (angle + 360) % 360
                    if angle > 180:
                        angle -= 360
                    if abs(angle) <= 25:
                        self.direction = target_vector
                        self.direction.scale_to_length(target_vector.length())
                        actor.take_damage(self.damage)
                        audio.electricity_zap()
                        for next_actor in self.game.curr_actors:
                            if isinstance(next_actor, Enemy):
                                new_target_vector = pygame.Vector2(next_actor.pos_x - actor.pos_x,
                                                                   next_actor.pos_y - actor.pos_y)
                                if 0 < new_target_vector.length() <= self.attack_range:
                                    bolt = LightningBolt(self.game, actor.pos_x, actor.pos_y, self.forks - 1,
                                                         self.damage, new_target_vector.length(),
                                                         new_target_vector, self.time)
                                    next_actor.take_damage(self.damage // 2)
                                    self.game.curr_actors.append(bolt)
                                    break



    def render(self):

        if pygame.time.get_ticks() - self.last_used >= self.time:
            self.game.curr_actors.remove(self)
        frame_set = self.sprite[self.state]
        anim_length = len(frame_set)
        self.frame %= anim_length
        curr_frame = frame_set[self.frame]
        frame_rect = curr_frame.get_rect()

        scale = max(self.direction.length() / frame_rect[3], 0.1)

        frame_rect.center = (self.pos_x, self.pos_y)
        center = ((frame_rect.centerx + self.direction.normalize()[0] * scale * frame_rect[3] / 2),
                  (frame_rect.centery + self.direction.normalize()[1] * scale * frame_rect[3] / 2))
        if self.update_frame == 0:
            self.frame = (self.frame + 1) % anim_length
        self.update_frame = (self.update_frame + 1) % 4
        angle = self.direction.angle_to(pygame.Vector2(0, 1))
        curr_frame = pygame.transform.rotozoom(curr_frame, angle, scale)
        new_rect = curr_frame.get_rect()
        new_rect.center = center

        if config.is_in_window(center[0], center[1]):
            self.game.display.blit(curr_frame, new_rect)

```
Addition of new magic effects would be performed in a similar way, this works closely to the elemental effects in that the magic effect must be instantiated by a different class and then will be removed once its effect ends.


## Map
To extend/modify the current Map either by adding new tiles, new levels or changing room design and floor color the `map.py` file and other relative files must be accessed as follow:


- [Adding more tiles.](#adding-more-tiles)
- [Changing design of a room.](#changing-design-of-a-room)
- [Adding new game level.](#adding-new-game-level)
- [Changing floor color for each level.](#changing-floor-color-for-each-level)

### Adding more tiles 
Tiles are accessed through `mapframe.txt` under the `[tilesets]` section. Add the source path of new tiles here and call it from the constructor of class `Map`. 
To use the new tile, change the tile accessed in `draw_map`.
```python
    for x, y in self.symbol_set_name:  
        self.game.display.blit(self.floor_tile_tuple[0], (x * 16, y * 16))  
        self.game.display.blit(self.your_tile_name, (x * 16, y * 16))
```
If the new tile is indicated by new symbol in map, the symbol need to be identified. Add a new empty symbol set in `_init_` and `generate_map`. Then a condition is needed in `generate_map` to locate the tile position in map.
```python
    if patch == 'new symbol':  
	    self.your_tile_set.add((x + self.map_offset[0], y + self.map_offset[1]))  
	    self.unpassable.add((x + self.map_offset[0], y + self.map_offset[1]))
```

### Changing design of a room  
The size of room should be no more than **67*33**. Edit the specification of a room in corresponding file (Level 1: `mapframe.txt`, Level2: `mapframe2.txt`, Level 3: `mapframe2.txt`).
 - `w`: wall
 - `p`: plant
 - `t`: any object
 - `-`: floor
 - `.`: empty space
 - `L` + number: ladder to the lower map level
 - `H` + number: ladder to the higher map level
 - numbers: door to the room indicated
 

    ```
     wwwwwwwwwwwwwwwwwwwwwww..................wwwwwwwwwwwwwwwwwwwww  
     w------p--------------w..................w------------------w  
     w---------------------w..................w-------------------w  
     w---------------------w..................w-------------------w  
     w---------------------wwwwwwwwwwwwwwwwwwww-------------------w  
     w------------------------------------------------------------w  
     w------------------------------------------------------------w  
     w---------------------wwwwwwww---wwwwwwwww-------------------w  
     w---------------------w......w---w.......w-------------------w  
     w---------------------w......w---w.......w-------------------w  
     w---------------------w......w---w.......w-------------------w  
     wwwwwwwww------wwwwwwww......w---w.......wwwwwww------wwwwwwww  
     ........w------w.............w---w.............w------w.......  
     ........w------wwwwwwwwwwwwwww---wwwwwwwwwwwwwww------w.......  
     ........w---------------------------------------------w.......  
     ........w------wwwwwwwwwwwwwww---wwwwwwwwwwwwwww------w.......  
     ........w------w.............w---w.............w------w.......  
     wwwwwwwww------wwwwwwww......w---w.......wwwH2ww------wwwwwwww  
     w---------------------w......w---w.......w-------------------w  
     w-----t---------------w......w---w.......w---L1--------------w  
     w---------------------w......w---w.......w-------------------w  
     w---------------------wwwwwwww---wwwwwwwww-------------------w  
     w------------------------------------------------------------w  
     w------------------------------------------------------------w  
     w---------------------wwwwwwww10wwwwwwwwww-------------------w  
     w---------------------w..................w-------------------w  
     w---------------------w..................w-------------------w  
     wwwwwwwwwwwwwwwwwwwwwww..................wwwwwwwwwwwwwwwwwwwww```

### Adding a new game level
In order to add a new game level,  a new file named `mapframe[level_number].txt` must be created which will contain the  design of the rooms.  
To show the of the level in minimap, it's necessary to add an element in `map_list.py` to access the level file.
```python
Levels = {-1: "mapframe_tutorial.txt", 1: "mapframe.txt", 2: "mapframe2.txt", 3: "mapframe3.txt", your_level_number: "mapframe[level_number].txt"}
```
The level configuration can be created by stating the position of the doors. Each room must have two doors with the exception of the first and last rooms, which only have one door.

 - `D`: leading to the below room
 - `U`: leading to the upper room
 - `R`: leading to the right room
 - `L`: leading to the left room

```python
ROOMS = {-1:('D', 'UD'),  
  1:('D', 'UD', 'UD', 'UR', 'LU', 'DU', 'DU', 'DR', 'LD', 'UD', 'UD', 'UR', 'LU', 'DU', 'DU', 'D'),  
  2:('R', 'LD', 'UL', 'RD', 'UD', 'UR', 'LU', 'DR', 'LD', 'UR', 'LU', 'DU', 'DL', 'RU', 'DR', 'L'),  
  3:('R', 'LR', 'LD', 'UL', 'RL', 'RD', 'UD', 'UR', 'LU', 'DR', 'LD', 'UR', 'LU', 'DU', 'DU', 'D'),
  level_number: "Fill in the position of doors in the room"}
  ```
  

### Changing floor color for each level
To change the featured color of floor, modify the rgb value of the level in `set_color`.

   ```python 
   elif self.current_level == level_number:  
	   for tile in floor_tiles:  
	        tile.fill((r_value, g_value, b_value), special_flags=pygame.BLEND_RGBA_MULT)  
	        self.floor_tile_tuple = self.floor_tile_tuple + (tile,)
  ```


## Menu

The menu file contains the `Menu` super class and its subclasses:  `MainMenu`   `StartMenu ` `NewGameMenu ` `LoadGameMenu ` `OptionsMenu` `VolumeMenu ` `CreditsMenu ` `CharacterMenu ` `PauseMenu `  `InGameIntro `   `DeathMenu`.  

### Adding new options to the StartMenu
The `StartMenu` class handles the selection of the game mode, currently there are three options:  new game, load game and tutorial, if the game mode options are to be expanded then first it has to be added to the  `display_menu` function as follows:    (game mode or option)

```python
self.game.draw_text("new_game_mode", font, horizontal_position, vertical_position, font_color)
```
Then it need to be added to the `check_input` method which should handle all the users inputs when interacting with the new game mode in the tutorial as shown below for the "New Game" option:

```python
elif (self.game.DOWN_KEY or self.game.RIGHT_KEY):  
    audio.menu_move()  
    if self.state == "New Game":  
        self.state = "Tutorial"  
		  self.load_font_color = self.primary_font  
        self.new_font_color = self.primary_font  
        self.tutorial_font_color = self.secondary_font  
        self.cursor_rect.midtop = (self.tutorial_x + self.offset, self.tutorial_y)```
```

### Adding a new character to the character menu

Adding a new character to the character menu can be done simply by appending it to the   `character_classes` array  which will be used by the `display_menu`  function:

```python
self.character_classes = [("PALADIN", "knight"), ("RANGER", "elf"), ("MAGE", "wizzard"), ("ROGUE", "lizard")]
```

### Modifying the game intro

The game intro text is stored in the `IN_GAME_INTRO` variable and can be easily modified:
```python
self.IN_GAME_INTRO = '''
MANY YEARS AGO A PORTAL WAS OPENED TO THE DEPTHS OF HELL. HUMANITY HAS FINALLY FOUND ITS MATCH.

CIVILISATION HAS FALLEN TO DISARRAY AND CIVIL STRIFE. ONLY A HANDFUL ELEMENTS OF RESISTANCE DARE TO DIMINISH THE DEMONS' POWER.

JOIN OUR 4 HEROES IN THEIR HEROIC JOURNEY TO RESTORE ORDER TO THE LAND.

FIND THE LEGENDARY DEMON SLAYER KEY. FOR GLORY!
'''
```
The scrolling speed is determined by the   `starting_pos`  in the `display_intro` and can be modified as one sees fit:
```python
starting_pos = 300
```


## Mob Drops

This file contains a single class called `MobDropPouch`. This is called by `Enemy` and `Boss` to create a pouch that holds loot. It is initialised as follows:

```python
def __init__(self, game, x, y, items, enemy_type):  
    self.items = items  
    self.game = game  
    self.pos_x = x  
    self.pos_y = y  
    self.enemy_type = "Regular"  
    self.location = (x, y)  
    if enemy_type == "Regular":  
        self.sprite = config.get_pouch_sprite()[0]  
    else:  
        self.sprite = config.get_boss_pouch_sprite()[0]  
    self.status = "active"  
    self.loot_msg_delay = 25  
    self.coins = 0
```
A pouch contains the items from the drop, the current game state, a position where it is to be dropped (where the monster was killed), whether the enemy is a boss or not (`enemy_type`), whether it is shown (`active`) and the number of coins it holds. 

There are also simple render functions for the pouch and associated message. None of these functions should require any changes.


## NPC and NPC Lookup

The  `NPC`  class handles the state and movement of non-hostile NPCs in the game such as the tutorial NPC. The addition of new NPCs or the modification of the behaviour of existing ones is achieved by writing into the `cutscene_lookup.py`  file, where each NPC has the following  list of attributes: 
`[npc_type, npc_name, health, shield, level, move_speed, combat_style, ai_type, vision_radius, attack_radius, attack_damage, cooldown]`:

```python
npcs = {"tutorial": {"wogol": [20, 5, 10, 1, "melee", "dumb", 500, 10, 3, 1000]}}
```
### Adding new NPCs

To add a new NPC a new entry must be added to the dictionary, specifying the NPC type and name, where the name should be consistent with a sprite name.
New NPC types should also be added to the  `spawn_npc`  function in  `game.py`  so they can be instantiated in the game.
There should be no need to change other functionality in this class as all NPC creation is handled through reference to the npc_lookup, to create easy NPC generation.



## Player and Character Classes
The Player class handles control of the player character, as well as storing all of the players items and stats

### Creating a new player character and character class
To create a new player character or character class first a new entry should be added to the `character_stats` dict in `character_classes.py`:
```python
"PALADIN": {"str": 16,
            "dex": 10,
            "con": 16,
            "int": 8,
            "wis": 8,
            "cha": 10}
```
This defines the starting attributes of the player character, where `str` `dex` and `int` affect weapon damage of that type, `wis` adds to crit chance, `cha` speeds up super charge time. `con` increases health and `dex` increases weapon speed and starting move speed. A new entry should also be made in the `starting_equipment` dict in `character_classes.py`:
```python
{"PALADIN": {"weapon": "regular_sword",
             "armor": "chainmail",
             "potion_1": ["heal_small", 5],
             "potion_2": ["shield_large", 5]}
```
the names of starting items should be the same as those appearing in `equipment_list.py`. Consumables or throwables in the potion slots are stored here as a list with list[0] the item name and list[1] the quantity held. 

### Adding a new special move
When creating a new character class, a new special move should also be created, to do this a function must first be created to be called on special activation. for example:
```python
    def spin_attack(self):
        audio.sword_swing()
        attack_width = self.special_sprite[0].get_width()
        attack_height = self.special_sprite[0].get_height()
        for actor in self.game.curr_actors:
            if isinstance(actor, (Enemy, GhostBoss, MageBoss, TentacleBoss)):
                if abs(actor.pos_x - self.pos_x) <= attack_width / 2 and abs(
                        actor.pos_y - self.pos_y) <= attack_height / 2:
                    actor.take_damage(self.special_damage)
                    audio.sword_hit()
```
this can function to have any desired effect to take place when the special is used. the new function should be called by the `special_ability(self)` function in `player.py`:

```python
    def special_ability(self):
        if self.special_charge >= 100:
            self.special_charge = 0
            self.rendering_special = True
            audio.special_move()
            if self.character_class == "ROGUE":
                self.invisible = True
            if self.character_class == "RANGER":
                self.arrow_spray()
            if self.character_class == "PALADIN":
                self.special_sprite = config.get_special_sprite("spin_attack")
                self.spin_attack()
            if self.character_class == "MAGE":
                self.special_sprite = config.get_special_sprite("magic_blast")
                self.special_sprite_offset = -50
                self.magic_blast()
```
within the if statement specific to the character class for the special attack, the special sprite can be set to create a desired animation, or left blank if this is not desired. if the special sprite is not in the desired position, the `special_sprite_offset` sets the y offset of the sprite. new special sprites should be added to the `special_sprite` section in `config.py`
### Attack and using items
the `use_item` method is the method called when right clicking with a held item:
```python
    def use_item(self):
        if isinstance(self.held_item, weapon.Weapon) and \
                pygame.time.get_ticks() - self.held_item.last_used >= 1000 * self.held_item.attack_speed:
            self.held_item.state = "blast"
            self.invisible = False

            crit_roll = random.randint(0, 100)
            crit = False
            if crit_roll <= self.held_item.crit_chance:
                crit = True
                self.display_crit = True
                audio.critical_attack()

                self.held_item.attack_damage *= 2
            if self.held_item.combat_style == "melee":
                self.attack()
                self.held_item.slash = True
                audio.sword_swing()
            elif self.held_item.combat_style == "ranged":
                self.held_item.ranged_attack()
                if self.held_item.projectile == "fireball" or self.held_item.projectile == "acid":
                    audio.magic_spell_cast()
                elif self.held_item.projectile == "magic_hammer":
                    audio.throw()
                else:
                    audio.arrow_launch()
            elif self.held_item.combat_style == "magic":
                self.held_item.magic_attack()
                audio.magic_spell_cast()

            # reset attack damage after previous crit
            if crit:
                self.held_item.attack_damage /= 2

            self.held_item.last_used = pygame.time.get_ticks()
        else:
            pass
```
melee type weapons use the attack function of the player as such:
```python
    def attack(self):
        for actor in self.game.curr_actors:
            if isinstance(actor, (Enemy, GhostBoss, MageBoss, TentacleBoss)):
                target_vector = pygame.Vector2(actor.pos_x - self.held_item.weapon_pos[0],
                                               actor.pos_y - (actor.height // 4) - self.held_item.weapon_pos[1])
                if 0 < target_vector.length() <= (self.held_item.weapon_length + actor.width / 2) / 2:
                    actor.take_damage(self.held_item.attack_damage)

                    # play hit sound
                    audio.sword_hit()
```
ranged and magic weapons use the `weapon.py` ranged and magic attack methods respectively, so to alter these this file should be altered. in order to change sounds for specific attacks, simply add a new audio call in the if statement for that weapon type.



## Projectile
The Projectile class handles missile attacks of the player, enemies and bosses, it uses the actor super class to inherit the attributes necessary for its functioning. all projectiles by default do damage when they interact with an enemy, but can also implement special additional effects using the on hit method.

### Adding new Projectiles
New projectiles specific effects added can be added by applying similar  structure  to the one below:

 ```python
def explosion(self):
    elemental_effects.Explosion(self.game, math.ceil(self.damage * 0.5), 1.5, self.pos_x, self.pos_y)
```

For the projectiles to have some extra effect on impact they must have an on hit method, therefore any new projectile will need to have a type and be added to the `on_hit` method whether the projectile is used by the player or non player actors as shown here :
```python
def on_hit(self):
    if self.projectile_type == "fireball":
        self.explosion()
    elif self.projectile_type == "acid":
        self.acid_pool()
```
### Extending/ Modifying the targeting system used by the player
The player's projectile  targeting system is currently point and click style that uses the mouse position to set the direction of the projectile:
```python
def seek_mouse(self):
    mouse_pos = pygame.mouse.get_pos()
    direction = pygame.Vector2(mouse_pos[0] - self.pos_x, mouse_pos[1] - self.pos_y)
    direction.scale_to_length(0.5)
    if pygame.mouse.get_pressed()[0] and self.seeking and not self.returning:
        self.direction += direction
        self.direction.scale_to_length(self.move_speed
```
Currently, only the magic hammer weapon has the ability to return to the player after throwing, to enable this ability the  if a new weapon was to also use this feature the `return_to_caster`  method detailed here should be called :
```python
def return_to_caster(self):
    self.returning = True
  player = self.game.curr_actors[0]
    self.direction = pygame.Vector2(player.pos_x - self.pos_x, player.pos_y - self.pos_y)
    if self.direction.length() <= 50:
        self.hit = True
 if player.held_item is not None:
            player.held_item.state = "idle"
  audio.sword_swing()
    self.direction.scale_to_length(self.move_speed * 2)
    if player.held_item is not None:
        player.held_item.last_used = pygame.time.get_ticks()
```


and the new projectile's type should be added to the  `return_weapon` method here as such  :
```python
def return_weapon(self):
    if self.projectile_type == "magic_hammer":
        if not pygame.mouse.get_pressed()[0] or self.returning:
            self.return_to_caster()
```


Similarly, only the ricochet bow weapon has the ability to launch projectiles that ricochet of walls therefore new added weapons that have this ability should same similar structure to the   `ricochet` method here  :
```python
def ricochet(self):
    if self.hits > 0:
        self.hit = False
  self.damage = max(2, self.damage // 2)
        for actor in self.game.curr_actors:
            if (isinstance(actor, Enemy) and not self.hits_player) or (isinstance(actor, Player) and self.hits_player):
                distance_vector = pygame.Vector2(actor.pos_x - self.pos_x, actor.pos_y - actor.height // 2 - self.pos_y)
                if 200 >= distance_vector.length() >= 50:
                    self.direction = distance_vector
                    break```
```

## Saving and Loading
The `GameSave` class holds the current state of the game, and allows writing of the state and reading of the state from serialized binary files using pythons pickle module. The `__init__` can be seen below:
```python
    def __init__(self):
        self.player_dict = {"score": 0, "character_class": "knight", "character_gender": "m", "health": 5, "shield": 0,
                            "level": 0, "money": 0, "stats": [0, 0, 0, 0, 0, 0], "weapons": [], "potion_1": None,
                            "potion_2": None, "inventory": []}
        self.save_name = ""
        self.score = ""
        self.save_time = ""
        self.curr_map_no = None
```

From this player dict, a player character can be fully recreated to save their progress. due to game limitations, position and state of other items is not maintained, but this allows for a more replayable game.

The first two functions in `GameSave` allow for saving and loading of the game:
```python
    def save_game(self, game, save_name=""):
        player = game.curr_actors[0]

        self.player_dict["score"] = player.score
        self.player_dict["character_class"] = game.player_character
        self.player_dict["character_gender"] = game.player_gender
        self.player_dict["health"] = player.health
        self.player_dict["shield"] = player.shield
        self.player_dict["level"] = player.entity_level
        self.player_dict["money"] = player.money
        self.player_dict["inventory"] = player.inventory
        self.player_dict["stats"] = [player.strength, player.dexterity, player.constitution, player.intellect, player.wisdom, player.charisma]
        self.player_dict["weapons"] = []
        for weapon in player.items:
            if weapon is not None:
                self.player_dict["weapons"].append(weapon.name)
        self.player_dict["potion_1"] = player.get_potion(1)
        self.player_dict["potion_2"] = player.get_potion(2)

        if save_name != "":
            self.save_name = save_name
        self.curr_map_no = game.current_map_no
        self.save_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.score = str(player.score)

        # save save state to file
        with open("./game_saves/" + self.save_name, "wb") as f:
            pickle.dump(self, f)

    def load_game(self, game):
        # load save state from file
        with open("./game_saves/" + self.save_name, "rb") as f:
            self.__dict__.update(pickle.load(f).__dict__)

        # update player attributes to save state
        player = game.curr_actors[0]
        game.player_gender = self.player_dict["character_gender"]
        game.player_character = self.player_dict["character_class"]
        player.character_class = game.player_classes[game.player_character]
        player.sprite = config.get_player_sprite(game.player_character, game.player_gender)
        player.strength = self.player_dict["stats"][0]
        player.dexterity = self.player_dict["stats"][1]
        player.constitution = self.player_dict["stats"][2]
        player.intellect = self.player_dict["stats"][3]
        player.wisdom = self.player_dict["stats"][4]
        player.charisma = self.player_dict["stats"][5]
        bonuses = {"str": (player.strength - 10) // 2,
                   "dex": (player.dexterity - 10) // 2,
                   "con": (player.constitution - 10) // 2,
                   "int": (player.intellect - 10) // 2,
                   "wis": (player.wisdom - 10) // 2,
                   "cha": (player.charisma - 10) // 2}

        player.move_speed = ((5 + ((character_classes.character_stats[player.character_class]["dex"] - 10) // 2)) / 5)

        player.score = self.player_dict["score"]
        player.health = self.player_dict["health"]
        player.shield = self.player_dict["shield"]
        player.entity_level = self.player_dict["level"]
        player.money = self.player_dict["money"]
        player.armor = equipment_list.armor_list[character_classes.starting_equipment[player.character_class]["armor"]]
        player.inventory = self.player_dict["inventory"]
        player.items = []
        for weapon in self.player_dict["weapons"]:
            player.items.append(Weapon(game, weapon, player.pos_x, player.pos_y,
                                       config.get_weapon_sprite(weapon), 1,
                                       equipment_list.weapons_list[weapon]["cost"],
                                       equipment_list.weapons_list[weapon]["type"],
                                       equipment_list.weapons_list[weapon]["range"] * 16,
                                       equipment_list.weapons_list[weapon]["dmg"]
                                       + bonuses[equipment_list.weapons_list[weapon]["main_stat"]],
                                       1 / max((equipment_list.weapons_list[weapon]["speed"] + (bonuses["dex"] / 2)),
                                               0.1),
                                       equipment_list.weapons_list[weapon]["crit_chance"]
                                       + (bonuses["wis"] * 2)))
        for none_weapon in range(len(self.player_dict["weapons"]), 3):
            player.items.append(None)
        player.held_item = player.items[0]

        player.potion_1 = []
        player.potion_2 = []

        if self.player_dict["potion_1"] is not None:
            player.add_potions_to_slot(1, self.player_dict["potion_1"])
        if self.player_dict["potion_2"] is not None:
            player.add_potions_to_slot(2, self.player_dict["potion_2"])
        game.change_map(self.curr_map_no)
```
These functions and the player dict would need to be modified if any additional states needed to be saved. Due to the limitations of pickle, saved objects must not include pygame surfaces as these are not supported by pickle.

the final function is called in the load game menu to display the saved time and score as well as save name to differentiate saves when loading:

```python
  def get_time_and_score(self, save_name):
        if save_name == "":
            pass
        # load save state from file
        try:
            with open("game_saves/" + save_name, "rb") as f:
                self.__dict__.update(pickle.load(f).__dict__)
            return [self.save_time, self.score]
        except PermissionError:
            return ["0", "0"]

```
This function should not require modification

## Setup
`setup.py` allows for the game to be built to create and executeable when you run `python setup.py build` from the terminal. any non python files required for game operation should be listed in the `include_files` list.
```python
import cx_Freeze
import sys
base_setup = 'Win32GUI' if sys.platform == 'win32' else None
executables = [cx_Freeze.Executable("main.pyw", base = base_setup, icon='dungeongameicon.ico', targetName='CavernousDepths.exe')]

buildOptions = dict(packages = ["pygame", "configparser", "random"], include_files = ['assets/', 'game_saves/', 'dungeongameicon.png', 'mapframe.txt', 'mapframe2.txt', 'mapframe3.txt', 'mapframe_tutorial.txt'])

cx_Freeze.setup(
         name = "DungeonGame",
         version = "0.1",
         options = dict(build_exe = buildOptions),
         executables = executables)
```
## Shop
This handles the creation of shops, along with the items that specific shops have. This is where a new shop should be created or current shops altered.

- [Transaction Logic](#transaction-logic)
- [Shop Stock](#shop-stock)

### Transaction Logic
`shop.py` contains the logic for interacting with shops. This involves: 
- Checking if the player has enough money to buy a chosen item
- Retrieving the cost of items
- Buying items
- Selling items

These are all functions belonging to the super-class `Shop` from which all shops should inherit, thus providing them with the same functionality.

### Shop Stock 
Each shop has its own inventory, held in `self.shop_inv`. This is a list of up to 25 items, holding the names of items, how many are in stock and an item type, either weapon, potion or throwable. This means that `ui.py` can retrieve the name, and thus render the sprites when creating the shop. 

An item can be added to a shop through:
```python
self.shop_inv[0] = ["knight_sword", self.max_stock, "weapon"]
```
Passing the item name, corresponding to those seen in `equimpent_list.py`. The indexing in `shop_inv[0]` corresponds to which slot the item should be in, and so the order and groupings of items can be customised.

## Throwables
This class handles the creation of potions and throwables and operations like targeting and using.

### Add new throwables
All the throwables and their features are stated in `equipment_list.py`.  There are two dicts (`potions_list` and `throwables_list`), the features and the player who can hold that need to be added to one of them depending on which type the throwable is.
For potions, features need to be filled in as follow:

```python
"potion type": {"sprite_name": "the name of the tile picture", "size": how much health/shield it heals, "type": "type of effect", "level": generic value, "cost": gold amount needed to buy,  
  "name": "the name of the potion"},
  ```

For throwables, element is a little different from potions.
```python
"explosion type": {"sprite_name": "the name of the tile picture", "element_size": size in tiles of the elemetal effect, "damage": damage of the effect, "type": "type of effect", "level": generic value,  
  "cost": gold amount needed to buy, "name": "the name of the throwable"}
  ```



## UI
To extend/modify the current User Interface (UI) system either by changing the sprites used or the design of shops, inventory and the hotbar the `ui.py` file must be accessed as follow:

- [Display UI](#display-ui)
- [Changing sprites](#changing-sprites)
- [Shop](#shop)
- [Shopkeeper](#shopkeeper)
- [Boss Name and Health](#boss-name-and-health)
- [Drawing the Inventory](#drawing-the-inventory)
- [Toggling Inventory and Shop](#toggling-inventory-and-shop)
- [Buying and Selling Items](#buying-and-selling-items)

### Display UI
The `display_ui` function handles the rendering of almost everything onto the screen, and as such is the last function called in the game loop in `game.py`. If new functions are needed to be run every tick, they should be implemented in `display_ui`.  

The function is passed 2 variables other than `self`, being `time` and `player`. These represent the current game tick and the player's current state respectively, being items, health, shield, experience, etc. 

These are passed to the likes of `self.render_stats` to update the current health, shield, experience and level. Because of this, `ui.py` doesn't deal with the altering of values, it is simply passed variables, and renders them to the screen as required. 

### Changing Sprites
Each sprite is loaded in the `__init__` function call, this ensures they are only loaded once, as loading images is a resource heavy task. Below shows how you can load a sprite. 
```python
self.coin_0 = pygame.image.load('./assets/frames/coin_anim_f0.png')
```
From here, some sprites are scaled by 2x and others by a specific value to provide the correct size for the screen. We can simply scale an image by 2x with the below call. Note that this returns a new scaled image, and so must be assigned to a variable.
```python
self.coin_0 = pygame.transform.scale2x(self.coin_0)
```
And the below shows how to scale by a value. Here we have used `self.coin_scale = 24` as the value to scale by.
```python
self.coin_0 = pygame.transform.scale(self.coin_0, (self.coin_scale, self.coin_scale))
```
One could either edit the current sprites so as to change the currently displayed sprites used by the UI, requiring no changes to other aspects of the code. Alternatively, new sprites could be added to the game and the code adjusted to display as required.


### Shop
`ui.py` handles the shop's functionality, including the rendering of the player's items, the shop's stock, highlighting of currently selected items, and the buying and selling of items. 

Selecting items is handled by `shop_select_item`, which retrieves the current mouse position with `mouse = pygame.mouse.get_pos()`, and as a result, the inventory slot which the mouse position corresponds to. We can then use this information to store the current inventory index in `self.item_to_find_info = index`, which holds the selected item. The inventory tile's location is stored 
in `self.item_to_find_info_pos` so that it can be highlighted. 

Highlighting is handled by: 
```python
def highlight_item(self, tile):  
    highlight = pygame.Surface(((tile[1][0] - tile[0][0]), (tile[1][1] - tile[0][1])))  
    highlight.set_alpha(50)  
    highlight.fill((252, 207, 3))  
    self.game.display.blit(highlight, (tile[0][0], tile[0][1]))
```
This is passed the tile's location as explained above, and then provides a golden highlight, this makes it clear which item is currently selected both in the Shop when selling or buying items, and also when swapping items in the inventory.

When an item is clicked, its stats are displayed so the user can easily compare weapons and make upgrades. `draw_item_stats` takes the currently selected item, looks up its stats in `equipment_list.py`, and neatly renders them to the screen. It separately handles weapons, potions and throwables, as they all hold different stats. This means if a new item is added to the game, its stats will already render correctly when clicked.

### Shopkeeper

We currently only have one shop, and so only require one shopkeeper, and they are rendered using: 
```python
def draw_shopkeeper(self, shop_type):  
    if shop_type == 'weapon':  
        shopkeeper = self.get_shopkeeper(pygame.time.get_ticks())  
        shopkeeper = pygame.transform.scale(shopkeeper, (200, 200))  
  
        self.game.display.blit(shopkeeper, (config.GAME_WIDTH // 2 - 550, config.GAME_HEIGHT // 2 - 120))  
        self.game.display.blit(self.big_chat_bubble, (150, 160))  
        self.game.draw_text("How can I help", 40, 246, 190, (0, 0, 0))  
        self.game.draw_text("you today?", 40, 246, 214, (0, 0, 0))
```
This function was made to be useable no matter how many shops there are, due to the argument `shop_type`. For the weapon shop we initially call `self.get_shopkeeper` (explained below) to retrieve the current sprite to be rendered. It is then scaled as mentioned in [Changing sprites](#changing-sprites). Finally, it is rendered to the screen with a chat box with customisable text.

```python
def get_shopkeeper(self, time):  
    if time % self.shopkeeper_rotation < self.shopkeeper_rotation / 4:  
        return self.shopkeeper_weapons_0  
    if self.shopkeeper_rotation / 4 <= time % self.shopkeeper_rotation < self.shopkeeper_rotation / 2:  
        return self.shopkeeper_weapons_1  
    if self.shopkeeper_rotation / 2 <= time % self.shopkeeper_rotation < self.shopkeeper_rotation * 3 / 4:  
        return self.shopkeeper_weapons_2  
    if time % self.shopkeeper_rotation >= self.shopkeeper_rotation * 3 / 4:  
        return self.shopkeeper_weapons_3
```
This checks the current game time and compares it to `self.shopkeeper_rotation = 1000`. The four `if` statements represent each of the four sprites used in the shopkeeper's animation. As can be seen, this splits the 1000 by 4, thus a full rotation of the sprite animation takes 1000ms with each of the four sprites occupying the screen for 250ms per rotation. Due to this, a new shopkeeper could be added for new stores, and the animation speed can be easily altered. Other functions act in a similar way, such as `coin_animation` and `specbar_animation`. 

### Boss Name and Health
The rendering of a boss's health and name is handled in:
```python
def display_boss_bar(self, curr_health, max_health, boss_name):  
    bg = pygame.Surface((450, 70))  
    bg.fill((0, 0, 0))  
    health_width = 436 * (curr_health / max_health)  
    if health_width > 0:  
        pygame.draw.rect(bg, self.hotbar_bg_colour, ((2, 48), (440, 16)))  
        pygame.draw.rect(bg, config.BLACK, ((4, 50), (436, 12)))  
        pygame.draw.rect(bg, (218, 78, 76), ((4, 50), (health_width, 12)))  
    self.game.display.blit(bg, (700, 6))  
    if curr_health <= 0:  
        self.game.draw_text("HAS BEEN DEFEATED", 50, 924, 50, (218, 78, 76))  
    self.game.draw_text(boss_name.upper(), 50, 924, 20)
```
Here we initial create a black background and a width for the health bar, which scales with respect to the current health (`curr_health`) and maximum health (`max_health`). While the boss is alive, the health bar is rendered to the screen, with the with corresponding to the percentage of health remaining. Once the boss is defeated, this is replaced by `"HAS BEEN DEFEATED"`. And finally, the boss's name is rendered above the health bar.

### Drawing the inventory

This is carried all handled by `draw_inventory`. First, a silver background is created, and then a smaller black surface inside this to provide the trim seen in the game. This is a reusable function and can be passed text, which is rendered above the box, and as such is how the inventory, shop and info boxes are drawn. 

If tiles are required, the keyword argument `tiles=true` should be passed into draw_inventory. It then loops through drawing a 5x5 grid, which can be altered changing `for _ in range(5):`.  Tiles are drawn and if it is for the inventory, the player's inventory is checked for items, if items are found, they are also rendered to the screen. The coordinates of each tile is added to a list, which can be indexed to find the coords of the tile containing the corresponding item from the player's inventory or shop's stock. This way we can easily highlight the tile when selected. 

### Toggling Inventory and Shop
This is carried out with a simple `True` or `False` flag.
```python
def toggle_shop(self):  
    self.shop_inventory_tile_positions = []  
    self.shop_shop_tile_positions = []  
    background_mask = pygame.Surface((config.GAME_WIDTH, config.GAME_HEIGHT))  
    background_mask.set_alpha(200)  
    background_mask.fill((0, 0, 0))  
    self.game.display.blit(background_mask, (0, 0))  
    self.draw_inventory(268, 268, config.GAME_WIDTH // 2 - (268 + 20), config.GAME_HEIGHT // 2 - 140, "Inventory", True)  
    self.draw_inventory(268, 268, config.GAME_WIDTH // 2 + 20, config.GAME_HEIGHT // 2 - 140, "Shop", True)  
    if self.item_to_find_info is not None:  
        self.draw_inventory(180, 268, config.GAME_WIDTH // 2 + 310, config.GAME_HEIGHT // 2 - 140, "Info", False)  
    self.draw_shopkeeper('weapon')
```
As we can see, any selected items are cleared when then shop or inventory is reopened. The `background_mask` simply applies a shading to the background, providing focus for the shop and inventory. `draw_inventory`, from [Drawing the Inventory](#drawing-the-inventory), is then called with locations of the width and height of the inventory and shop, x and y coordinates for rendering, a name and the tile flag.

If there is a currently selected item, as checked in:
```python 
if self.item_to_find_info is not None:
```
Then the info for the corresponding item is rendered. And finally, the shopkeeper, in this case for the weapon shop, is drawn.

### Buying and Selling Items

The transaction of items and gold between the player and shopkeeper is all dealt with in `shop_buy_or_sell`. When an item is selected, its type is checked, and if from the player inventory, a sell option is displayed, otherwise, a buy option is. Simple checks are run to check quantity owned, if there is enough gold when buying, and if there is space in the inventory. If satisfied, the transaction occurs and items are placed in the inventory and money deducted.
  

## Weapon
The Weapon class handles weapons that can be held by the player. all weapons are displayed to rotate to the direction the player is aiming. instantiation and usage of weapons is primarily handled by the `Player` class.
### Adding new Weapons
New Weapons are handled through the `equipment_list.py` file, which can be added to as so:

 ```python
weapons_list = {
    "regular_sword": {"main_stat": "str", "dmg": 5, "speed": 1, "range": 2, "crit_chance": 15, "type": "melee",
                     "cost": 5, "name": "Basic Sword"},
    "knight_sword": {"main_stat": "str", "dmg": 10, "speed": 1, "range": 2, "crit_chance": 15, "type": "melee",
                     "cost": 150, "name": "Knight Sword"},
    "bow": {"main_stat": "dex", "dmg": 2, "speed": 0.5, "range": 0, "crit_chance": 5, "type": "ranged", "projectile": "standard_arrow", "cost": 5,
            "name": "Bow"},...
```
Where main stat attribute adds bonus damage based on players amount of that stat, dmg is base damage per hit, speed is number of attacks per second, gets bonus from dex, range is attack range in cells, crit_chance is percentage to do double damage, gets bonus from wis, type is the weapon type, cost is amount of gold to buy / sell, name is the displayed name in game, and projectile determines what projectile is created if the weapon is ranged.

To extend and add new types of weapon beyond magic, melee or ranged, you must also create a new method to be called when that weapon is used. for example:
```python
    def ranged_attack(self):
        missile = Projectile(self.game, self.weapon_pos[0], self.weapon_pos[1],
                             config.get_projectile_sprite(self.projectile),
                             self.attack_damage, self.target_direction, self.projectile)
        if self.name == "magic_hammer":
            self.state = "thrown"
            missile.move_speed = 10
        self.game.curr_actors.append(missile)
```



