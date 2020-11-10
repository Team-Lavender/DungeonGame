import config
from game import *
import math

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

    def render(self):
        frame_set = self.sprite[self.state]
        anim_length = len(frame_set)
        self.frame %= anim_length
        curr_frame = frame_set[self.frame]
        if self.update_frame == 0:
            self.frame = (self.frame + 1) % anim_length
        self.update_frame = (self.update_frame + 1) % 6
        frame_rect = curr_frame.get_rect()
        frame_rect.midbottom = (self.pos_x, self.pos_y)

        if config.is_in_window(frame_rect[0], frame_rect[1]):
            self.game.display.blit(curr_frame, frame_rect)

    def can_move(self, direction):
        if (math.floor(self.pos_x + direction[0]) // 16, math.floor(self.pos_y + direction[1]) // 16) in self.game.curr_map.unpassable:
            return False
        else:
            return True
