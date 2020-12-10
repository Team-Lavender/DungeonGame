
## Projectile
The Projectile class handles missile attacks of the player, enemies and bosses, it uses the actor super class to inherit the attributes necessary for its functioning.

### Adding new Projectiles
New projectiles added can be added by applying similar  structure  to the one below:

 ```python
def explosion(self):
    elemental_effects.Explosion(self.game, math.ceil(self.damage * 0.5), 1.5, self.pos_x, self.pos_y)
```

For the projectiles to do damage they must be instantiated on hit, therefore any new projectile will need to have a type and be added to the `on_hit` method whether the projectile is used by the player or non player actors as shown here :
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

