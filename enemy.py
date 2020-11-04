from entities import *


class Enemy(Entity):

    def __init__(self, game, pos_x, pos_y, sprite, health, shield, has_ai, entity_level, entity_status, move_speed):
        super(Enemy, self).__init__(game, pos_x, pos_y, sprite, health, shield, has_ai, entity_level, entity_status,
                                    move_speed)
