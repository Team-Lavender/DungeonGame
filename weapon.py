from item import *
from projectile import *
from magic import *


class Weapon(Item):
    def __init__(self, game, pos_x, pos_y, sprite, item_level, cost, combat_style, attack_range, dmg, speed,
                 crit_chance, projectile=None):
        super(Weapon, self).__init__(game, pos_x, pos_y, sprite, item_level, cost, combat_style)
        self.attack_range = attack_range
        self.attack_damage = dmg
        self.attack_speed = speed
        self.crit_chance = crit_chance
        self.target_direction = pygame.Vector2(1, 0)
        self.angle = self.target_direction.angle_to(pygame.Vector2(0, -1))
        self.in_inventory = True
        self.last_used = pygame.time.get_ticks()
        self.weapon_pos = pygame.Rect
        self.projectile = projectile

    def render(self):
        if pygame.time.get_ticks() - self.last_used >= 400:
            self.state = "idle"
        offset = self.target_direction
        offset.scale_to_length(2)
        frame_set = self.sprite[self.state]
        anim_length = len(frame_set)
        self.frame %= anim_length
        curr_frame = frame_set[self.frame]
        frame_rect = curr_frame.get_rect()
        frame_rect.center = (self.pos_x, self.pos_y - 10)
        center = ((frame_rect.centerx + offset[0] * frame_rect[3] / 2),
                  (frame_rect.centery + offset[1] * frame_rect[3] / 2))
        if self.update_frame == 0:
            self.frame = (self.frame + 1) % anim_length
        self.update_frame = (self.update_frame + 1) % 6
        curr_frame = pygame.transform.rotate(curr_frame, self.angle)
        new_rect = curr_frame.get_rect()
        new_rect.center = center
        self.weapon_pos = center

        if config.is_in_window(center[0], center[1]) and not self.in_inventory:
            self.game.display.blit(curr_frame, new_rect)

    def ranged_attack(self):
        missile = Projectile(self.game, self.weapon_pos[0], self.weapon_pos[1],
                             config.get_projectile_sprite(self.projectile),
                             self.attack_damage, self.target_direction)
        self.game.curr_actors.append(missile)

    def magic_attack(self):
        lightning = LightningBolt(self.game, self.weapon_pos[0], self.weapon_pos[1], 1, self.attack_damage,
                                  self.attack_range, self.target_direction, self.attack_speed * 1000)


