from game import *
from enemy import *
from entities import *
import pygame
import audio


class Explosion:
    def __init__(self, game, damage, size, pos_x, pos_y):
        self.game = game
        self.damage = damage
        self.size = size
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.sprite = config.get_magic_sprite("explosion")["idle"]
        # height is size times 2 times a cell width
        self.height = self.size * 16 * 2
        self.width = self.height * 114 / 64 # aspect ratio of explosion
        self.frame = 0
        self.update_frame = 0
        self.rendering = True
        self.explosion()
        self.game.elemental_surfaces.append(self)

    def explosion(self):
        for actor in self.game.curr_actors:
            if isinstance(actor, Entity):
                if abs(actor.pos_x - self.pos_x) <= self.width / 2 and abs(
                        actor.pos_y - self.pos_y) <= self.height / 2:
                    actor.take_damage(self.damage)
        audio.explosion()

    def render(self):

        frames = self.sprite
        anim_length = len(frames)

        # render animation if it exists
        if frames is not None:
            curr_frame = frames[self.frame]
            curr_height = curr_frame.get_height()
            curr_frame = pygame.transform.scale(curr_frame, (round(curr_frame.get_width() * self.height / curr_height), round(self.height)))
            frame_rect = curr_frame.get_rect()
            frame_rect.center = (self.pos_x, self.pos_y)
            self.game.display.blit(curr_frame, frame_rect)

        if self.update_frame == 0:
            self.frame = (self.frame + 1) % anim_length
        if self.frame == anim_length - 1:
            self.game.elemental_surfaces.remove(self)

class AcidPool:
    def __init__(self, game, damage, size, pos_x, pos_y):
        self.game = game
        self.damage = damage
        self.size = size
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.sprite = config.get_magic_sprite("acid_pool")["idle"]
        # height is size times 2 times a cell width
        self.height = self.size * 16 * 2
        self.width = self.height * 114 / 64 # aspect ratio of pool
        self.frame = 0
        self.loop = 0
        self.loops = 6 # number of times the animation is applied and surface exists
        self.update_frame = 0
        self.rendering = True
        self.game.elemental_surfaces.append(self)

    def melt(self):
        for actor in self.game.curr_actors:
            if isinstance(actor, Entity):
                if abs(actor.pos_x - self.pos_x) <= self.width / 2 and abs(
                        actor.pos_y - self.pos_y) <= self.height / 2:
                    actor.take_damage(self.damage)
                    audio.melt()

    def render(self):

        frames = self.sprite
        anim_length = len(frames)

        # render animation if it exists
        if frames is not None:
            curr_frame = frames[self.frame]
            curr_height = curr_frame.get_height()
            curr_frame = pygame.transform.scale(curr_frame, (round(self.width), round(self.height)))
            frame_rect = curr_frame.get_rect()
            frame_rect.center = (self.pos_x, self.pos_y)
            self.game.display.blit(curr_frame, frame_rect)

        if self.update_frame == 0:
            self.frame = (self.frame + 1) % anim_length


        if self.frame == anim_length - 1:
            self.loop += 1
            # apply damage every loop
            self.melt()
        if self.loop == self.loops:
            self.game.elemental_surfaces.remove(self)

class Tentacle:
    def __init__(self, game, damage, size, pos_x, pos_y):
        self.game = game
        self.damage = damage
        self.size = size
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.sprite = config.get_tentacle_sprite("tenticles")["idle"]
        # height is size times 2 times a cell width
        self.height = self.size * 16
        self.width = self.height * 114 / 64  # aspect ratio of explosion
        self.frame = 0
        self.update_frame = 0
        self.rendering = True
        self.tentacle_attack()
        self.game.elemental_surfaces.append(self)

    def tentacle_attack(self):
        for actor in self.game.curr_actors:
            if isinstance(actor, Entity):
                if abs(actor.pos_x - self.pos_x) <= self.width / 2 and abs(
                        actor.pos_y - self.pos_y) <= self.height / 2:
                    actor.take_damage(self.damage)
        # TODO add tentacle audio
        audio.explosion()

    def render(self):

        frames = self.sprite
        anim_length = len(frames)
        # render animation if it exists
        if frames is not None:
            curr_frame = frames[self.frame]
            curr_height = curr_frame.get_height()
            curr_frame = pygame.transform.scale(curr_frame, (
            round(curr_frame.get_width() * ((self.height) / curr_height)), round(self.height)))
            frame_rect = curr_frame.get_rect()
            frame_rect.center = (self.pos_x, self.pos_y)
            self.game.display.blit(curr_frame, frame_rect)
        if self.update_frame == 0:
            self.frame = (self.frame + 1) % anim_length
        if self.frame == anim_length - 1:
            self.game.elemental_surfaces.remove(self)