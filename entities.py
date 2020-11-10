from actor import *


class Entity(Actor):
    def __init__(self, game, pos_x, pos_y, sprite, health, shield, has_ai, entity_level, entity_status, move_speed):
        super(Entity, self).__init__(game, pos_x, pos_y, sprite)
        self.max_health = health
        self.max_shield = shield
        self.health = health
        self.shield = shield
        self.has_ai = has_ai
        self.entity_level = entity_level
        self.entity_status = entity_status
        self.move_speed = move_speed
        self.flip_sprite = False

    def move(self, direction):
        if self.can_move(direction):
            self.pos_x += direction[0]
            self.pos_y += direction[1]
            if direction[0] < 0:
                self.flip_sprite = True
            elif direction[0] > 0:
                self.flip_sprite = False
            if direction.length() > 0:
                self.state = "run"
            else:
                self.state = "idle"
