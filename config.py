import pygame

GAME_HEIGHT = 720
GAME_WIDTH = 1280


def is_in_window(x, y):
    return 0 < x < GAME_WIDTH and 0 < y < GAME_HEIGHT


# sprites are dicts containing lists of frames for the given animation state
def get_player_sprite(name, gender):
    return {"idle": [pygame.image.load("assets/frames/" + name + "_" + gender + "_idle_anim_f0.png"),
                     pygame.image.load("assets/frames/" + name + "_" + gender + "_idle_anim_f1.png"),
                     pygame.image.load("assets/frames/" + name + "_" + gender + "_idle_anim_f2.png"),
                     pygame.image.load("assets/frames/" + name + "_" + gender + "_idle_anim_f3.png")],
            "run": [pygame.image.load("assets/frames/" + name + "_" + gender + "_run_anim_f0.png"),
                    pygame.image.load("assets/frames/" + name + "_" + gender + "_run_anim_f1.png"),
                    pygame.image.load("assets/frames/" + name + "_" + gender + "_run_anim_f2.png"),
                    pygame.image.load("assets/frames/" + name + "_" + gender + "_run_anim_f3.png")],
            "hit": [(colorize(pygame.image.load("assets/frames/" + name + "_" + gender + "_hit_anim_f0.png"), WHITE))]}


def get_enemy_sprite(name):
    if not name == "minionhead":
        if name == "dumb_chort":
            return {"idle": [pygame.image.load("assets/frames/chort_idle_anim_f0.png"),
                             pygame.image.load("assets/frames/chort_idle_anim_f1.png"),
                             pygame.image.load("assets/frames/chort_idle_anim_f2.png"),
                             pygame.image.load("assets/frames/chort_idle_anim_f3.png")],
                    "run": [pygame.image.load("assets/frames/chort_run_anim_f0.png"),
                            pygame.image.load("assets/frames/chort_run_anim_f1.png"),
                            pygame.image.load("assets/frames/chort_run_anim_f2.png"),
                            pygame.image.load("assets/frames/chort_run_anim_f3.png")]}
        else:
            return {"idle": [pygame.image.load("assets/frames/" + name + "_idle_anim_f0.png"),
                             pygame.image.load("assets/frames/" + name + "_idle_anim_f1.png"),
                             pygame.image.load("assets/frames/" + name + "_idle_anim_f2.png"),
                             pygame.image.load("assets/frames/" + name + "_idle_anim_f3.png")],
                    "run": [pygame.image.load("assets/frames/" + name + "_run_anim_f0.png"),
                            pygame.image.load("assets/frames/" + name + "_run_anim_f1.png"),
                            pygame.image.load("assets/frames/" + name + "_run_anim_f2.png"),
                            pygame.image.load("assets/frames/" + name + "_run_anim_f3.png")]}
    else:
        return {"idle": [pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f0.png"),
                          pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f1.png"),
                          pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f2.png"),
                          # pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f3.png"),
                          # pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f4.png"),
                          # pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f5.png")
                          ],
                "run": [pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f0.png"),
                          pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f1.png"),
                          pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f2.png"),
                          # pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f3.png"),
                          # pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f4.png"),
                          # pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f5.png")
                            ]}


def get_weapon_sprite(name):
    return {"idle": [pygame.image.load("assets/frames/weapon_" + name + ".png")],

            "blast": [colorize(pygame.image.load("assets/frames/weapon_" + name + ".png"), WHITE)],
            "thrown": [pygame.image.load("assets/frames/blank.png")]}

def get_projectile_sprite(name):
    return {"idle": [pygame.image.load("assets/frames/projectiles_" + name + ".png")]}


def get_magic_sprite(name):
    return {"idle": [pygame.image.load("assets/frames/magic/magic_" + name + "_f0.png"),
                     pygame.image.load("assets/frames/magic/magic_" + name + "_f1.png"),
                     pygame.image.load("assets/frames/magic/magic_" + name + "_f2.png"),
                     pygame.image.load("assets/frames/magic/magic_" + name + "_f3.png"),
                     pygame.image.load("assets/frames/magic/magic_" + name + "_f4.png"),
                     pygame.image.load("assets/frames/magic/magic_" + name + "_f5.png"),
                     pygame.image.load("assets/frames/magic/magic_" + name + "_f6.png"),
                     pygame.image.load("assets/frames/magic/magic_" + name + "_f7.png")]}

def get_tentacle_sprite(name):
    return {"idle": [pygame.image.load("assets/frames/Boss/" + name + "_anim_f0.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_anim_f1.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_anim_f2.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_anim_f3.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_anim_f4.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_anim_f5.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_anim_f6.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_anim_f7.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_anim_f8.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_anim_f9.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_anim_f10.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_anim_f11.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_anim_f12.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_anim_f13.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_anim_f14.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_anim_f15.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_anim_f16.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_anim_f17.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_anim_f18.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_anim_f19.png")]}

def get_npc_sprite(name):
    print('we in')
    return {"idle": [pygame.image.load("assets/frames/GnollShaman_idle_1.png"),
                     pygame.image.load("assets/frames/GnollShaman_idle_2.png"),
                     pygame.image.load("assets/frames/GnollShaman_idle_3.png"),
                     pygame.image.load("assets/frames/GnollShaman_idle_4.png")],
            "run": [pygame.image.load("assets/frames/GnollShaman_Walk_1.png"),
                    pygame.image.load("assets/frames/GnollShaman_Walk_2.png"),
                    pygame.image.load("assets/frames/GnollShaman_Walk_3.png"),
                    pygame.image.load("assets/frames/GnollShaman_Walk_4.png")]}



def get_potion_fx_sprite(name):
    return {"idle": [pygame.image.load("assets/frames/magic/" + name + "/" + name + "_f0.png"),
                     pygame.image.load("assets/frames/magic/" + name + "/" + name + "_f1.png"),
                     pygame.image.load("assets/frames/magic/" + name + "/" + name + "_f2.png"),
                     pygame.image.load("assets/frames/magic/" + name + "/" + name + "_f3.png"),
                     pygame.image.load("assets/frames/magic/" + name + "/" + name + "_f4.png"),
                     pygame.image.load("assets/frames/magic/" + name + "/" + name + "_f5.png"),
                     pygame.image.load("assets/frames/magic/" + name + "/" + name + "_f6.png"),
                     pygame.image.load("assets/frames/magic/" + name + "/" + name + "_f7.png")]}

def get_sword_swing_fx():
    return [pygame.image.load("assets/frames/weapon_swing/sword_swing_f0.png"),
                     pygame.image.load("assets/frames/weapon_swing/sword_swing_f1.png"),
                     pygame.image.load("assets/frames/weapon_swing/sword_swing_f2.png"),
                     pygame.image.load("assets/frames/weapon_swing/sword_swing_f3.png"),
                     pygame.image.load("assets/frames/weapon_swing/sword_swing_f4.png"),
                     pygame.image.load("assets/frames/weapon_swing/sword_swing_f5.png"),
                     pygame.image.load("assets/frames/weapon_swing/sword_swing_f6.png"),
                     pygame.image.load("assets/frames/weapon_swing/sword_swing_f7.png")]

def get_special_sprite(name):
    return [pygame.image.load("assets/frames/special_moves/" + name + "_f0.png"),
            pygame.image.load("assets/frames/special_moves/" + name + "_f1.png"),
            pygame.image.load("assets/frames/special_moves/" + name + "_f2.png"),
            pygame.image.load("assets/frames/special_moves/" + name + "_f3.png"),
            pygame.image.load("assets/frames/special_moves/" + name + "_f4.png"),
            pygame.image.load("assets/frames/special_moves/" + name + "_f5.png")]

def get_super_mage_bomb_sprite():
    return {"idle": [pygame.image.load("assets/frames/Boss/mage_bullet.png")]}

def get_super_mage_flame_ball():
    return {"idle": [pygame.image.load("assets/frames/Boss/flame_ball_blue.png")]}

def get_super_mage_sprite(name):
    return {"idle": [pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f0.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f1.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f2.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f3.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f4.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f5.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f6.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f7.png")],
            "attack": [pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f0.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f1.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f2.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f3.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f4.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f5.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f6.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f7.png")],
            "attack_2": [pygame.image.load("assets/frames/Boss/" + name + "_attack2_anim_f0.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack2_anim_f1.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack2_anim_f2.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack2_anim_f3.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack2_anim_f4.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack2_anim_f5.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack2_anim_f6.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack2_anim_f7.png")],
            "death": [pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f0.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f1.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f2.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f3.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f4.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f5.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f6.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f7.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f8.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f9.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f10.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f11.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f12.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f13.png")] }
def get_wizard_boss_sprite(name): # 11 death # 11 atack # 9 idle # 5 for move
# big_wizard
    return {"idle": [pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f0.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f1.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f2.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f3.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f4.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f5.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f6.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f7.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f8.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f9.png")],

            "idle2": [pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f0.png")],

        "run": [pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f0.png"),
                 pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f1.png"),
                 pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f2.png"),
                 pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f3.png"),
                 pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f4.png"),
                 pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f5.png"),
                 pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f6.png"),
                 pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f7.png"),
                 pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f8.png"),
                 pygame.image.load("assets/frames/Boss/" + name + "_idle_anim_f9.png")],

            "attack2": [pygame.image.load("assets/frames/Boss/" + name + "_attack2_anim_f0.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack2_anim_f1.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack2_anim_f2.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack2_anim_f3.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack2_anim_f4.png"),
                    pygame.image.load("assets/frames/Boss/" + name + "_attack2_anim_f5.png")],

            "attack": [pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f0.png"),
                       pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f1.png"),
                       pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f2.png"),
                       pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f3.png"),
                       pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f4.png"),
                       pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f5.png"),
                       pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f6.png"),
                       pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f7.png"),
                       pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f8.png"),],

            "death": [pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f0.png"),
                      pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f1.png"),
                      pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f2.png"),
                      pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f3.png"),
                      pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f4.png"),
                      pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f5.png"),
                      pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f6.png"),
                      pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f7.png"),
                      pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f8.png"),
                      pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f9.png"),
                      pygame.image.load("assets/frames/Boss/" + name + "_death_anim_f10.png")]}

def get_greenhead_boss_sprite(name):
    return {"attack": [pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f0.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f1.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f2.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f3.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f4.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f5.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f6.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f7.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f8.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f9.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f10.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f11.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f12.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f13.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f14.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f15.png")],
            "death": [pygame.image.load("assets/frames/Boss/super_mage_death_anim_f0.png"),
                      pygame.image.load("assets/frames/Boss/super_mage_death_anim_f1.png"),
                      pygame.image.load("assets/frames/Boss/super_mage_death_anim_f2.png"),
                      pygame.image.load("assets/frames/Boss/super_mage_death_anim_f3.png"),
                      pygame.image.load("assets/frames/Boss/super_mage_death_anim_f4.png"),
                      pygame.image.load("assets/frames/Boss/super_mage_death_anim_f5.png"),
                      pygame.image.load("assets/frames/Boss/super_mage_death_anim_f6.png"),
                      pygame.image.load("assets/frames/Boss/super_mage_death_anim_f7.png"),
                      pygame.image.load("assets/frames/Boss/super_mage_death_anim_f8.png"),
                      pygame.image.load("assets/frames/Boss/super_mage_death_anim_f9.png"),
                      pygame.image.load("assets/frames/Boss/super_mage_death_anim_f10.png"),
                      pygame.image.load("assets/frames/Boss/super_mage_death_anim_f11.png"),
                      pygame.image.load("assets/frames/Boss/super_mage_death_anim_f12.png"),
                      pygame.image.load("assets/frames/Boss/super_mage_death_anim_f13.png")]}


def get_greenhead_minion_sprite(name):
    return {"attack": [pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f0.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f1.png"),
                     pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f2.png"),
                     # pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f3.png"),
                     # pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f4.png"),
                     # pygame.image.load("assets/frames/Boss/" + name + "_attack_anim_f5.png")
                        ]}

def get_wizard_projectile_sprite():
    return {"idle": [pygame.image.load("assets/frames/Boss/z_projectile.png")]}

enemy_bite = [pygame.image.load("assets/frames/enemy_attacks/bite_f0.png"),
                pygame.image.load("assets/frames/enemy_attacks/bite_f1.png"),
                pygame.image.load("assets/frames/enemy_attacks/bite_f2.png"),
                pygame.image.load("assets/frames/enemy_attacks/bite_f3.png"),
                pygame.image.load("assets/frames/enemy_attacks/bite_f4.png")]


special_cast = [pygame.image.load("assets/frames/special_moves/special_cast_f0.png"),
                pygame.image.load("assets/frames/special_moves/special_cast_f1.png"),
                pygame.image.load("assets/frames/special_moves/special_cast_f2.png"),
                pygame.image.load("assets/frames/special_moves/special_cast_f3.png"),
                pygame.image.load("assets/frames/special_moves/special_cast_f4.png"),
                pygame.image.load("assets/frames/special_moves/special_cast_f5.png")]

def get_green_head_projectile():
    return {"idle": [pygame.image.load("assets/frames/Boss/flame_ball_green.png")]}

def get_potion_sprite(name):
    return {"idle": [pygame.image.load("assets/frames/" + name + ".png")]}

def get_pouch_sprite():
    return [pygame.image.load("./assets/frames/loot_bag.png")]

def get_boss_pouch_sprite():
    return [pygame.image.load("./assets/frames/boss_loot_bag.png")]


def colorize(input_image, color):
    image = input_image.copy()
    image.fill(color, None, pygame.BLEND_RGBA_MULT)
    return image


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LIGHT_RED = (161, 0, 0)
GREEN = (71, 209, 51)
GOLD = (250, 203, 62)
FOV_COLOR = (255, 255, 255)
DARK = (65, 65, 90)
PINK = (255, 0, 127)
BLUE = (0, 172, 238)
