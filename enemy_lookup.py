

# each enemy has a list of attributes:
# [health, shield, level, move_speed, combat_style, ai_type, vision_radius, attack_radius, attack_damage, cooldown, drops{item_name: drop chance}, projectile]
enemies = {"demon": {"big_demon": [20, 20, 5, 0.7, "melee", "dumb", 200, 10, 3, 750, {"dagger_ruby": 15 , "coins": 3, "shield_large": 50}],
                     "imp": [5, 5, 1, 0.8, "melee", "dumb", 300, 5, 1, 1000, {"katana": 30 , "coins": 1, "heal_small": 70}],
                     "wogol": [10, 10, 3, 0.7, "ranged", "dumb", 300, 5, 2, 2000, {"katana": 30 , "coins": 1, "heal_small": 70}, "fireball"],
                     "chort": [10, 5, 2, 0.7, "ranged", "dumb", 300, 5, 1, 1000, {"katana": 30 , "coins": 1, "heal_small": 70}, "fireball"]},
           "undead": {"big_zombie": []},
           "orc": {"ogre": []}}
