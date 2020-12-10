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