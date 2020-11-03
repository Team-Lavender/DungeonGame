from actor import *


class Entity(Actor):

    def __init__(self, game, pos_x, pos_y, sprite, health, shield, has_ai, entity_level, entity_status, move_speed):
        super(Entity, self).__init__(game, pos_x, pos_y, sprite)
        self.health = health
        self.shield = shield
        self.has_ai = has_ai
        self.entity_level = entity_level
        self.entity_status = entity_status
        self.move_speed = move_speed

    def move(self, direction):
        self.pos_x += direction[0]
        self.pos_y += direction[1]
        if direction.length() > 0:
            self.state = "run"
        else:
            self.state = "idle"

    def attack(self):
        # TODO fill in attack method.
        pass
