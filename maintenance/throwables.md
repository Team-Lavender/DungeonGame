## Throwables
This class handles the creation of potions and throwables and operations like targeting and using.

### Add new throwables
All the throwables and their features are stated in `equipment_list.txt`.  There are two dicts (`potions_list` and `throwables_list`), the features and the player who can hold that need to be added to one of them depending on which type the throwable is.
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


  

