
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




