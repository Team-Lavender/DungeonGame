

# each enemy has a list of attributes:
# [health, shield, level, move_speed, combat_style, ai_type, vision_radius, attack_radius, attack_damage, cooldown, drops{item_name: drop chance}]
enemies = {"demon": {"big_demon": [20, 5, 5, 0.5, "melee", "dumb", 500, 10, 3, 1000, {"dagger_ruby": 100 , "coins": 50, "shield_large": 70}],
                     "chort": [10, 3, 3, 0.7, "melee", "dumb", 200, 5, 1, 500, {"katana": 100 , "coins": 50, "heal_small": 100}]},
           "undead": {"big_zombie": []},
           "orc": {"ogre": []}}
