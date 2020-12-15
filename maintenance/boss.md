<h1 align="center">
  <br>
  <a href="https://github.com/Team-Lavender/DungeonGame"><img src="https://github.com/Team-Lavender/DungeonGame/blob/Revisions/assets/frames/title.png" alt="DungeonGame" width="500"></a>

</h1>

<h4 align="center">A challenging 2D roguelike game with a variety of enemies and exciting boss battles made entirely in <a href="https://www.pygame.org/" target="_blank">Pygame</a>.</h4>

<p align="center">
 </a>
  <a href="https://saythanks.io/to/amitmerchant1990">
      <img src="https://img.shields.io/badge/python-3.8-blue.svg">



<h1 align="center">
  <br>
  <a ></a>
  <br>
  Maintenance guide
  <br>
</h1>


  
  </a>

</p>

<p align="center">
  <a href="#boss">Boss battles</a> •
  <a href="#ui">UI</a> •
  <a href="#enemies">Enemies</a> •
  <a href="#cutscene">Cutscene</a> •
</p>


## Boss
To extend/modify the current boss system either by changing the boss mechanics or adding new bosses the `boss.py` and  `boss_lookup.py` files must be accessed as follow:
- [Adding/modifying boss types.](#adding-modifying-boss-types)
-  [Adding new attack mechanics](#adding-new-attack-mechanics)
-  [Modifying the boss movement patterns and pattern finding algorithms.](#modifying-the-boss-movement-patterns-and-path-finding-algorithms)

### Adding modifying boss types
Each boss is structured as a separate class that inherits from the entity super class, each new boss must then be added in the boss_lookup.py file in the bosses dictionary, the modifiable attributes are as follows:
```python
bosses = {"boss":{'new_boss_name': [health, shield, level, move_speed, combat_style, ai_type, vision_radius, attack_radius, attack_damage, cooldown, drops{item_name: drop chance}]}}
```
Then in the class definition the entity super class is called as follows with the 'get_new_boss_sprite' replaced with the new boss sprite:
```python
super(GhostBoss, self).__init__(game, pos_x, pos_y, config.get_new_boss_sprite(boss_name), self.lookup[0], self.lookup[1], True, self.lookup[2], "alive", self.lookup[3])
```


### Adding new attack mechanics

- After creating the new function that handles the new attack, it must be added to the current_attack method so that the boss can call it when the turn of the attack comes up.
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
- If the added attack uses projectiles then a projectile object must be instantiated with the desired characteristics and attributes, the projectile sprite must be placed in the config file and follow the template as shown here:

```python
missile = projectile.Projectile(self.game, self.pos_x, self.pos_y,config.get_new_projectile_sprite(), self.special_damage, direction, projectile_type, True, 8):
```

### Modifying the boss movement patterns and path finding algorithms

- Currently the boss file contains two movement behaviours, patrol and linear path. If new movement behaviours are to be added they need to be called from within the ai method and replace the 'new_movement_pattern' function as such:


```python
def ai(self):  
      ......
        if self.ai_type == "patrol":  
            player = self.game.curr_actors[0]  
            if pygame.time.get_ticks() - self.last_attack >= self.cooldown and not player.invisible:  
                self.current_attack()   
            self.new_movement_pattern(direction)  
 ```



