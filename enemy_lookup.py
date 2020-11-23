

# each enemy has a list of attributes:
# [health, shield, level, move_speed, combat_style, ai_type, vision_radius, attack_radius, attack_damage, cooldown, drops]
enemies = {"demon": {"big_demon": [20, 5, 5, 0.5, "melee", "dumb", 500, 10, 3, 1000, {"Sword": 40 , "Coins": 50, "Key": 10}],
                     "chort": [10, 3, 3, 0.7, "melee", "dumb", 200, 5, 1, 500, {"Sword": 40 , "Coins": 50, "Key": 10}]},
           "undead": {"big_zombie": []},
           "orc": {"ogre": []}}
