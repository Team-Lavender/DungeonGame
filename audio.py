import pygame
import random


class MusicMixer:
    def __init__(self, volume):
        self.battle_theme = pygame.mixer.Sound('./assets/audio/music/battle_theme.wav')
        self.battle_theme.set_volume(0)
        self.battle_theme.play(-1)
        self.underworld_theme = pygame.mixer.Sound('assets/audio/music/underworld_theme.wav')
        self.underworld_theme.set_volume(0)
        self.underworld_theme.play(-1)
        self.menu_theme = pygame.mixer.Sound('./assets/audio/music/menu_theme.wav')
        self.menu_theme.set_volume(0)
        self.menu_theme.play(-1)
        # volume is percentage volume
        self.volume = volume
        self.max_volume = 0.3

        # the following functions set their respective music volume to the game volume and set the other music to 0

    def play_overworld_theme(self):
        pass
    def play_battle_theme(self):
        self.battle_theme.set_volume(self.max_volume * self.volume / 100)
        self.underworld_theme.set_volume(0)
        self.menu_theme.set_volume(0)
    def play_underworld_theme(self):
        self.battle_theme.set_volume(0)
        self.underworld_theme.set_volume(self.max_volume * self.volume / 100)
        self.menu_theme.set_volume(0)
    def play_menu_theme(self):
        self.battle_theme.set_volume(0)
        self.underworld_theme.set_volume(0)
        self.menu_theme.set_volume(self.max_volume * self.volume / 100)
    def play_boss_theme(self):
        pass
    def change_volume(self, new_volume):
        self.volume = new_volume

def menu_select():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/interactions/armor_damage.ogg')
    sound.set_volume(0.07)
    sound.play()

def menu_back():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/weapon_sounds/sword_hit.ogg')
    sound.set_volume(0.1)
    sound.play()

def menu_move():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/weapon_sounds/sheathe_weapon.ogg')
    sound.set_volume(0.3)
    sound.play()

def menu_type():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/weapon_sounds/draw_weapon.ogg')
    sound.set_volume(0.5)
    sound.play()


def play_footstep():
    # play random footstep sound
    rand_number = random.randint(0, 9)
    footstep = pygame.mixer.Sound('./assets/audio/soundfx/footsteps/footstep0' + str(rand_number) + '.ogg')
    footstep.set_volume(0.01)
    footstep.play()

def player_health_damage():
    # play random grunt
    rand_number = random.randint(1, 3)
    grunt = pygame.mixer.Sound('./assets/audio/soundfx/interactions/damage_' + str(rand_number) + '.ogg')
    grunt.set_volume(0.07)
    grunt.play()

def player_armor_damage():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/interactions/armor_damage.ogg')
    sound.set_volume(0.07)
    sound.play()

def level_up():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/interactions/level_up.ogg')
    sound.set_volume(0.1)
    sound.play()

def monster_bite():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/enemy_sounds/monster_bite.ogg')
    sound.set_volume(0.1)
    sound.play()

def monster_growl():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/enemy_sounds/monster_growl.ogg')
    sound.set_volume(0.03)
    sound.play()

def open_door():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/environment/open_door.ogg')
    sound.set_volume(0.07)
    sound.play()

def pouch_dropped():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/environment/bag_drop.ogg')
    sound.set_volume(0.07)
    sound.play()

def coin_pickup():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/interactions/coin_pickup.ogg')
    sound.set_volume(0.07)
    sound.play()

def draw_weapon():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/weapon_sounds/draw_weapon.ogg')
    sound.set_volume(0.7)
    sound.play()

def sheathe_weapon():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/weapon_sounds/sheathe_weapon.ogg')
    sound.set_volume(0.7)
    sound.play()

def sword_swing():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/weapon_sounds/sword_swing.ogg')
    sound.set_volume(0.3)
    sound.play()

def sword_hit():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/weapon_sounds/sword_hit.ogg')
    sound.set_volume(0.1)
    sound.play()

def arrow_launch():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/weapon_sounds/arrow_launch.ogg')
    sound.set_volume(0.1)
    sound.play()

def arrow_hit():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/weapon_sounds/arrow_hit.ogg')
    sound.set_volume(0.1)
    sound.play()

def arrow_wall_hit():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/weapon_sounds/arrow_wall_hit.ogg')
    sound.set_volume(0.07)
    sound.play()

def magic_spell_cast():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/weapon_sounds/magic_spell.ogg')
    sound.set_volume(0.1)
    sound.play()

def electricity_zap():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/magic/electricity_zap.ogg')
    sound.set_volume(0.05)
    sound.play()

def explosion():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/magic/explosion.ogg')
    sound.set_volume(0.05)
    sound.play()

def melt():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/magic/melt.ogg')
    sound.set_volume(0.03)
    sound.play()

def throw():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/interactions/throw.ogg')
    sound.set_volume(0.1)
    sound.play()

def bottle_break():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/interactions/bottle_break.ogg')
    sound.set_volume(0.1)
    sound.play()


def drink_potion():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/interactions/drink_potion.ogg')
    sound.set_volume(0.07)
    sound.play()

def shield_up():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/interactions/shield_up.ogg')
    sound.set_volume(0.05)
    sound.play()

def heal_up():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/interactions/heal_up.ogg')
    sound.set_volume(0.05)
    sound.play()

def super_up():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/interactions/super_up.ogg')
    sound.set_volume(0.05)
    sound.play()

def special_move():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/interactions/special_move.ogg')
    sound.set_volume(0.07)
    sound.play()

def critical_attack():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/interactions/critical_attack.ogg')
    sound.set_volume(0.3)
    sound.play()

