from enemy import *
from boss import *
from player import *
import pygame
import audio
import elemental_effects
import math
import magic

class Projectile(Actor):
    def __init__(self, game, pos_x, pos_y, sprite, damage, direction, projectile_type, hits_player=False, move_speed=8):
        super(Projectile, self).__init__(game, pos_x, pos_y, sprite, state="idle")
        self.damage = damage
        self.direction = direction
        self.projectile_type = projectile_type
        self.hits = 3
        self.move_speed = move_speed
        self.hits_player = hits_player
        self.hit = False
        self.hit_wall = False
        self.time_in_wall = pygame.time.get_ticks()
        self.last_hit = pygame.time.get_ticks()
        self.hitbox = self.sprite["idle"][0].get_rect()
        self.width = self.hitbox[2]
        self.height = self.hitbox[3]
        if self.projectile_type == "split_arrow":
            # create sub projectiles
            extra_1 = Projectile(game, pos_x, pos_y, sprite, damage, direction, "standard_arrow", hits_player, move_speed)
            extra_2 = Projectile(game, pos_x, pos_y, sprite, damage, direction, "standard_arrow", hits_player, move_speed)
            extra_1.direction = extra_1.direction.rotate(5)
            extra_2.direction = extra_2.direction.rotate(-5)
            self.game.curr_actors.append(extra_1)
            self.game.curr_actors.append(extra_2)
        self.seeking = False
        if self.projectile_type == "seeking_arrow" or self.projectile_type == "magic_hammer":
            self.seeking = True
        self.returning = False


    def move(self, move_speed):
        self.seek_mouse()
        self.return_weapon()
        direction = self.direction
        direction.scale_to_length(move_speed)

        if self.can_move(direction) or self.returning:
            self.pos_x += direction[0]
            self.pos_y += direction[1]

            for actor in self.game.curr_actors:
                if (isinstance(actor, (Enemy, WizardBoss, MageBoss)) and not self.hits_player) or (isinstance(actor, Player) and self.hits_player):
                    distance_vector = (actor.pos_x - self.pos_x, actor.pos_y - actor.height // 2 - self.pos_y)

                    if not self.hit and abs(distance_vector[1]) <= actor.height // 2 and abs(
                            distance_vector[0]) <= actor.width // 2 + self.width // 2:
                        actor.take_damage(self.damage)
                        if pygame.time.get_ticks() - self.last_hit >= 60 and self.projectile_type != "magic_hammer":
                            self.hit = True
                        if self.projectile_type == "fireball" or self.projectile_type == "acid":
                            pass
                        else:
                            # play hit sound
                            audio.arrow_hit()
                        if pygame.time.get_ticks() - self.last_hit >= 60:
                            self.last_hit = pygame.time.get_ticks()
                            self.on_hit()
                            self.hits -= 1
        else:
            if not self.hit_wall:
                self.time_in_wall = pygame.time.get_ticks()
                self.hit_wall = True
                self.seeking = False
                if pygame.time.get_ticks() - self.last_hit >= 60:
                    self.last_hit = pygame.time.get_ticks()
                    self.on_hit()
                    self.hits -= 1
                if self.projectile_type == "fireball" or self.projectile_type == "acid":
                    self.hit = True
                else:
                    audio.arrow_wall_hit()
            else:
                if pygame.time.get_ticks() - self.time_in_wall >= 2000 and self.projectile_type != "magic_hammer":
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
        elif self.projectile_type == "ricochet_arrow":
            self.ricochet()
        elif self.projectile_type == "magic_hammer":
            self.lightning()
        elif self.projectile_type == "bounce_wall":
            self.bounce_wall()
        elif self.projectile_type == "tenticles":
            self.tentacle()
        elif self.projectile_type is None:
            pass
        else:
            pass

    def explosion(self):
        elemental_effects.Explosion(self.game, math.ceil(self.damage * 0.5), 1.5, self.pos_x, self.pos_y)

    def acid_pool(self):
        elemental_effects.AcidPool(self.game, math.ceil(self.damage * 0.1), 0.8, self.pos_x, self.pos_y)

    def lightning(self):
        for actor in self.game.curr_actors:
            if (isinstance(actor, Enemy) and not self.hits_player) or (isinstance(actor, Player) and self.hits_player):
                distance_vector = pygame.Vector2(actor.pos_x - self.pos_x, actor.pos_y - actor.height // 2 - self.pos_y)
                if 100 >= distance_vector.length():
                    direction = distance_vector
                    actor.take_damage(max(1, self.damage // 4))
                    audio.electricity_zap()
                    magic.LightningBolt(self.game, self.pos_x, self.pos_y, 0, 0,
                                                   100, direction, 0.1 * 1000)


    def tentacle(self):
        if not self.hit_wall:
            elemental_effects.Tentacle(self.game, self.damage, 2, self.pos_x, self.pos_y)

    def ricochet(self):
        if self.hits > 0:
            self.hit = False
            self.damage = max(2, self.damage // 2)
            for actor in self.game.curr_actors:
                if (isinstance(actor, Enemy) and not self.hits_player) or (isinstance(actor, Player) and self.hits_player):
                    distance_vector = pygame.Vector2(actor.pos_x - self.pos_x, actor.pos_y - actor.height // 2 - self.pos_y)
                    if 200 >= distance_vector.length() >= 50:
                        self.direction = distance_vector
                        break

    def bounce_wall(self):
        if self.hits > 0:
            self.hit = False
            self.damage = max(2, self.damage // 2)
            for actor in self.game.curr_actors:
                if (isinstance(actor, Enemy) and not self.hits_player) or (isinstance(actor, Player) and self.hits_player):
                    distance_vector = pygame.Vector2(actor.pos_x - self.pos_x, actor.pos_y - actor.height // 2 - self.pos_y)
                    self.direction = distance_vector
                    break

    # player only
    def seek_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        direction = pygame.Vector2(mouse_pos[0] - self.pos_x, mouse_pos[1] - self.pos_y)
        direction.scale_to_length(0.5)
        if pygame.mouse.get_pressed()[0] and self.seeking and not self.returning:
            self.direction += direction
            self.direction.scale_to_length(self.move_speed)

    # player only
    def return_to_caster(self):
        self.returning = True
        player = self.game.curr_actors[0]
        self.direction = pygame.Vector2(player.pos_x - self.pos_x, player.pos_y - self.pos_y)
        if self.direction.length() <= 50:
            # remove projectile when returned
            self.hit = True
            if player.held_item is not None:
                player.held_item.state = "idle"
            audio.sword_swing()
        self.direction.scale_to_length(self.move_speed * 2)
        # delay weapon cooldown until returned
        if player.held_item is not None:
            player.held_item.last_used = pygame.time.get_ticks()

    def return_weapon(self):
        if self.projectile_type == "magic_hammer":
            # return on mouse release
            if not pygame.mouse.get_pressed()[0] or self.returning:
                self.return_to_caster()