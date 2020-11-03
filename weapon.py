from item import *


class Weapon(Item):
    def __init__(self, game, pos_x, pos_y, sprite, item_level, cost, combat_style, attack_range, dmg, speed,
                 crit_chance):
        super(Weapon, self).__init__(game, pos_x, pos_y, sprite, item_level, cost, combat_style)
        self.attack_range = attack_range
        self.attack_damage = dmg
        self.attack_speed = speed
        self.crit_chance = crit_chance
