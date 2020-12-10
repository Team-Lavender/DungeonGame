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