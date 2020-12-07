from entities import *
import boss_lookup
import config
import math
import projectile
from enemy import *

class WizardBoss(Entity):


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
        self.score_when_killed = 350
        self.target_list = [(1017,261),(990,261)]
        self.curr_target = self.target_list[0]
        self.index = 0
        self.special_damage = 0
        self.attack_cooldown = 150
        self.direction = 0
        self.curr_sprite_index = 0
        self.flip_sprite = False
        self.state = "idle2"
        self.death_counter = 0
        self.curr_attack = 1
        self.death_animation_done = False
        self.has_shield = False
        self.biting = False
        self.name = "Deathbringer"
        self.game.in_boss_battle = True
        if self.shield > 0:
            self.has_shield = True
        self.spawn_minions_every = 0



    def ai(self):
        if self.state != "death":
            if pygame.time.get_ticks() - self.last_attack >= 900:
                self.state = "idle2"
            player = self.game.curr_actors[0]
            self.current_attack(player)
            self.linear_path(player)
        else:
            self.death_animation()


    def change_attack(self):
        if (self.curr_attack + 1) % 4 == 0:
            self.curr_attack = 1
        else:
            self.curr_attack += 1


    def current_attack(self, player):
        if pygame.time.get_ticks() - self.last_attack >= self.cooldown and not player.invisible:
            if self.curr_attack == 1:
                self.state = "attack2"
                self.single_arrow()
                self.last_attack = pygame.time.get_ticks()

            elif self.curr_attack == 2:
                self.state = "attack"
                self.arrow_spray()
                self.last_attack = pygame.time.get_ticks()


            elif self.curr_attack == 3:
                if self.spawn_minions_every == 0:
                    self.state = "idle"
                    self.spawn_minions()
                    self.last_attack = pygame.time.get_ticks()
                self.spawn_minions_every += 1
                if self.spawn_minions_every == 4:
                    self.spawn_minions_every = 0


            self.change_attack()







    def move(self, direction):
        if self.can_move(direction):
            self.pos_x += direction[0]
            self.pos_y += direction[1]
            if direction[0] < 0:
                self.flip_sprite = False
            elif direction[0] > 0:
                self.flip_sprite = True



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


    def arrow_spray(self):
        for angle in range(0, 360, 48):
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
        # # top
        # Enemy(self.game, self.pos_x, self.pos_y - angle_straight, "demon", "chort")
        # # bottom
        # Enemy(self.game, self.pos_x, self.pos_y + angle_straight, "demon", "chort")
        # # #middle top left
        # Enemy(self.game, self.pos_x - angle_inbetween, self.pos_y- angle_inbetween, "demon", "chort")
        # Enemy(self.game, self.pos_x - angle_inbetween, self.pos_y + angle_inbetween, "demon", "chort")
        # Enemy(self.game, self.pos_x - angle_straight, self.pos_y, "demon", "chort")
        # Enemy(self.game, self.pos_x - angle_inbetween, self.pos_y + angle_inbetween, "demon", "chort")

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

        #https://answers.unity.com/questions/714835/best-way-to-spawn-prefabs-in-a-circle.html


    def death_animation(self):
        self.state = "death"
        if self.frame == len(self.sprite["death"]) - 1:
            self.death_animation_done = True
        if self.death_animation_done:
            self.game.in_boss_battle = False
            self.entity_status = "dead"
            # add to player score and special ability charge
            self.game.curr_actors[0].score += self.score_when_killed
            self.game.curr_actors[0].xp += self.score_when_killed
            self.game.curr_actors[0].special_charge += 10 + (self.game.curr_actors[0].charisma - 10) // 2
            # cap special charge at 100
            self.game.curr_actors[0].special_charge = min(self.game.curr_actors[0].special_charge, 100)


    def mob_drop(self):
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
            self.game.mob_drops.append(MobDropPouch(self.game, self.pos_x, self.pos_y, pouch, "Boss"))
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
        self.score_when_killed = 500
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
        self.game.in_boss_battle = True
        self.name = "Mage of the cursed corpses"
        if self.shield > 0:
            self.has_shield = True




    def ai(self):

        if self.state != "death":
            if self.health < (self.max_health//2):
                self.state = "attack_2"
            if self.ai_type == "patrol":
                player = self.game.curr_actors[0]
                if pygame.time.get_ticks() - self.last_attack >= self.cooldown and not player.invisible:
                    self.current_attack()
                    self.attack(player)
                self.linear_path(player)
        else:
            self.death_animation()

            # if self.attack_cooldown == 0:
            #     #self.spawn_minions()
            #     self.arrow_spray()
            #     self.attack_cooldown =


    def current_attack(self):
        if self.curr_attack == "single_arrow" and self.state == "attack":
            if self.frame == len(self.sprite[self.state]) - 1:
                self.single_arrow()
                self.frame = 0
                self.last_attack = pygame.time.get_ticks()
                self.curr_attack = "single_arrow"

        elif self.state == "attack_2":
            self.arrow_spray()
            self.last_attack = pygame.time.get_ticks()
            self.curr_attack = "multiple_arrow"



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

    def attack(self, target):
        # cant attack until cool-down has passed
        if pygame.time.get_ticks() - self.last_attack >= self.cooldown:

            target_vector = pygame.Vector2(target.pos_x - self.pos_x, target.pos_y - self.pos_y)
            if 0 < target_vector.length() <= self.attack_radius:
                audio.monster_bite()
                self.biting = True
                target.take_damage(self.damage)
                self.last_attack = pygame.time.get_ticks()



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


    def arrow_spray(self):
        for angle in range(0, 360, 60):
            direction = pygame.Vector2()
            direction.from_polar((1, angle))
            if self.flip_sprite:
                missile = projectile.Projectile(self.game, self.pos_x - 5 , self.pos_y - 60,
                                     config.get_super_mage_bomb_sprite(),
                                     self.special_damage, direction, "ricochet_arrow", True, 8)
            else:
                missile = projectile.Projectile(self.game, self.pos_x + 5, self.pos_y - 60,
                                     config.get_super_mage_bomb_sprite(),
                                     self.special_damage, direction, "ricochet_arrow", True, 8)
            self.game.curr_actors.append(missile)

    def single_arrow(self):
        direction = pygame.Vector2((self.game.curr_actors[0].pos_x - self.pos_x), (self.game.curr_actors[0].pos_y - self.pos_y + 30 ))
        if self.flip_sprite:
            missile = projectile.Projectile(self.game, self.pos_x - 60, self.pos_y - 50,
                                 config.get_super_mage_flame_ball(),
                                 self.special_damage, direction, "bounce_wall", True, 8)
        else:
            missile = projectile.Projectile(self.game, self.pos_x + 60, self.pos_y - 50,
                                            config.get_super_mage_flame_ball(),
                                            self.special_damage, direction, "bounce_wall", True, 8)

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

        #https://answers.unity.com/questions/714835/best-way-to-spawn-prefabs-in-a-circle.html


    def death_animation(self):
        self.state = "death"
        if self.frame == len(self.sprite["death"]) - 1:
            self.death_animation_done = True
        if self.death_animation_done:
            self.game.in_boss_battle = False
            self.entity_status = "dead"
            # add to player score and special ability charge
            # add to player score and special ability charge
            self.game.curr_actors[0].score += self.score_when_killed
            self.game.curr_actors[0].xp += math.ceil(
            self.score_when_killed * (self.entity_level / self.game.curr_actors[0].entity_level))
            self.game.curr_actors[0].special_charge += 10 + (self.game.curr_actors[0].charisma - 10) // 2
            # cap special charge at 100
            self.game.curr_actors[0].special_charge = min(self.game.curr_actors[0].special_charge, 100)

    def mob_drop(self):
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
            self.game.mob_drops.append(MobDropPouch(self.game, self.pos_x, self.pos_y, pouch, "Boss"))
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

class GreenHeadBoss(Entity):

    def __init__(self, game, pos_x, pos_y, boss_type, boss_name):
        self.lookup = boss_lookup.bosses[boss_type][boss_name]
        super(GreenHeadBoss, self).__init__(game, pos_x, pos_y, config.get_greenhead_boss_sprite(boss_name),
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
        self.hitbox = self.sprite["attack"][0].get_rect()
        self.width = self.hitbox[2]
        self.height = self.hitbox[3]
        # For testing at the moment
        self.sees_target = False
        self.growling = True
        self.has_drop_loot = True
        self.score_when_killed = 650
        self.target_list = [(1017, 261), (990, 261)]
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
        self.game.in_boss_battle = True
        self.name = "Green Tentacle Head"
        if self.shield > 0:
            self.has_shield = True
        self.attack_number = 0


    def ai(self):
        if self.state != "death":
            if self.ai_type == "patrol":
                player = self.game.curr_actors[0]
                if pygame.time.get_ticks() - self.last_attack >= self.cooldown and not player.invisible:
                    self.current_attack()
                self.linear_path(player)
        else:
            self.death_animation()

    def current_attack(self):
        if self.health < self.max_health / 2:
            self.spawn_minions()
            self.last_attack = pygame.time.get_ticks()
        # if self.frame == len(self.sprite[self.state]) - 1:
        self.single_arrow()
        self.frame = 0
        self.last_attack = pygame.time.get_ticks()

        # elif self.curr_attack == "multiple_arrow":
        #     self.arrow_spray()
        #     self.last_attack = pygame.time.get_ticks()
        #     self.curr_attack = "spawn_minions"



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

    def attack(self, target):
        # cant attack until cool-down has passed
        if pygame.time.get_ticks() - self.last_attack >= self.cooldown:

            target_vector = pygame.Vector2(target.pos_x - self.pos_x, target.pos_y - self.pos_y)
            if 0 < target_vector.length() <= self.attack_radius:
                audio.monster_bite()
                self.biting = True
                target.take_damage(self.damage)
                self.last_attack = pygame.time.get_ticks()

    def patrol(self):
        target_vector = pygame.Vector2(self.curr_target[0] - self.pos_x, self.curr_target[1] - self.pos_y)
        if target_vector.length() > 3:
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

    def arrow_spray(self):
        for angle in range(0, 360, 60):
            direction = pygame.Vector2()
            direction.from_polar((1, angle))
            if self.flip_sprite:
                missile = projectile.Projectile(self.game, self.pos_x - 5, self.pos_y - 60,
                                                config.get_super_mage_bomb_sprite(),
                                                self.special_damage, direction, "ricochet_arrow", True, 8)
            else:
                missile = projectile.Projectile(self.game, self.pos_x + 5, self.pos_y - 60,
                                                config.get_super_mage_bomb_sprite(),
                                                self.special_damage, direction, "ricochet_arrow", True, 8)
            self.game.curr_actors.append(missile)

    def single_arrow(self):
        direction = pygame.Vector2((self.game.curr_actors[0].pos_x - self.pos_x),
                                   (self.game.curr_actors[0].pos_y - self.pos_y + 30))
        if self.flip_sprite:
            missile = projectile.Projectile(self.game, self.pos_x - 20, self.pos_y - 45,
                                            config.get_green_head_projectile(),
                                            self.special_damage, direction, "ricochet_arrow", True, 8)
        else:
            missile = projectile.Projectile(self.game, self.pos_x + 20 , self.pos_y - 45,
                                            config.get_green_head_projectile(),
                                            self.special_damage, direction, "ricochet_arrow", True, 8)

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

        # https://answers.unity.com/questions/714835/best-way-to-spawn-prefabs-in-a-circle.html

    def death_animation(self):
        self.state = "death"
        if self.frame == len(self.sprite["death"]) - 1:
            self.death_animation_done = True
        if self.death_animation_done:
            self.game.in_boss_battle = False
            self.entity_status = "dead"
            # add to player score and special ability charge
            # add to player score and special ability charge
            self.game.curr_actors[0].score += self.score_when_killed
            self.game.curr_actors[0].xp += math.ceil(
                self.score_when_killed * (self.entity_level / self.game.curr_actors[0].entity_level))
            self.game.curr_actors[0].special_charge += 10 + (self.game.curr_actors[0].charisma - 10) // 2
            # cap special charge at 100
            self.game.curr_actors[0].special_charge = min(self.game.curr_actors[0].special_charge, 100)

    def spawn_minions(self):
        if self.attack_number == 0:
            angle_straight = 40
            angle_inbetween = angle_straight * 0.75

            # # right straight
            Enemy(self.game, self.pos_x + angle_straight, self.pos_y, "demon", "minionhead")
            # # top right
            Enemy(self.game, self.pos_x + angle_inbetween, self.pos_y - angle_inbetween, "demon", "minionhead")
            self.attack_number += 1
        elif self.attack_number + 1 == 3:
            self.attack_number = 0
        else:
            self.attack_number += 1
        # top
        # Enemy(self.game, self.pos_x, self.pos_y - angle_straight, "demon", "minionhead")
        # # bottom
        # Enemy(self.game, self.pos_x, self.pos_y + angle_straight, "demon", "minionhead")
        # # #middle top left
        # Enemy(self.game, self.pos_x - angle_inbetween, self.pos_y - angle_inbetween, "demon", "minionhead")
        # Enemy(self.game, self.pos_x - angle_inbetween, self.pos_y + angle_inbetween, "demon", "minionhead")
        # Enemy(self.game, self.pos_x - angle_straight, self.pos_y, "demon", "minionhead")
        # Enemy(self.game, self.pos_x - angle_inbetween, self.pos_y + angle_inbetween, "demon", "minionhead")


    def mob_drop(self):
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
            self.game.mob_drops.append(MobDropPouch(self.game, self.pos_x, self.pos_y, pouch, "Boss"))
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