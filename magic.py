from enemy import *
import math

class LightningBolt(Actor):
    def __init__(self, game, pos_x, pos_y, forks, damage, attack_range, direction, time):
        super(LightningBolt, self).__init__(game, pos_x, pos_y, config.get_magic_sprite("lightning"), state="idle")
        self.forks = forks
        self.damage = damage
        self.direction = direction
        self.direction.scale_to_length(attack_range)
        self.attack_range = attack_range
        self.time = time
        self.last_used = pygame.time.get_ticks()
        self.zap()

    def zap(self):
        if self.forks <= 0:
            return

        for actor in self.game.curr_actors:
            if isinstance(actor, Enemy):
                target_vector = pygame.Vector2(actor.pos_x - self.pos_x,  actor.pos_y - self.pos_y)
                if 0 < target_vector.length() <= self.attack_range:

                    if target_vector.angle_to(self.direction) <= 20:
                        self.direction.scale_to_length(target_vector.length())
                        actor.take_damage(self.damage)
                        for next_actor in self.game.curr_actors:
                            if isinstance(next_actor, Enemy):
                                new_target_vector = pygame.Vector2(next_actor.pos_x - actor.pos_x, next_actor.pos_y - actor.pos_y)
                                if 0 < new_target_vector.length() <= self.attack_range:
                                    bolt = LightningBolt(self.game, actor.pos_x, actor.pos_y, self.forks - 1, self.damage // 2, new_target_vector.length(), new_target_vector, self.time)
                                    self.game.curr_actors.append(bolt)

                break



    def render(self):

        if pygame.time.get_ticks() - self.last_used >= self.time:
            self.game.curr_actors.remove(self)
        frame_set = self.sprite[self.state]
        anim_length = len(frame_set)
        self.frame %= anim_length
        curr_frame = frame_set[self.frame]
        frame_rect = curr_frame.get_rect()

        scale = max(self.direction.length() / frame_rect[3], 0.1)

        frame_rect.center = (self.pos_x, self.pos_y)
        center = ((frame_rect.centerx + self.direction.normalize()[0] * scale * frame_rect[3] / 2),
                  (frame_rect.centery + self.direction.normalize()[1] * scale * frame_rect[3] / 2))
        if self.update_frame == 0:
            self.frame = (self.frame + 1) % anim_length
        self.update_frame = (self.update_frame + 1) % 6
        angle = self.direction.angle_to(pygame.Vector2(0, 1))
        curr_frame = pygame.transform.rotozoom(curr_frame, angle, scale)
        new_rect = curr_frame.get_rect()
        new_rect.center = center

        if config.is_in_window(center[0], center[1]):
            self.game.display.blit(curr_frame, new_rect)
