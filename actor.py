import config
from game import *
import math
import pygame


class Actor:
    def __init__(self, game, pos_x, pos_y, sprite, state="idle"):
        self.game = game
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.sprite = sprite
        self.state = state
        self.frame = 0
        self.update_frame = 0
        self.game.curr_actors.append(self)
        self.flip_sprite = False

        # makes actor untargetable by ai an changes sprite to transparent
        self.invisible = False

    def render(self):
        frame_set = self.sprite[self.state]
        anim_length = len(frame_set)
        self.frame %= anim_length

        if self.invisible:
            curr_frame = config.colorize(frame_set[self.frame], config.DARK)
        else:
            curr_frame = frame_set[self.frame]
        if self.update_frame == 0:
            self.frame = (self.frame + 1) % anim_length
        self.update_frame = (self.update_frame + 1) % 6
        frame_rect = curr_frame.get_rect()
        frame_rect.midbottom = (self.pos_x, self.pos_y)
        if self.flip_sprite:
            curr_frame = pygame.transform.flip(curr_frame, True, False)

        if config.is_in_window(frame_rect[0], frame_rect[1]):
            self.game.display.blit(curr_frame, frame_rect)

    def can_move(self, direction):
        if (math.floor(self.pos_x + direction[0]) // 16,
            math.floor(self.pos_y + direction[1]) // 16) in self.game.curr_map.unpassable:
            return False
        else:
            return True
