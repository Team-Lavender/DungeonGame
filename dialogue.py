import pygame
from actor import *
from game import *


class StaticText:

    def __init__(self, game, text, color):
        self.game = game
        self.offset_x = -14  # Change this later
        self.offset_y = -45
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont(None, 25)
        self.coordinates = (0, 0)

    def display_text(self, curr_actors):
        for actor in curr_actors:
            self.coordinates = (actor.pos_x + self.offset_x, actor.pos_y + self.offset_y)
            self.blit_screen(actor)

    def blit_screen(self, actor):
        screen_text = self.font.render(self.text, True, self.color)
        pos = screen_text.get_rect(center=(actor.pos_x, actor.pos_y - 34))
        self.game.window.blit(screen_text, pos)
        pygame.display.update()

    def check_events(self):
        pass
