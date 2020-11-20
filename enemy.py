from entities import *
import enemy_lookup
import random
import pygame
import audio

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
        self.last_attack = pygame.time.get_ticks()
        self.last_damaged = pygame.time.get_ticks()
        self.hitbox = self.sprite["idle"][0].get_rect()
        self.width = self.hitbox[2]
        self.height = self.hitbox[3]
        self.sees_target = False
        self.growling = True

    def render_health(self):
        if self.health > 0:
            bar_rect = pygame.Rect(0, 0, self.health, 2)
            bar_rect_red = pygame.Rect(0, 0, self.max_health, 2)
            bar_rect.midleft = (self.pos_x - self.max_health // 2, self.pos_y + 5)
            bar_rect_red.midleft = (self.pos_x - self.max_health // 2, self.pos_y + 5)
            pygame.draw.rect(self.game.display, config.RED, bar_rect_red)
            pygame.draw.rect(self.game.display, config.GREEN, bar_rect)


    def ai(self):

        player = self.game.curr_actors[0]
        self.attack(player)
        if self.sees_target and self.growling:
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
        if 0 < target_vector.length() <= self.vision_radius and not target.invisible:
            self.sees_target = True
            target_vector.scale_to_length(self.move_speed)
            self.move(target_vector)

    def attack(self, target):
        # cant attack until cool-down has passed
        if pygame.time.get_ticks() - self.last_attack >= self.cooldown:
            target_vector = pygame.Vector2(target.pos_x - self.pos_x, target.pos_y - self.pos_y)
            if 0 < target_vector.length() <= self.attack_radius:
                audio.monster_bite()
                target.take_damage(self.damage)
                self.last_attack = pygame.time.get_ticks()

    def take_damage(self, damage):
        if pygame.time.get_ticks() - self.last_damaged >= 60:
            self.health -= damage
            self.is_hit = True
            self.last_hit = pygame.time.get_ticks()
            self.hit_damage = damage
            # random flinch
            self.move(pygame.Vector2(random.randint(-10, 10), random.randint(-10, 10)))
            if self.health <= 0:
                self.entity_status = "dead"
                # add to player score and special ability charge
                self.game.curr_actors[0].score += 50
                self.game.curr_actors[0].special_charge += 10 + (self.game.curr_actors[0].charisma - 10) // 2
                # cap special charge at 100
                self.game.curr_actors[0].special_charge = min(self.game.curr_actors[0].special_charge, 100)

            self.last_damaged = pygame.time.get_ticks()
