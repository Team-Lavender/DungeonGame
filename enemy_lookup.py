

# each enemy has a list of attributes:
# [health, shield, level, move_speed, combat_style, ai_type, vision_radius, attack_radius, attack_damage, cooldown, drops{item_name: drop chance}]
enemies = {"demon": {"big_demon": [20, 5, 5, 0.5, "melee", "dumb", 500, 10, 3, 750, {"dagger_ruby": 15 , "coins": 3, "shield_large": 50}],
                     "wogol": [10, 3, 3, 0.7, "ranged", "dumb", 300, 5, 1, 1000, {"katana": 30 , "coins": 1, "heal_small": 70}]},
           "undead": {"big_zombie": []},
           "orc": {"ogre": []}}
