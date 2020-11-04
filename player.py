import pygame

from entities import *


class Player(Entity):
    def __init__(self, game, pos_x, pos_y, sprite, health, shield, has_ai, entity_level, entity_status, move_speed,
                 money):
        super(Player, self).__init__(game, pos_x, pos_y, sprite, health, shield, has_ai, entity_level, entity_status,
                                     move_speed)
        self.money = money
        self.held_item = None
        self.items = []

    def use_item(self):
        pass

    def swap_item(self):
        pass

    def get_input(self):
        dx = 0
        dy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        direction = pygame.Vector2(dx, dy)
        if direction.length() > 0:
            direction.scale_to_length(self.move_speed)
        self.move(direction)
        dx, dy = 0, 0

    def mine(self):
        pass
