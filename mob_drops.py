import pygame
import config

class MobDropPouch():
    def __init__(self, game, x, y, items):
        self.items = items
        self.game = game
        self.pos_x = x
        self.pos_y = y
        self.location = (x, y)
        self.sprite = config.get_pouch_sprite()[0]
        self.status = "active"
        self.loot_msg_delay = 20
        self.coins = 0

    def render(self):
        if self.status == "removed":
            self.game.draw_text("Acquired loot: " + self.items_to_string(), 35, config.GAME_WIDTH - 300, config.GAME_HEIGHT - 50)
        else:
            frame_rect = self.sprite.get_rect()
            frame_rect.midbottom = (self.pos_x, self.pos_y)
            if config.is_in_window(frame_rect[0], frame_rect[1]):
                self.game.display.blit(self.sprite, frame_rect)

    def render_loot_msg(self):
        self.game.draw_text("Acquired loot: " + self.items_to_string(), 30, self.game.curr_actors[0].pos_x,
        self.game.curr_actors[0].pos_y - 30)

    def items_to_string(self):
        joined_string = ""
        for item in self.items:
            joined_string += item[0] + " "

        if self.coins > 0:
            joined_string += str(self.coins) + " coin(s)"

        return joined_string



