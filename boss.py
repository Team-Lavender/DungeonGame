from entities import *
import boss_lookup
import config
import math
import projectile
from enemy import *

class WizardBoss(Entity):

    # Fix the projectile
    # TODO: proper bogmetric paterns
    # Boss bar  outsource maybe

    def __init__(self, game, pos_x, pos_y, boss_type, boss_name):
        self.lookup = boss_lookup.bosses[boss_type][boss_name]
        super(WizardBoss, self).__init__(game, pos_x, pos_y, config.get_wizard_boss_sprite(boss_name),
                                         self.lookup[0], self.lookup[1], True, self.lookup[2], "alive",
                                         self.lookup[3])
        self.combat_style = self.lookup[4]
        self.ai_type = self.lookup[5]
        self.vision_radius = self.lookup[6]
        self.attack_radius = self.lookup[7]
        self.damage = self.lookup[8]
        self.cooldown = self.lookup[9]
        self.drops = self.lookup[10]
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
        self.target_list = [(1017,261),(990,261)]
        self.curr_target = self.target_list[0]
        self.index = 0
        self.special_damage = 0
        self.attack_cooldown = 150
        self.direction = 0
        self.curr_sprite_index = 0
        self.flip_sprite = False
        self.state = "attack"
        self.death_counter = 0
        self.curr_attack = "single_arrow"
        self.death_animation_done = False
        self.has_shield = False
        self.biting = False
        if self.shield > 0:
            self.has_shield = True



    def ai(self):
        if self.state != "death":
            if self.ai_type == "patrol":
                if pygame.time.get_ticks() - self.last_attack >= self.cooldown:
                    self.current_attack()
                player = self.game.curr_actors[0]
                self.linear_path(player)
        else:
            self.death_animation()

            # if self.attack_cooldown == 0:
            #     #self.spawn_minions()
            #     self.arrow_spray()
            #     self.attack_cooldown =


    def current_attack(self):
        if self.curr_attack == "single_arrow":
            if self.frame == len(self.sprite[self.state]) - 1:
                self.single_arrow()
                self.frame = 0
                self.last_attack = pygame.time.get_ticks()
                self.curr_attack = "multiple_arrow"

        elif self.curr_attack == "multiple_arrow":
            self.arrow_spray()
            self.last_attack = pygame.time.get_ticks()
            self.curr_attack = "spawn_minions"

        elif self.curr_attack == "spawn_minions":
            self.spawn_minions()
            self.last_attack = pygame.time.get_ticks()
            self.curr_attack = "single_arrow"






    def move(self, direction):
        if self.can_move(direction):
            self.pos_x += direction[0]
            self.pos_y += direction[1]
            if direction[0] < 0:
                self.flip_sprite = False
            elif direction[0] > 0:
                self.flip_sprite = True
            # self.game.curr_actors[0] - self.pos_x
            if self.pos_x- self.game.curr_actors[0].pos_x > 0.5 and not self.state == "death" :
                self.state = "attack"
            # else:
            #     self.state = "idle"



    def patrol(self):
        target_vector = pygame.Vector2(self.curr_target[0] - self.pos_x, self.curr_target[1] - self.pos_y)
        if target_vector.length() > 3 :
            self.sees_target = True
            target_vector.scale_to_length(self.move_speed)
            self.move(target_vector)
        else:
            if self.index + 1 == len(self.target_list):
                self.index = 0
                self.curr_target = self.target_list[self.index]
            else:
                self.index += 1
                self.curr_target = self.target_list[self.index]


    def linear_path(self, target):
        target_vector = pygame.Vector2(target.pos_x - self.pos_x, target.pos_y - self.pos_y)
        if 0 < target_vector.length() <= self.vision_radius and not target.invisible:
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


    def arrow_spray(self):
        for angle in range(0, 360, 24):
            direction = pygame.Vector2()
            direction.from_polar((1, angle))
            if self.flip_sprite:
                missile = projectile.Projectile(self.game, self.pos_x + 6, self.pos_y - 40,
                                     config.get_wizard_projectile_sprite(),
                                     self.special_damage, direction, None, True, 8)
            else:
                missile = projectile.Projectile(self.game, self.pos_x - 6, self.pos_y - 40,
                                     config.get_wizard_projectile_sprite(),
                                     self.special_damage, direction, None, True, 8)
            self.game.curr_actors.append(missile)

    def single_arrow(self):
        direction = pygame.Vector2((self.game.curr_actors[0].pos_x - self.pos_x), (self.game.curr_actors[0].pos_y - self.pos_y + 30 ))
        #angle = player_vector.angle_to(pygame.Vector2(0, -1))
        #direction.from_polar((1, angle))
        #print(direction[0])
        # if direction[0]<0:
        #     self.flip_sprite = False
            # missile = Projectile(self.game, self.pos_x, self.pos_y - 40,
            #                      config.get_wizard_projectile_sprite(),
            #                      self.special_damage, direction)
            # self.game.curr_actors.append(missile)
            # print(self.flip_sprite)
        # if direction[0]>0:
            #self.flip_sprite = True
        missile = projectile.Projectile(self.game, self.pos_x, self.pos_y - 40,
                             config.get_wizard_projectile_sprite(),
                             self.special_damage, direction, None, True, 8)
        self.game.curr_actors.append(missile)






    def spawn_minions(self):
        angle_straight = 40
        angle_inbetween = angle_straight * 0.75

        # # right straight
        Enemy(self.game, self.pos_x + angle_straight, self.pos_y, "demon", "chort")
        # # top right
        Enemy(self.game, self.pos_x + angle_inbetween, self.pos_y - angle_inbetween, "demon", "chort")
        # top
        Enemy(self.game, self.pos_x, self.pos_y - angle_straight, "demon", "chort")
        # bottom
        Enemy(self.game, self.pos_x, self.pos_y + angle_straight, "demon", "chort")
        # #middle top left
        Enemy(self.game, self.pos_x - angle_inbetween, self.pos_y- angle_inbetween, "demon", "chort")
        Enemy(self.game, self.pos_x - angle_inbetween, self.pos_y + angle_inbetween, "demon", "chort")
        Enemy(self.game, self.pos_x - angle_straight, self.pos_y, "demon", "chort")
        Enemy(self.game, self.pos_x - angle_inbetween, self.pos_y + angle_inbetween, "demon", "chort")

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
                self.death_animation()

            self.last_damaged = pygame.time.get_ticks()


            # if pygame.time.get_ticks() - self.last_damaged >= 60:
            #     self.health -= damage
            #     self.is_hit = True
            #     self.last_hit = pygame.time.get_ticks()
            #     self.hit_damage = damage
            #     # random flinch
            #     self.move(pygame.Vector2(random.randint(-10, 10), random.randint(-10, 10)))
            #     if self.health <= 0:
            #         self.death_animation()
            #     self.last_damaged = pygame.time.get_ticks()

        # for i in range(6):
        #     angle = i * 30
        #     pos_x = self.pos_x + (5 * math.sin(math.radians(angle)))
        #     pos_y = self.pos_y + (5 * math.cos(math.radians(angle)))
        #     Enemy(self.game, pos_x, pos_y, "demon", "chort")

        #https://answers.unity.com/questions/714835/best-way-to-spawn-prefabs-in-a-circle.html


    def death_animation(self):
        self.state = "death"
        if self.frame == len(self.sprite["death"]) - 1:
            self.death_animation_done = True
        if self.death_animation_done:
            self.entity_status = "dead"
            # add to player score and special ability charge
            self.game.curr_actors[0].score += self.score_when_killed
            self.game.curr_actors[0].xp += self.score_when_killed
            self.game.curr_actors[0].special_charge += 10 + (self.game.curr_actors[0].charisma - 10) // 2
            # cap special charge at 100
            self.game.curr_actors[0].special_charge = min(self.game.curr_actors[0].special_charge, 100)




class MageBoss(Entity):


    def __init__(self, game, pos_x, pos_y, boss_type, boss_name):
        self.lookup = boss_lookup.bosses[boss_type][boss_name]
        super(MageBoss, self).__init__(game, pos_x, pos_y, config.get_super_mage_sprite(boss_name),
                                         self.lookup[0], self.lookup[1], True, self.lookup[2], "alive",
                                         self.lookup[3])
        self.combat_style = self.lookup[4]
        self.ai_type = self.lookup[5]
        self.vision_radius = self.lookup[6]
        self.attack_radius = self.lookup[7]
        self.damage = self.lookup[8]
        self.cooldown = self.lookup[9]
        self.drops = self.lookup[10]
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
        self.target_list = [(1017,261),(990,261)]
        self.curr_target = self.target_list[0]
        self.index = 0
        self.special_damage = 0
        self.attack_cooldown = 150
        self.direction = 0
        self.curr_sprite_index = 0
        self.flip_sprite = False
        self.state = "attack"
        self.death_counter = 0
        self.curr_attack = "single_arrow"
        self.death_animation_done = False
        self.has_shield = False
        self.biting = False
        if self.shield > 0:
            self.has_shield = True




    def ai(self):

        if self.state != "death":
            if self.health < (self.max_health//2):
                self.state = "attack_2"
            if self.ai_type == "patrol":
                if pygame.time.get_ticks() - self.last_attack >= self.cooldown:
                    self.current_attack()
                player = self.game.curr_actors[0]
                self.linear_path(player)
        else:
            self.death_animation()

            # if self.attack_cooldown == 0:
            #     #self.spawn_minions()
            #     self.arrow_spray()
            #     self.attack_cooldown =


    def current_attack(self):
        if self.curr_attack == "single_arrow":
            if self.frame == len(self.sprite[self.state]) - 1:
                self.single_arrow()
                self.frame = 0
                self.last_attack = pygame.time.get_ticks()
                self.curr_attack = "multiple_arrow"

        elif self.curr_attack == "multiple_arrow":
            self.arrow_spray()
            self.last_attack = pygame.time.get_ticks()
            self.curr_attack = "single_arrow"







    def move(self, direction):
        if self.can_move(direction):
            self.pos_x += direction[0]
            self.pos_y += direction[1]
            if direction[0] < 0:
                self.flip_sprite = True
            elif direction[0] > 0:
                self.flip_sprite = False
            # self.game.curr_actors[0] - self.pos_x
            # if self.pos_x - self.game.curr_actors[0].pos_x > 0.5 and not self.state == "death":
            #     self.state = "attack"

            # else:
            #     self.state = "idle"



    def patrol(self):
        target_vector = pygame.Vector2(self.curr_target[0] - self.pos_x, self.curr_target[1] - self.pos_y)
        if target_vector.length() > 3 :
            self.sees_target = True
            target_vector.scale_to_length(self.move_speed)
            self.move(target_vector)
        else:
            if self.index + 1 == len(self.target_list):
                self.index = 0
                self.curr_target = self.target_list[self.index]
            else:
                self.index += 1
                self.curr_target = self.target_list[self.index]


    def linear_path(self, target):
        target_vector = pygame.Vector2(target.pos_x - self.pos_x, target.pos_y - self.pos_y)
        if 0 < target_vector.length() <= self.vision_radius and not target.invisible:
            self.sees_target = True
            target_vector.scale_to_length(self.move_speed)
            self.move(target_vector)
        # else:
        #     angle = self.move_direction
        #     move_vector = pygame.Vector2(1,1)
        #     move_vector.from_polar((self.move_speed, angle))
        #     self.move(move_vector)
        #     if not self.can_move(move_vector):
        #         self.update_move_direction()


    def arrow_spray(self):
        for angle in range(0, 360, 24):
            direction = pygame.Vector2()
            direction.from_polar((1, angle))
            if self.flip_sprite:
                missile = projectile.Projectile(self.game, self.pos_x + 6, self.pos_y - 40,
                                     config.get_super_mage_bomb_sprite(),
                                     self.special_damage, direction, None, True, 8)
            else:
                missile = projectile.Projectile(self.game, self.pos_x - 6, self.pos_y - 40,
                                     config.get_super_mage_bomb_sprite(),
                                     self.special_damage, direction, None, True, 8)
            self.game.curr_actors.append(missile)

    def single_arrow(self):
        direction = pygame.Vector2((self.game.curr_actors[0].pos_x - self.pos_x), (self.game.curr_actors[0].pos_y - self.pos_y + 30 ))
        #angle = player_vector.angle_to(pygame.Vector2(0, -1))
        #direction.from_polar((1, angle))
        #print(direction[0])
        # if direction[0]<0:
        #     self.flip_sprite = False
            # missile = Projectile(self.game, self.pos_x, self.pos_y - 40,
            #                      config.get_wizard_projectile_sprite(),
            #                      self.special_damage, direction)
            # self.game.curr_actors.append(missile)
            # print(self.flip_sprite)
        # if direction[0]>0:
            #self.flip_sprite = True
        if self.flip_sprite:
            missile = projectile.Projectile(self.game, self.pos_x - 50, self.pos_y - 40,
                                 config.get_super_mage_flame_ball(),
                                 self.special_damage, direction, None, True, 8)
        else:
            missile = projectile.Projectile(self.game, self.pos_x + 50, self.pos_y - 40,
                                            config.get_super_mage_flame_ball(),
                                            self.special_damage, direction, None, True, 8)

        self.game.curr_actors.append(missile)






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
                self.death_animation()

            self.last_damaged = pygame.time.get_ticks()

            #
            # if pygame.time.get_ticks() - self.last_damaged >= 60:
            #     self.health -= damage
            #     self.is_hit = True
            #     self.last_hit = pygame.time.get_ticks()
            #     self.hit_damage = damage
            #     # random flinch
            #     self.move(pygame.Vector2(random.randint(-10, 10), random.randint(-10, 10)))
            #     if self.health <= 0:
            #         self.death_animation()
            #     self.last_damaged = pygame.time.get_ticks()

        # for i in range(6):
        #     angle = i * 30
        #     pos_x = self.pos_x + (5 * math.sin(math.radians(angle)))
        #     pos_y = self.pos_y + (5 * math.cos(math.radians(angle)))
        #     Enemy(self.game, pos_x, pos_y, "demon", "chort")

        #https://answers.unity.com/questions/714835/best-way-to-spawn-prefabs-in-a-circle.html


    def death_animation(self):
        self.state = "death"
        if self.frame == len(self.sprite["death"]) - 1:
            self.death_animation_done = True
        if self.death_animation_done:
            self.entity_status = "dead"
            # add to player score and special ability charge
            # add to player score and special ability charge
            self.game.curr_actors[0].score += self.score_when_killed
            self.game.curr_actors[0].xp += math.ceil(
            self.score_when_killed * (self.entity_level / self.game.curr_actors[0].entity_level))
            self.game.curr_actors[0].special_charge += 10 + (self.game.curr_actors[0].charisma - 10) // 2
            # cap special charge at 100
            self.game.curr_actors[0].special_charge = min(self.game.curr_actors[0].special_charge, 100)