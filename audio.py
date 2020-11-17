import pygame
import random


def play_footstep():
    # play random footstep sound
    rand_number = random.randint(0, 9)
    footstep = pygame.mixer.Sound('./assets/audio/soundfx/footsteps/footstep0' + str(rand_number) + '.ogg')
    footstep.set_volume(0.02)
    footstep.play()

def player_health_damage():
    # play random grunt
    rand_number = random.randint(1, 3)
    grunt = pygame.mixer.Sound('./assets/audio/soundfx/interactions/damage_' + str(rand_number) + '.ogg')
    grunt.set_volume(0.05)
    grunt.play()

def player_armor_damage():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/interactions/armor_damage.ogg')
    sound.set_volume(0.05)
    sound.play()

def monster_bite():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/enemy_sounds/monster_bite.ogg')
    sound.set_volume(0.05)
    sound.play()

def monster_growl():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/enemy_sounds/monster_growl.ogg')
    sound.set_volume(0.01)
    sound.play()

def open_door():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/environment/open_door.ogg')
    sound.set_volume(0.1)
    sound.play()

def draw_weapon():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/weapon_sounds/draw_weapon.ogg')
    sound.set_volume(0.5)
    sound.play()

def sheathe_weapon():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/weapon_sounds/sheathe_weapon.ogg')
    sound.set_volume(0.5)
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
    sound.set_volume(0.3)
    sound.play()

def arrow_hit():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/weapon_sounds/arrow_hit.ogg')
    sound.set_volume(0.3)
    sound.play()

def arrow_wall_hit():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/weapon_sounds/arrow_wall_hit.ogg')
    sound.set_volume(0.05)
    sound.play()

def magic_spell_cast():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/weapon_sounds/magic_spell.ogg')
    sound.set_volume(0.05)
    sound.play()

def electricity_zap():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/magic/electricity_zap.ogg')
    sound.set_volume(0.03)
    sound.play()

def drink_potion():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/interactions/drink_potion.ogg')
    sound.set_volume(0.05)
    sound.play()

def shield_up():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/interactions/shield_up.ogg')
    sound.set_volume(0.05)
    sound.play()

def heal_up():
    sound = pygame.mixer.Sound('./assets/audio/soundfx/interactions/heal_up.ogg')
    sound.set_volume(0.05)
    sound.play()