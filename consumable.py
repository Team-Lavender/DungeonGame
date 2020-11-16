from item import *
import equipment_list
import pygame


class Consumable(Item):
    def __init__(self, game, name):
        self.player = game.curr_actors[0]
        self.stats = equipment_list.potions_list[name]
        self.type = self.stats["type"]
        self.size = self.stats["size"]
        # get the sprite for the potion use animation
        if self.type == "shield":
            self.fx_sprite = config.get_potion_fx_sprite("shield_up")
        elif self.type == "heal":
            self.fx_sprite = config.get_potion_fx_sprite("heal_up")
        self.fx_frame = 0
        self.fx_update_frame = True
        self.render_fx_on = False
        self.used = False
        self.consumed = False

        super(Consumable, self).__init__(game, 0, 0,
                                         config.get_potion_sprite(self.stats["sprite_name"]), self.stats["level"],
                                         self.stats["cost"], "none")

    def use(self):
        if not self.used:
            self.used = True
            # render fx, set fx_frame to start of animation
            self.render_fx_on = True
            self.fx_frame = 0
            if self.type == "heal":
                self.heal_up()
            elif self.type == "shield":
                self.shield_up()

    # healing potions heal a player up to their maximum health
    def heal_up(self):
        self.player.health = min(self.player.max_health, self.player.health + self.size)

    # shield potions can provide armor exceeding player equipment maximum
    def shield_up(self):
        self.player.has_shield = True
        self.player.shield += self.size

    def render_fx(self):
        frame_set = self.fx_sprite["idle"]
        anim_length = len(frame_set)

        self.fx_frame %= anim_length
        curr_frame = frame_set[self.fx_frame]
        if self.fx_update_frame:
            self.fx_frame = (self.fx_frame + 1) % anim_length
        if self.fx_frame == 7:
            self.render_fx_on = False
            if self.used:
                self.consumed = True
        self.fx_update_frame = not self.fx_update_frame

        frame_rect = curr_frame.get_rect()
        frame_rect.midbottom = (self.player.pos_x, self.player.pos_y)
        # adjust render position for healing fx
        if self.type == "heal":
            frame_rect.midbottom = (self.player.pos_x, self.player.pos_y + 6)
        if config.is_in_window(frame_rect[0], frame_rect[1]):
            self.game.display.blit(curr_frame, frame_rect)

    # overwrite render method from actor to pass render
    def render(self):
        pass
