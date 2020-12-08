import pygame
import config
import equipment_list

class MobDropPouch():
    def __init__(self, game, x, y, items, enemy_type):
        self.items = items
        self.game = game
        self.pos_x = x
        self.pos_y = y
        self.enemy_type = "Regular"
        self.location = (x, y)
        if enemy_type == "Regular":
            self.sprite = config.get_pouch_sprite()[0]
        else:
            self.sprite = config.get_boss_pouch_sprite()[0]
        self.status = "active"
        self.loot_msg_delay = 25
        self.coins = 0

    def render(self):
        if self.status == "removed":
            self.game.draw_text("Acquired loot: ", 32, config.GAME_WIDTH - 300, config.GAME_HEIGHT - 65)
            self.game.draw_text(self.items_to_string(), 32, config.GAME_WIDTH - 300, config.GAME_HEIGHT - 40, config.GOLD)
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
            if item[0] in equipment_list.weapons_list:
                joined_string += equipment_list.weapons_list.get(item[0]).get("name") + " , "
            elif item[0] in equipment_list.throwables_list:
                joined_string += equipment_list.throwables_list.get(item[0]).get("name") + " , "
            elif item[0] in equipment_list.potions_list:
                joined_string += equipment_list.potions_list.get(item[0]).get("name") + " , "

        if self.coins > 0:
            joined_string += str(self.coins) + " coin(s)"
        else:
            joined_string = joined_string.rstrip(', ')

        return joined_string



