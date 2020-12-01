from enemy import *
from player import *
import pygame
import audio
import elemental_effects
import math

class Projectile(Actor):
    def __init__(self, game, pos_x, pos_y, sprite, damage, direction, projectile_type, hits_player=False, move_speed=8):
        super(Projectile, self).__init__(game, pos_x, pos_y, sprite, state="idle")
        self.damage = damage
        self.direction = direction
        self.projectile_type = projectile_type
        self.move_speed = move_speed
        self.hits_player = hits_player
        self.hit = False
        self.hit_wall = False
        self.time_in_wall = pygame.time.get_ticks()

    def move(self, move_speed):
        direction = self.direction
        direction.scale_to_length(move_speed)
        if self.can_move(direction):
            self.pos_x += direction[0]
            self.pos_y += direction[1]

            for actor in self.game.curr_actors:
                if (isinstance(actor, Enemy) and not self.hits_player) or (isinstance(actor, Player) and self.hits_player):
                    distance_vector = (actor.pos_x - self.pos_x, actor.pos_y - actor.height // 2 - self.pos_y)

                    if not self.hit and abs(distance_vector[1]) <= actor.height // 2 and abs(
                            distance_vector[0]) <= actor.width // 2:
                        actor.take_damage(self.damage)
                        self.hit = True
                        if self.projectile_type == "fireball" or self.projectile_type == "acid":
                            pass
                        else:
                            # play hit sound
                            audio.arrow_hit()
                        self.on_hit()
        else:
            if not self.hit_wall:
                self.time_in_wall = pygame.time.get_ticks()
                self.hit_wall = True
                self.on_hit()
                if self.projectile_type == "fireball" or self.projectile_type == "acid":
                    self.hit = True
                else:
                    audio.arrow_wall_hit()
            else:
                if pygame.time.get_ticks() - self.time_in_wall >= 2000:
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

    def on_hit(self):
        if self.projectile_type == "fireball":
            self.explosion()
        elif self.projectile_type == "acid":
            self.acid_pool()
        else:
            pass

    def explosion(self):
        elemental_effects.Explosion(self.game, math.ceil(self.damage * 0.5), 1.5, self.pos_x, self.pos_y)

    def acid_pool(self):
        elemental_effects.AcidPool(self.game, math.ceil(self.damage * 0.1), 0.8, self.pos_x, self.pos_y)
