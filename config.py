import pygame

GAME_HEIGHT = 1080
GAME_WIDTH = 1920


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
            "hit": [pygame.image.load("assets/frames/" + name + "_" + gender + "_hit_anim_f0.png")]}


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
            "blast": [pygame.image.load("assets/frames/fx_blast_f0.png"),
                      pygame.image.load("assets/frames/fx_blast_f1.png"),
                      pygame.image.load("assets/frames/fx_blast_f2.png"),
                      pygame.image.load("assets/frames/fx_blast_f3.png")]}


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


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
