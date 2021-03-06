# character stats start from 0, with 10 being an average stat

character_stats = {"PALADIN": {"str": 16,
                               "dex": 10,
                               "con": 16,
                               "int": 8,
                               "wis": 8,
                               "cha": 10},

                   "RANGER": {"str": 12,
                              "dex": 16,
                              "con": 12,
                              "int": 10,
                              "wis": 10,
                              "cha": 12},

                   "MAGE": {"str": 8,
                            "dex": 10,
                            "con": 10,
                            "int": 16,
                            "wis": 14,
                            "cha": 14},

                   "ROGUE": {"str": 10,
                             "dex": 16,
                             "con": 12,
                             "int": 12,
                             "wis": 14,
                             "cha": 16}}

starting_equipment = {"PALADIN": {"weapon": "regular_sword",
                                  "armor": "chainmail",
                                  "potion_1": ["heal_small", 5],
                                  "potion_2": ["shield_large", 5]},

                      "RANGER": {"weapon": "bow",
                                 "armor": "leather",
                                 "potion_1": ["heal_large", 2],
                                 "potion_2": ["shield_small", 5]},

                      "MAGE": {"weapon": "staff_of_lightning",
                               "armor": "none",
                               "potion_1": ["heal_large", 4],
                               "potion_2": ["shield_small", 3]},

                      "ROGUE": {"weapon": "knife",
                                "armor": "none",
                                "potion_1": ["shield_large", 3],
                                "potion_2": ["super_small", 6]}}
