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


weapons_list = {"knight_sword": {"main_stat": "str", "dmg": 5, "speed": 1, "range": 2, "crit_chance": 5, "type": "melee", "cost": 5},
                "bow": {"main_stat": "dex", "dmg": 2, "speed": 1, "range": 0, "crit_chance": 5, "type": "ranged", "cost": 5},
                "green_magic_staff": {"main_stat": "int", "dmg": 5, "speed": 1, "range": 5, "crit_chance": 5, "type": "magic", "cost": 5},
                "knife": {"main_stat": "dex", "dmg": 1, "speed": 5, "range": 1, "crit_chance": 5, "type": "melee", "cost": 5}}