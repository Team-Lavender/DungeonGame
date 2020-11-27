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
                     "cost": 5},
    "bow": {"main_stat": "dex", "dmg": 2, "speed": 1, "range": 0, "crit_chance": 5, "type": "ranged", "cost": 5},
    "green_magic_staff": {"main_stat": "int", "dmg": 5, "speed": 1, "range": 5, "crit_chance": 15, "type": "magic",
                          "cost": 5},
    "knife": {"main_stat": "dex", "dmg": 1, "speed": 5, "range": 1, "crit_chance": 5, "type": "melee", "cost": 5},
    "katana": {"main_stat": "dex", "dmg": 3, "speed": 2, "range": 1, "crit_chance": 7, "type": "melee", "cost": 5},
    "lavish_sword": {"main_stat": "str", "dmg": 2, "speed": 2, "range": 1, "crit_chance": 8, "type": "melee", "cost": 5},
    "dagger_ruby": {"main_stat": "dex", "dmg": 2, "speed": 3, "range": 1, "crit_chance": 3, "type": "melee", "cost": 5}}


# potion_type: {sprite name, size, type, level, cost}
potions_list = {"heal_small": {"sprite_name": "flask_red", "size": 2, "type": "heal", "level": 1, "cost": 1},
                "heal_large": {"sprite_name": "flask_big_red", "size": 5, "type": "heal", "level": 2, "cost": 2},
                "shield_small": {"sprite_name": "flask_blue", "size": 2, "type": "shield", "level": 1, "cost": 1},
                "shield_large": {"sprite_name": "flask_big_blue", "size": 5, "type": "shield", "level": 2, "cost": 2},
                "super_small": {"sprite_name": "flask_purple", "size": 20, "type": "super", "level": 1, "cost": 1},
                "super_large": {"sprite_name": "flask_big_purple", "size": 100, "type": "super", "level": 2, "cost": 2}}

throwables_list = {
    "explosive_small": {"sprite_name": "bomb_small", "element_size": 2, "damage": 5, "type": "explosive", "level": 1, "cost": 1},
    "explosive_large": {"sprite_name": "bomb_big", "element_size": 3, "damage": 10, "type": "explosive", "level": 2, "cost": 2},
    "acid_small": {"sprite_name": "flask_green", "element_size": 1, "damage": 1, "type": "acid", "level": 1,
                        "cost": 1},
    "acid_large": {"sprite_name": "flask_big_green", "element_size": 2, "damage": 2, "type": "acid",
                        "level": 2, "cost": 2}}
