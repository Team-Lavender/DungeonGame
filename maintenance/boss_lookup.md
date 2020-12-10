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