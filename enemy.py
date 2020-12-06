from entities import *
import enemy_lookup
import random
import pygame
import audio
import equipment_list
from mob_drops import *
import projectile

class Enemy(Entity):

    def __init__(self, game, pos_x, pos_y, enemy_type, enemy_name):
        self.lookup = enemy_lookup.enemies[enemy_type][enemy_name]
        super(Enemy, self).__init__(game, pos_x, pos_y, config.get_enemy_sprite(enemy_name),
                                    self.lookup[0], self.lookup[1], True, self.lookup[2], "alive",
                                    self.lookup[3])
        self.combat_style = self.lookup[4]
        self.ai_type = self.lookup[5]
        self.vision_radius = self.lookup[6]
        self.attack_radius = self.lookup[7]
        self.damage = self.lookup[8]
        self.cooldown = self.lookup[9]
        self.drops = self.lookup[10]
        self.projectile = ""
        if self.combat_style == "ranged":
            self.projectile = self.lookup[11]
        self.move_direction = random.randint(0, 360)
        self.last_attack = pygame.time.get_ticks()
        self.last_damaged = pygame.time.get_ticks()
        self.hitbox = self.sprite["idle"][0].get_rect()
        self.width = self.hitbox[2]
        self.height = self.hitbox[3]
        # For testing at the moment
        self.sees_target = False
        self.growling = True
        self.has_drop_loot = True
        self.score_when_killed = 50
        self.has_shield = False
        self.biting = False
        if self.shield > 0:
            self.has_shield = True

    def render_health(self):
        health_ratio = 24 / self.max_health
        if self.max_shield > 0:
            shield_ratio = 24 / self.max_shield
        else:
            shield_ratio = 1
        if self.health > 0:
            bar_rect = pygame.Rect(0, 0, self.health * health_ratio, 2)
            bar_rect_red = pygame.Rect(0, 0, self.max_health * health_ratio, 2)
            bar_rect.midleft = (self.pos_x - self.max_health * health_ratio // 2, self.pos_y + 5)
            bar_rect_red.midleft = (self.pos_x - self.max_health * health_ratio // 2, self.pos_y + 5)
            pygame.draw.rect(self.game.display, config.RED, bar_rect_red)
            pygame.draw.rect(self.game.display, config.GREEN, bar_rect)
            if self.shield > 0:
                bar_rect_shield = pygame.Rect(0, 0, self.shield * shield_ratio, 2)
                bar_rect_shield.midleft = (self.pos_x - self.max_health * health_ratio // 2, self.pos_y + 8)
                pygame.draw.rect(self.game.display, config.BLUE, bar_rect_shield)

    def render_attack(self, target):
        frame_set = config.enemy_bite
        anim_length = len(frame_set)
        self.frame %= anim_length



        curr_frame = frame_set[self.frame]
        if self.update_frame == 0 or self.update_frame == len(frame_set) // 2:
            self.frame = (self.frame + 1) % anim_length
            if self.frame == len(frame_set) - 1:
                self.biting = False
        self.update_frame = (self.update_frame + 1) % 6
        frame_rect = curr_frame.get_rect()
        frame_rect.midbottom = (target.pos_x, target.pos_y + 16)
        if self.flip_sprite:
            curr_frame = pygame.transform.flip(curr_frame, True, False)

        if config.is_in_window(frame_rect[0], frame_rect[1]):
            self.game.display.blit(curr_frame, frame_rect)

    def ai(self):

        player = self.game.curr_actors[0]
        if self.combat_style == "ranged" and not player.invisible:
            self.ranged_attack(player)
        self.attack(player)
        if self.sees_target:
            player.in_combat = True
            if self.growling:
                # make a single growl on seeing player
                audio.monster_growl()
                self.growling = False
        if self.ai_type == "smart":
            # A* pathfinding
            pass
        elif self.ai_type == "dumb":
            # linear pathfinding
            self.linear_path(player)
        elif self.ai_type == "patrol":
            # predefined route
            pass

    def linear_path(self, target):
        target_vector = pygame.Vector2(target.pos_x - self.pos_x, target.pos_y - self.pos_y)
        if self.combat_style == "ranged" and 0 < target_vector.length() <= self.vision_radius and not target.invisible:
            self.sees_target = True
            if 0 < target_vector.length() <= self.vision_radius // 4:
                target_vector.scale_to_length(self.move_speed)
                self.move(target_vector)

        elif 0 < target_vector.length() <= self.vision_radius and not target.invisible:
            self.sees_target = True
            target_vector.scale_to_length(self.move_speed)
            self.move(target_vector)
        else:
            angle = self.move_direction
            move_vector = pygame.Vector2(1,1)
            move_vector.from_polar((self.move_speed, angle))
            self.move(move_vector)
            if not self.can_move(move_vector):
                self.update_move_direction()

    def update_move_direction(self):
        self.move_direction = random.randint(0, 360)

    def attack(self, target):
        # cant attack until cool-down has passed
        if pygame.time.get_ticks() - self.last_attack >= self.cooldown:

            target_vector = pygame.Vector2(target.pos_x - self.pos_x, target.pos_y - self.pos_y)
            if 0 < target_vector.length() <= self.attack_radius:
                audio.monster_bite()
                self.biting = True
                target.take_damage(self.damage)
                self.last_attack = pygame.time.get_ticks()

    def ranged_attack(self, target):
        if pygame.time.get_ticks() - self.last_attack >= self.cooldown:
            target_vector = pygame.Vector2(target.pos_x - self.pos_x, target.pos_y - self.pos_y)
            if self.vision_radius // 2 < target_vector.length() <= self.vision_radius:
                missile = projectile.Projectile(self.game, self.pos_x, self.pos_y,
                                     config.get_projectile_sprite(self.projectile),
                                     self.damage, target_vector, self.projectile, True, 3)
                self.game.curr_actors.append(missile)

                self.last_attack = pygame.time.get_ticks()

    def take_damage(self, damage):
        if pygame.time.get_ticks() - self.last_damaged >= 60:
            if self.shield > 0:
                self.shield -= damage
                audio.player_armor_damage()
            if self.shield <= 0 and self.has_shield:
                temp = damage + self.shield
                damage -= temp
                self.shield = 0
                self.has_shield = False
            if not self.has_shield:
                self.health -= damage

            self.is_hit = True
            self.last_hit = pygame.time.get_ticks()
            self.hit_damage = damage
            # random flinch
            flinch_direction = pygame.Vector2(random.randint(-4, 4), random.randint(-4, 4))
            if self.can_move(flinch_direction):
                self.move(flinch_direction)
            if self.health <= 0:
                self.entity_status = "dead"
                # add to player score and special ability charge
                self.game.curr_actors[0].score += self.score_when_killed
                self.game.curr_actors[0].xp += math.ceil(self.score_when_killed * max(self.entity_level / self.game.curr_actors[0].entity_level, 1))
                self.game.curr_actors[0].special_charge += 10 + (self.game.curr_actors[0].charisma - 10) // 2
                # cap special charge at 100
                self.game.curr_actors[0].special_charge = min(self.game.curr_actors[0].special_charge, 100)

            self.last_damaged = pygame.time.get_ticks()



    def mob_drop(self):
        #TODO: add randomised quantity for coins
        pouch = []
        rnd = random.randint(0, 100)
        quantity_chance = random.randrange(0, 5)
        for item in self.drops:
            if item == "coins":
                coins_dropped = self.drops.get(item) * quantity_chance
                if coins_dropped != 0:
                    pouch.append(self.item_lookup(item, coins_dropped))
            elif self.drops.get(item) > rnd:
                pouch.append(self.item_lookup(item, 1))

        if len(pouch) != 0:
            # Create a pouch object
            self.game.mob_drops.append(MobDropPouch(self.game, self.pos_x, self.pos_y, pouch))
            audio.pouch_dropped()


    def item_lookup(self, item_name, quantity):
        if item_name in equipment_list.weapons_list:
            return [item_name, quantity, "weapon"]
        elif item_name in equipment_list.potions_list:
            return [item_name, quantity, "potion"]
        elif item_name in equipment_list.throwables_list:
            return [item_name, quantity, "throwable"]
        elif item_name == "coins":
            return [item_name, quantity]


