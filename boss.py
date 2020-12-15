from entities import *
import boss_lookup
import config
import math
import projectile
from enemy import *

# Used in level 1
class GhostBoss(Entity):

    def __init__(self, game, pos_x, pos_y, boss_type, boss_name):
        self.lookup = boss_lookup.bosses[boss_type][boss_name]
        super(GhostBoss, self).__init__(game, pos_x, pos_y, config.get_wizard_boss_sprite(boss_name),
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
        '''
        Procedure for cycling through boss attacks
        :return:
        '''
        if (self.curr_attack + 1) % 4 == 0:
            self.curr_attack = 1
        else:
            self.curr_attack += 1


    def current_attack(self, player):
        '''
        Cycle through attacks and change animation sprite for each attack
        :param player: Used for checking if the player is invlisible
        :return:
        '''
        if pygame.time.get_ticks() - self.last_attack >= self.cooldown and not player.invisible:
            if self.curr_attack == 1:
                self.state = "attack2"
                self.single_projectile()
                self.last_attack = pygame.time.get_ticks()

            elif self.curr_attack == 2:
                self.state = "attack"
                self.spray_attack()
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
        '''
        Move boss towards direction. Flip sprite when changing direction
        :param direction:
        :return:
        '''
        if self.can_move(direction):
            self.pos_x += direction[0]
            self.pos_y += direction[1]
            if direction[0] < 0:
                self.flip_sprite = False
            elif direction[0] > 0:
                self.flip_sprite = True

    # Currently unused function
    def patrol(self):
        '''
        Function that moves the boss through a predefined path
        :return:
        '''
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
        '''
        Function that moves the boss towards the player using linear path
        :param target:
        :return:
        '''
        target_vector = pygame.Vector2(target.pos_x - self.pos_x, target.pos_y - self.pos_y)
        if 0 < target_vector.length() <= self.vision_radius and not target.invisible:
            self.sees_target = True
            target_vector.scale_to_length(self.move_speed)
            self.move(target_vector)


    def spray_attack(self):
        '''
        A boss attack with performs a spray of projectile attacks
        :return:
        '''
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

    def single_projectile(self):
        '''
        Function that throws a single projectile towards the player
        :return:
        '''
        direction = pygame.Vector2((self.game.curr_actors[0].pos_x - self.pos_x), (self.game.curr_actors[0].pos_y - self.pos_y + 30 ))
        missile = projectile.Projectile(self.game, self.pos_x, self.pos_y - 40,
                             config.get_wizard_projectile_sprite(),
                             self.special_damage, direction, None, True, 8)
        self.game.curr_actors.append(missile)


    def spawn_minions(self):
        '''
        Boss ability which spawns minions
        :return:
        '''
        angle_straight = 40
        angle_inbetween = angle_straight * 0.75

        # # right straight
        Enemy(self.game, self.pos_x + angle_straight, self.pos_y, "demon", "chort_boss")
        # # top right
        Enemy(self.game, self.pos_x + angle_inbetween, self.pos_y - angle_inbetween, "demon", "chort_boss")
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
        '''
        Function that performs damage to the boss.
        If health is below 0, perform death_animation()
        :param damage:
        :return:
        '''
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
        '''
        Function that changes the sprite state to "death" and sets the entity_status to "dead"
        when the death animation has finished.
        :return:
        '''
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
        '''
        Function that randomly drops items from the boss drops
        :param self:
        :return:
        '''
        pouch = []
        rnd = random.randint(0, 100)
        quantity_chance = random.randrange(1, 5)
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
        '''
        Helper function for looking up item names
        :param self:
        :param item_name:
        :param quantity:
        :return:  Return a list of [item_name, quantity, item_type]
        '''
        if item_name in equipment_list.weapons_list:
            return [item_name, quantity, "weapon"]
        elif item_name in equipment_list.potions_list:
            return [item_name, quantity, "potion"]
        elif item_name in equipment_list.throwables_list:
            return [item_name, quantity, "throwable"]
        elif item_name == "coins":
            return [item_name, quantity]


# Used in level 3
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
        '''
        Function that controls the ai of the boss
        :return:
        '''
        if self.state != "death":
            # If health less or equal than half, change sprite
            if self.health <= (self.max_health//2):
                self.state = "attack_2"
            if self.ai_type == "patrol":
                player = self.game.curr_actors[0]
                if pygame.time.get_ticks() - self.last_attack >= self.cooldown and not player.invisible:
                    self.current_attack()
                    self.attack(player)
                self.linear_path(player)
        else:
            self.death_animation()

    def current_attack(self):
        '''
        Function that cycles through attacks
        :return:
        '''
        if self.curr_attack == "single_arrow" and self.state == "attack":
            if self.frame == len(self.sprite[self.state]) - 1:
                self.single_projecticle()
                self.frame = 0
                self.last_attack = pygame.time.get_ticks()
                self.curr_attack = "single_arrow"

        elif self.state == "attack_2":
            self.spray_attack()
            self.last_attack = pygame.time.get_ticks()
            self.curr_attack = "multiple_arrow"



    def move(self, direction):
        '''
        Function that moves the boss towards a direction
        Flips the sprite to face the direction
        :param direction:
        :return:
        '''
        if self.can_move(direction):
            self.pos_x += direction[0]
            self.pos_y += direction[1]
            if direction[0] < 0:
                self.flip_sprite = True
            elif direction[0] > 0:
                self.flip_sprite = False



    def attack(self, target):
        '''
        Function which attacks the target if in close range
        :param target:
        :return:
        '''
        # cant attack until cool-down has passed
        if pygame.time.get_ticks() - self.last_attack >= self.cooldown:

            target_vector = pygame.Vector2(target.pos_x - self.pos_x, target.pos_y - self.pos_y)
            if 0 < target_vector.length() <= self.attack_radius:
                audio.monster_bite()
                self.biting = True
                target.take_damage(self.damage)
                self.last_attack = pygame.time.get_ticks()

    # Currently unused
    def patrol(self):
        '''
        Function that allows the boss to move in a predefined path
        :return:
        '''
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
        '''
        Function that follows a linear path towards a target
        :param target:
        :return:
        '''
        target_vector = pygame.Vector2(target.pos_x - self.pos_x, target.pos_y - self.pos_y)
        if 0 < target_vector.length() <= self.vision_radius and not target.invisible:
            self.sees_target = True
            target_vector.scale_to_length(self.move_speed)
            self.move(target_vector)


    def spray_attack(self):
        '''
        Function that performs the spray attack ability
        :return:
        '''
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

    def single_projecticle(self):
        '''
        Function that shoots a projectile towards the player
        :return:
        '''
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
        '''
        Function that performs damage to the boss
        If health is below 0, perform death_animation()
        :param damage:
        :return:
        '''
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
        '''
        Function that changes the sprite to "death" animation
        When the animation is finished, set the entity_status to "dead"
        :return:
        '''
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
        '''
        Function that drops random items from the boss drops dictionary
        and appends them to a new pouch object
        :return:
        '''
        pouch = []
        rnd = random.randint(0, 100)
        quantity_chance = random.randrange(1, 5)
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
        '''
        Helper function to lookup items
        :param item_name:
        :param quantity:
        :return: Return a list in the form of [item_name, quantity, item_type]
        '''
        if item_name in equipment_list.weapons_list:
            return [item_name, quantity, "weapon"]
        elif item_name in equipment_list.potions_list:
            return [item_name, quantity, "potion"]
        elif item_name in equipment_list.throwables_list:
            return [item_name, quantity, "throwable"]
        elif item_name == "coins":
            return [item_name, quantity]


# Used in level 2
class TentacleBoss(Entity):

    def __init__(self, game, pos_x, pos_y, boss_type, boss_name):
        self.lookup = boss_lookup.bosses[boss_type][boss_name]
        super(TentacleBoss, self).__init__(game, pos_x, pos_y, config.get_greenhead_boss_sprite(boss_name),
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
        self.name = "Sephiroth, lord of tentacles"
        if self.shield > 0:
            self.has_shield = True
        self.attack_number = 0


    def ai(self):
        '''
        Function that controls the ai of the boss
        :return:
        '''
        if self.state != "death":
            if self.ai_type == "patrol":
                player = self.game.curr_actors[0]
                if pygame.time.get_ticks() - self.last_attack >= self.cooldown and not player.invisible:
                    self.current_attack()
                self.linear_path(player)
        else:
            self.death_animation()

    def current_attack(self):
        '''
        Function that handles the current attack
        :return:
        '''
        if self.health < self.max_health / 2:
            self.spawn_minions()
            self.last_attack = pygame.time.get_ticks()
        self.single_projectile()
        self.frame = 0
        self.last_attack = pygame.time.get_ticks()



    def move(self, direction):
        '''
        Function that moves the boss to a direction
        Flip sprite to face the direction
        :param direction:
        :return:
        '''
        if self.can_move(direction):
            self.pos_x += direction[0]
            self.pos_y += direction[1]
            if direction[0] < 0:
                self.flip_sprite = True
            elif direction[0] > 0:
                self.flip_sprite = False


    def attack(self, target):
        '''
        Attack the target if in range
        :param target:
        :return:
        '''
        # cant attack until cool-down has passed
        if pygame.time.get_ticks() - self.last_attack >= self.cooldown:

            target_vector = pygame.Vector2(target.pos_x - self.pos_x, target.pos_y - self.pos_y)
            if 0 < target_vector.length() <= self.attack_radius:
                audio.monster_bite()
                self.biting = True
                target.take_damage(self.damage)
                self.last_attack = pygame.time.get_ticks()

    # Currently unused
    def patrol(self):
        '''
        Function that moves the boss through a predefined path
        :return:
        '''
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
        '''
        Moves the boss through a liner path towards the target
        :param target:
        :return:
        '''
        target_vector = pygame.Vector2(target.pos_x - self.pos_x, target.pos_y - self.pos_y)
        if 0 < target_vector.length() <= self.vision_radius and not target.invisible:
            self.sees_target = True
            target_vector.scale_to_length(self.move_speed)
            self.move(target_vector)

    # Currently unused
    def spray_attack(self):
        '''
        Function that sprays projectiles in a 360 range
        :return:
        '''
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

    def single_projectile(self):
        '''
        Function that shoots a single projectile towards the player
        :return:
        '''
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
        '''
        Function that performs damage to the boss
        If health is below 0, call the death_animation() function
        :param damage:
        :return:
        '''
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
        '''
        Sets the sprite to "death"
        If the animation has finished, change the entity_status to "dead"
        :return:
        '''
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
        '''
        Function that spawns minions for the boss
        :return:
        '''
        if self.attack_number == 0:
            angle_straight = 40
            angle_inbetween = angle_straight * 0.75

            # # right straight
            Enemy(self.game, self.pos_x + angle_straight, self.pos_y, "demon", "minionhead_boss")
            # # top right
            Enemy(self.game, self.pos_x + angle_inbetween, self.pos_y - angle_inbetween, "demon", "minionhead_boss")
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
        '''
        Functions that drops random loot from the boss loot dictionary
        :return:
        '''
        pouch = []
        rnd = random.randint(0, 100)
        quantity_chance = random.randrange(1, 5)
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
        '''
        Helper function to lookup items
        :param item_name:
        :param quantity:
        :return:  Returns a list in the form of [item_name, quantity, item_type]
        '''
        if item_name in equipment_list.weapons_list:
            return [item_name, quantity, "weapon"]
        elif item_name in equipment_list.potions_list:
            return [item_name, quantity, "potion"]
        elif item_name in equipment_list.throwables_list:
            return [item_name, quantity, "throwable"]
        elif item_name == "coins":
            return [item_name, quantity]