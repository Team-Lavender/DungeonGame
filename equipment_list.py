# AC is the amount of shielding provided. weight provides a movement penalty if strength is too low
armor_list = {"chainmail": {"AC": 5, "weight": 5},
              "leather": {"AC": 2, "weight": 2},
              "none": {"AC": 0, "weight": 0}}

# main stat: attribute must be 13 or greater to use this weapon, attribute adds bonus damage
# dmg is base damage per hit
# speed is number of attacks per second, gets bonus from dex
# range is attack range in cells
# crit_chance is percentage to do double damage, gets bonus from wis
# type is the weapon type
# cost is amount of gold to buy / sell


weapons_list = {
    "knight_sword": {"main_stat": "str", "dmg": 5, "speed": 1, "range": 2, "crit_chance": 15, "type": "melee",
                     "cost": 5, "name": "Knight Sword"},
    "bow": {"main_stat": "dex", "dmg": 2, "speed": 0.1, "range": 0, "crit_chance": 5, "type": "ranged", "projectile": "standard_arrow", "cost": 5,
            "name": "Bow"},
    "staff_of_lightning": {"main_stat": "int", "dmg": 5, "speed": 0.75, "range": 7, "crit_chance": 15, "type": "magic",
                         "cost": 5, "name": "Staff of Lightning"},
    "staff_of_fireball": {"main_stat": "int", "dmg": 5, "speed": 0.5, "range": 5, "crit_chance": 15, "type": "ranged",
                          "projectile": "fireball", "cost": 5, "name": "Staff of Fireball"},
    "staff_of_acid": {"main_stat": "int", "dmg": 5, "speed": 0.5, "range": 5, "crit_chance": 15, "type": "ranged",
                          "projectile": "acid", "cost": 5, "name": "Staff of Acid"},
    "knife": {"main_stat": "dex", "dmg": 1, "speed": 5, "range": 1, "crit_chance": 5, "type": "melee", "cost": 5,
              "name": "Knife"},
    "katana": {"main_stat": "dex", "dmg": 3, "speed": 2, "range": 1, "crit_chance": 7, "type": "melee", "cost": 5,
               "name": "Katana"},
    "lavish_sword": {"main_stat": "str", "dmg": 2, "speed": 2, "range": 1, "crit_chance": 8, "type": "melee", "cost": 5,
                     "name": "Lavish Sword"},
    "dagger_ruby": {"main_stat": "dex", "dmg": 2, "speed": 3, "range": 1, "crit_chance": 3, "type": "melee", "cost": 5,
                    "name": "Ruby Dagger"}}

# potion_type: {sprite name, size, type, level, cost, name}
potions_list = {"heal_small": {"sprite_name": "flask_red", "size": 2, "type": "heal", "level": 1, "cost": 1,
                               "name": "Small Healing Potion"},
                "heal_large": {"sprite_name": "flask_big_red", "size": 5, "type": "heal", "level": 2, "cost": 2,
                               "name": "Large Healing Potion"},
                "shield_small": {"sprite_name": "flask_blue", "size": 2, "type": "shield", "level": 1, "cost": 1,
                                 "name": "Small Shield Potion"},
                "shield_large": {"sprite_name": "flask_big_blue", "size": 5, "type": "shield", "level": 2, "cost": 2,
                                 "name": "Large Shield Potion"},
                "super_small": {"sprite_name": "flask_purple", "size": 20, "type": "super", "level": 1, "cost": 1},
                "super_large": {"sprite_name": "flask_big_purple", "size": 100, "type": "super", "level": 2, "cost": 2}}

throwables_list = {
    "explosive_small": {"sprite_name": "bomb_small", "element_size": 2, "damage": 5, "type": "explosive", "level": 1,
                        "cost": 1, "name": "Small Bomb"},
    "explosive_large": {"sprite_name": "bomb_big", "element_size": 3, "damage": 10, "type": "explosive", "level": 2,
                        "cost": 2, "name": "Large Bomb"},
    "acid_small": {"sprite_name": "flask_green", "element_size": 1, "damage": 1, "type": "acid", "level": 1,
                   "cost": 1, "name": "Small Acid Bomb"},
    "acid_large": {"sprite_name": "flask_big_green", "element_size": 2, "damage": 2, "type": "acid",
                   "level": 2, "cost": 2, "name": "Large Acid Bomb"}}
