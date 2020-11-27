import pygame
from actor import *
from game import *


class StaticText:

    def __init__(self, game,  color):
        self.game = game
        self.offset_x = -14  # Change this later
        self.offset_y = -45
        self.color = color
        self.font = pygame.font.Font(self.game.font_name, 25)
        self.coordinates = (0, 0)

    def display_text(self, curr_actors):
        self.coordinates = (curr_actors[0].pos_x + self.offset_x, curr_actors[0].pos_y + self.offset_y)
        self.blit_screen(curr_actors[0])

    # Generic function to display text for any actor
    def display_text_dialogue(self, actor, text):
        self.coordinates = (actor.pos_x + self.offset_x, actor.pos_y + self.offset_y)
        screen_text = self.font.render(text, True, self.color)
        pos = screen_text.get_rect(center=(actor.pos_x, actor.pos_y - 34))
        self.game.window.blit(screen_text, pos)

    def blit_screen(self, actor):
        screen_text = self.font.render(self.text, True, self.color)
        pos = screen_text.get_rect(center=(actor.pos_x, actor.pos_y - 34))
        self.game.window.blit(screen_text, pos)

    def check_events(self):
        pass

