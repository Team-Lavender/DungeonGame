
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
Where main stat attribute adds bonus damage based on players amount of that stat, dmg is base damage per hit, speed is number of attacks per second, gets bonus from dex, range is attack range in cells, crit_chance is percentage to do double damage, gets bonus from wis, type is the weapon type, cost is amount of gold to buy / sell, name is the diaplsyed name in game, and projectile determines what projectile is created if the weapon is ranged.

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


