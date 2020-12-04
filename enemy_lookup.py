

# each enemy has a list of attributes:
# [health, shield, level, move_speed, combat_style, ai_type, vision_radius, attack_radius, attack_damage, cooldown, drops{item_name: drop chance}, projectile]
enemies = {"demon": {"big_demon": [20, 20, 5, 0.7, "melee", "dumb", 200, 32, 3, 1000, {"dagger_ruby": 15 , "coins": 3, "shield_large": 50}],
                     "imp": [5, 5, 1, 0.8, "melee", "dumb", 300, 16, 1, 1000, {"katana": 30 , "coins": 1, "heal_small": 70}],
                     "wogol": [10, 10, 3, 0.7, "ranged", "dumb", 300, 16, 2, 2000, {"katana": 30 , "coins": 1, "heal_small": 70}, "fireball"],
                     "chort": [10, 5, 2, 0.7, "ranged", "dumb", 300, 16, 1, 1000, {"katana": 30 , "coins": 1, "heal_small": 70}, "fireball"],
                     "minionhead": [5, 5, 1, 0.8, "ranged", "dumb", 500, 16, 1, 1000, {"katana": 30 , "coins": 1, "heal_small": 70}, "tenticles"]},
           "undead": {"big_zombie": [100, 100, 15, 0.7, "melee", "dumb", 200, 32, 3, 750, {"dagger_ruby": 15 , "coins": 3, "shield_large": 50}],
                     "zombie": [50, 50, 1, 0.8, "melee", "dumb", 300, 16, 1, 1000, {"katana": 30 , "coins": 1, "heal_small": 70}],
                     "ice_zombie": [30, 10, 3, 0.7, "ranged", "dumb", 300, 16, 2, 2000, {"katana": 30 , "coins": 1, "heal_small": 70}, "acid"],
                     "skelet": [10, 0, 2, 0.7, "ranged", "dumb", 300, 16, 1, 1000, {"katana": 30 , "coins": 1, "heal_small": 70}, "standard_arrow"]},
           "orc": {"ogre": [200, 200, 25, 0.7, "melee", "dumb", 200, 32, 3, 750, {"dagger_ruby": 15 , "coins": 3, "shield_large": 50}],
                     "swampy": [5, 5, 20, 0.8, "melee", "dumb", 300, 16, 1, 1000, {"katana": 30 , "coins": 1, "heal_small": 70}],
                     "orc_shaman": [10, 10, 22, 0.7, "ranged", "dumb", 300, 16, 2, 500, {"katana": 30 , "coins": 1, "heal_small": 70}, "fireball"],
                     "orc_warrior": [10, 5, 20, 0.7, "ranged", "dumb", 300, 16, 1, 1000, {"katana": 30 , "coins": 1, "heal_small": 70}, "ricochet_arrow"]}}
