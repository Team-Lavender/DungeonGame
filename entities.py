from actor import *
import random

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
        self.is_hit = False
        self.hit_damage = 0
        self.last_hit = pygame.time.get_ticks()

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

    def print_damage_numbers(self, color):
        if pygame.time.get_ticks() - self.last_hit >= 200:
            self.is_hit = False
        damage_int = int(self.hit_damage)
        string = str(damage_int)

        x = self.pos_x
        y = self.pos_y - self.sprite["idle"][0].get_height() - 8
        if self.is_hit:
            self.game.draw_text(string, 25, x, y, color)
