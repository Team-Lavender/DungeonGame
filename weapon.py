from item import *
from projectile import *
from magic import *


class Weapon(Item):
    def __init__(self, game, name, pos_x, pos_y, sprite, item_level, cost, combat_style, attack_range, dmg, speed,
                 crit_chance):
        super(Weapon, self).__init__(game, pos_x, pos_y, sprite, item_level, cost, combat_style)
        self.name = name
        self.attack_range = attack_range
        self.attack_damage = dmg
        self.attack_speed = speed
        self.crit_chance = crit_chance
        self.target_direction = pygame.Vector2(1, 0)
        self.angle = self.target_direction.angle_to(pygame.Vector2(0, -1))
        self.last_used = 0
        self.weapon_pos = pygame.Rect
        self.weapon_length = self.sprite["idle"][0].get_height()
        self.projectile = ""
        if self.combat_style == "ranged":
            self.projectile = equipment_list.weapons_list[self.name]["projectile"]
        self.slash_frame = 0
        self.slash = False

    def render(self):
        if pygame.time.get_ticks() - self.last_used >= self.attack_speed * 1000:
            self.state = "idle"
        offset = self.target_direction
        offset.scale_to_length(2)
        frame_set = self.sprite[self.state]
        anim_length = len(frame_set)
        self.frame %= anim_length
        curr_frame = frame_set[self.frame]

        frame_rect = curr_frame.get_rect()

        if self.combat_style == "melee" and self.slash:
            swing_fx = self.render_sword_slash()
            swing_rect = swing_fx.get_rect()
            curr_frame = pygame.transform.rotozoom(swing_fx, 90, frame_rect[3] * 1.1 / swing_rect[3])

        frame_rect.center = (self.pos_x, self.pos_y - 10)
        center = ((frame_rect.centerx + offset[0] * frame_rect[3] / 2),
                  (frame_rect.centery + offset[1] * frame_rect[3] / 2))
        if self.update_frame == 0:
            self.frame = (self.frame + 1) % anim_length
        self.update_frame = (self.update_frame + 1) % 1
        curr_frame = pygame.transform.rotate(curr_frame, self.angle)
        new_rect = curr_frame.get_rect()
        new_rect.center = center
        self.weapon_pos = center

        if config.is_in_window(center[0], center[1]) and self.game.curr_actors[0].held_item == self:
            self.game.display.blit(curr_frame, new_rect)

    def ranged_attack(self):
        missile = Projectile(self.game, self.weapon_pos[0], self.weapon_pos[1],
                             config.get_projectile_sprite(self.projectile),
                             self.attack_damage, self.target_direction, self.projectile)
        self.game.curr_actors.append(missile)

    def magic_attack(self):
        lightning = LightningBolt(self.game, self.weapon_pos[0], self.weapon_pos[1], 1, self.attack_damage,
                                  self.attack_range, self.target_direction, self.attack_speed * 1000)

    def render_sword_slash(self):
        swing_frames = config.get_sword_swing_fx()
        anim_length = len(swing_frames)
        curr_frame = swing_frames[self.slash_frame]
        if self.update_frame == 0:
            self.slash_frame = (self.slash_frame + 1) % anim_length
        if self.slash_frame == anim_length - 1:
            self.slash = False
        return curr_frame




