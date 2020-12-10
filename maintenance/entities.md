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