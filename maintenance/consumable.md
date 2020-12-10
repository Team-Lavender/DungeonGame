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
If a new consumable is added to the game, an `elif` statement should be added for its type to apply its related effect, visual effects and audio on usage.

There should be no need to alter any other functions, but if adding new consumables a `'consumable_name'_up` function should be added, applying the required effects.