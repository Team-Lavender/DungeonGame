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
    "regular_sword": {"main_stat": "str", "dmg": 5, "speed": 1, "range": 2, "crit_chance": 15, "type": "melee",
                     "cost": 5, "name": "Basic Sword"},
    "knight_sword": {"main_stat": "str", "dmg": 10, "speed": 1, "range": 2, "crit_chance": 15, "type": "melee",
                     "cost": 500, "name": "Knight Sword"},
    "bow": {"main_stat": "dex", "dmg": 2, "speed": 0.1, "range": 0, "crit_chance": 5, "type": "ranged", "projectile": "standard_arrow", "cost": 5,
            "name": "Bow"},
    "ricochet_bow": {"main_stat": "dex", "dmg": 15, "speed": 0.1, "range": 0, "crit_chance": 5, "type": "ranged", "projectile": "ricochet_arrow", "cost": 1000,
            "name": "Ricochet Bow"},
    "split_bow": {"main_stat": "dex", "dmg": 5, "speed": 0.1, "range": 0, "crit_chance": 5, "type": "ranged", "projectile": "split_arrow", "cost": 500,
            "name": "Split Bow"},
    "seeking_bow": {"main_stat": "dex", "dmg": 10, "speed": 0.1, "range": 0, "crit_chance": 15, "type": "ranged", "projectile": "seeking_arrow", "cost": 500,
            "name": "Seeking Bow"},
    "staff_of_lightning": {"main_stat": "int", "dmg": 5, "speed": 0.75, "range": 7, "crit_chance": 15, "type": "magic",
                         "cost": 5, "name": "Staff of Lightning"},
    "staff_of_fireball": {"main_stat": "int", "dmg": 15, "speed": 0.5, "range": 5, "crit_chance": 15, "type": "ranged",
                          "projectile": "fireball", "cost": 500, "name": "Staff of Fireball"},
    "staff_of_acid": {"main_stat": "int", "dmg": 25, "speed": 0.5, "range": 5, "crit_chance": 15, "type": "ranged",
                          "projectile": "acid", "cost": 2000, "name": "Staff of Acid"},
    "knife": {"main_stat": "dex", "dmg": 1, "speed": 5, "range": 1, "crit_chance": 5, "type": "melee", "cost": 5,
              "name": "Knife"},
    "katana": {"main_stat": "dex", "dmg": 15, "speed": 2, "range": 1, "crit_chance": 7, "type": "melee", "cost": 1000,
               "name": "Katana"},
    "lavish_sword": {"main_stat": "str", "dmg": 20, "speed": 2, "range": 1, "crit_chance": 8, "type": "melee", "cost": 1000,
                     "name": "Lavish Sword"},
    "dagger_ruby": {"main_stat": "dex", "dmg": 10, "speed": 3, "range": 1, "crit_chance": 3, "type": "melee", "cost": 500,
                    "name": "Ruby Dagger"},
    "magic_hammer": {"main_stat": "str", "dmg": 20, "speed": 2, "range": 0, "crit_chance": 5, "type": "ranged",
                    "projectile": "magic_hammer", "cost": 5000,
                    "name": "Hammer of Storms"}}


# potion_type: {sprite name, size, type, level, cost, name}
potions_list = {"heal_small": {"sprite_name": "flask_red", "size": 2, "type": "heal", "level": 1, "cost": 5,
                               "name": "Small Healing Potion"},
                "heal_large": {"sprite_name": "flask_big_red", "size": 5, "type": "heal", "level": 2, "cost": 15,
                               "name": "Large Healing Potion"},
                "shield_small": {"sprite_name": "flask_blue", "size": 2, "type": "shield", "level": 1, "cost": 5,
                                 "name": "Small Shield Potion"},
                "shield_large": {"sprite_name": "flask_big_blue", "size": 5, "type": "shield", "level": 2, "cost": 15,
                                 "name": "Large Shield Potion"},
                "super_small": {"sprite_name": "flask_purple", "size": 20, "type": "super", "level": 1, "cost": 10,
                                "name": "Small Super Potion"},
                "super_large": {"sprite_name": "flask_big_purple", "size": 100, "type": "super", "level": 2, "cost": 20,
                                "name": "Small Super Potion"}}

throwables_list = {
    "explosive_small": {"sprite_name": "bomb_small", "element_size": 2, "damage": 20, "type": "explosive", "level": 1,
                        "cost": 20, "name": "Small Bomb"},
    "explosive_large": {"sprite_name": "bomb_big", "element_size": 3, "damage": 50, "type": "explosive", "level": 2,
                        "cost": 50, "name": "Large Bomb"},
    "acid_small": {"sprite_name": "flask_green", "element_size": 1, "damage": 10, "type": "acid", "level": 1,
                   "cost": 40, "name": "Small Acid Bomb"},
    "acid_large": {"sprite_name": "flask_big_green", "element_size": 2, "damage": 15, "type": "acid",
                   "level": 2, "cost": 60, "name": "Large Acid Bomb"}}
