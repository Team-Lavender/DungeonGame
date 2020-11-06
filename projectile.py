from enemy import *
import pygame


class Projectile(Actor):
    def __init__(self, game, pos_x, pos_y, sprite, damage, direction):
        super(Projectile, self).__init__(game, pos_x, pos_y, sprite, state="idle")
        self.damage = damage
        self.direction = direction
        self.hit = False

    def move(self, move_speed):
        direction = self.direction
        direction.scale_to_length(move_speed)
        self.pos_x += direction[0]
        self.pos_y += direction[1]
        for actor in self.game.curr_actors:
            if isinstance(actor, Enemy):
                distance_vector = pygame.Vector2(actor.pos_x - self.pos_x, actor.pos_y - self.pos_y)
                if 0 < distance_vector.length() <= 75:
                    target_vector = pygame.Vector2(distance_vector[0], distance_vector[1])
                    target_vector.scale_to_length(0.5)
                    self.pos_x += target_vector[0]
                    self.pos_y += target_vector[1]
                if 0 < distance_vector.length() <= 25:
                    actor.take_damage(self.damage)
                    self.hit = True

    def render(self):
        angle = self.direction.angle_to(pygame.Vector2(0, -1))
        frame_set = self.sprite[self.state]
        anim_length = len(frame_set)
        self.frame %= anim_length
        curr_frame = frame_set[self.frame]

        if self.update_frame == 0:
            self.frame = (self.frame + 1) % anim_length
        self.update_frame = (self.update_frame + 1) % 6

        curr_frame = pygame.transform.rotate(curr_frame, angle)
        frame_rect = curr_frame.get_rect()
        frame_rect.center = (self.pos_x, self.pos_y)

        if config.is_in_window(frame_rect[0], frame_rect[1]):
            self.game.display.blit(curr_frame, frame_rect)