import pygame

GAME_HEIGHT = 720
GAME_WIDTH = 1280

LEVEL1_ROOMS = {1:(0, 0, 'T'), 2:(0, 1, 'E')}
ROOMS_IMG = {'T': 'room_top.png', 'B': 'room_bottom.png', 'R': 'room_right.png', 'L': 'room_left.png', 'E': 'room.png'}

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
    return {"idle": [pygame.image.load("assets/frames/" + name + "_idle_anim_f0.png"),
                     pygame.image.load("assets/frames/" + name + "_idle_anim_f1.png"),
                     pygame.image.load("assets/frames/" + name + "_idle_anim_f2.png"),
                     pygame.image.load("assets/frames/" + name + "_idle_anim_f3.png")],
            "run": [pygame.image.load("assets/frames/" + name + "_run_anim_f0.png"),
                    pygame.image.load("assets/frames/" + name + "_run_anim_f1.png"),
                    pygame.image.load("assets/frames/" + name + "_run_anim_f2.png"),
                    pygame.image.load("assets/frames/" + name + "_run_anim_f3.png")]}


def get_weapon_sprite(name):
    return {"idle": [pygame.image.load("assets/frames/weapon_" + name + ".png")],

            "blast": [colorize(pygame.image.load("assets/frames/weapon_" + name + ".png"), WHITE)]}


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

def get_potion_sprite(name):
    return {"idle": [pygame.image.load("assets/frames/" + name + ".png")]}


def colorize(image, color):
    image.fill(color, None, pygame.BLEND_RGBA_MULT)
    return image


BLACK = (0, 0, 0, 100)
WHITE = (255, 255, 255, 100)
RED = (255, 0, 0, 100)
GREEN = (71, 209, 51)
GOLD = (250, 203, 62)
FOV_COLOR = (255, 255, 255)
DARK = (65, 65, 90)
