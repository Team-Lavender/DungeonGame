import pygame

GAME_HEIGHT = 600
GAME_WIDTH = 800

PLAYER = {"idle": [pygame.image.load("frames/knight_m_idle_anim_f0.png"), pygame.image.load("frames/knight_m_idle_anim_f1.png"), pygame.image.load("frames/knight_m_idle_anim_f2.png"), pygame.image.load("frames/knight_m_idle_anim_f3.png")], "run": [pygame.image.load("frames/knight_m_run_anim_f0.png"), pygame.image.load("frames/knight_m_run_anim_f1.png"), pygame.image.load("frames/knight_m_run_anim_f2.png"), pygame.image.load("frames/knight_m_run_anim_f3.png")]}
SWORD = {"idle": [pygame.image.load("frames/weapon_knight_sword.png")]}

BLACK = (0, 0, 0)