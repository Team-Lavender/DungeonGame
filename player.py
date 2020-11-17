
import equipment_list
import character_classes
from weapon import *
from consumable import *

class Player(Entity):
    def __init__(self, game, pos_x, pos_y, sprite, character_class):
        # initial character stats from character class
        self.score = 0
        self.character_class = character_class
        self.strength = character_classes.character_stats[character_class]["str"]
        self.dexterity = character_classes.character_stats[character_class]["dex"]
        self.constitution = character_classes.character_stats[character_class]["con"]
        self.intellect = character_classes.character_stats[character_class]["int"]
        self.wisdom = character_classes.character_stats[character_class]["wis"]
        self.charisma = character_classes.character_stats[character_class]["cha"]

        self.armor = equipment_list.armor_list[character_classes.starting_equipment[self.character_class]["armor"]]

        super(Player, self).__init__(game, pos_x, pos_y, sprite, 5 + ((self.constitution - 10) // 2),
                                     self.armor["AC"], False, 1, "alive",
                                     ((5 + ((self.dexterity - 10) // 2)) / 5))
        # penalty to movement if armor is too heavy
        if self.armor["weight"] > (self.strength - 10 // 2):
            self.move_speed /= 4

        self.money = 0
        self.last_damaged = pygame.time.get_ticks()
        self.special_charge = 0

        starting_weapon = character_classes.starting_equipment[self.character_class]["weapon"]

        bonuses = {"str": (self.strength - 10) // 2,
                   "dex": (self.dexterity - 10) // 2,
                   "con": (self.constitution - 10) // 2,
                   "int": (self.intellect - 10) // 2,
                   "wis": (self.wisdom - 10) // 2,
                   "cha": (self.charisma - 10) // 2}

        self.items = \
            [Weapon(game, self.pos_x, self.pos_y,
                    config.get_weapon_sprite(starting_weapon), 1,
                    equipment_list.weapons_list[starting_weapon]["cost"],
                    equipment_list.weapons_list[starting_weapon]["type"],
                    equipment_list.weapons_list[starting_weapon]["range"] * 32,
                    equipment_list.weapons_list[starting_weapon]["dmg"]
                    + bonuses[equipment_list.weapons_list[starting_weapon]["main_stat"]],
                    1 / max((equipment_list.weapons_list[starting_weapon]["speed"] + (bonuses["dex"] / 2)), 0.1),
                    equipment_list.weapons_list[starting_weapon]["crit_chance"]
                    + (bonuses["wis"] * 4)), None, None]
        self.held_item_index = 0
        self.held_item = self.items[self.held_item_index]

        self.potion_1 = [Consumable(game, "heal_small"), ]
        self.potion_2 = [Consumable(game, "shield_large"), Consumable(game, "shield_large")]

        self.look_direction = pygame.Vector2(1, 0)
        self.has_shield = False
        if self.shield > 0:
            self.has_shield = True




    def use_item(self):
        if isinstance(self.held_item, Weapon) and \
                pygame.time.get_ticks() - self.held_item.last_used >= 1000 * self.held_item.attack_speed:
            self.held_item.state = "blast"
            crit_roll = random.randint(0, 101)
            crit = False
            if crit_roll <= self.held_item.crit_chance:
                crit = True
                self.held_item.attack_damage *= 2
            if self.held_item.combat_style == "melee":
                self.attack()
            elif self.held_item.combat_style == "ranged":
                self.held_item.ranged_attack()
            elif self.held_item.combat_style == "magic":
                self.held_item.magic_attack()

            if crit:
                self.held_item.attack_damage /= 2
            self.held_item.last_used = pygame.time.get_ticks()
        else:
            pass

    def attack(self):
        for actor in self.game.curr_actors:
            if isinstance(actor, Enemy):
                target_vector = pygame.Vector2(actor.pos_x - self.pos_x, actor.pos_y - (actor.height // 4) - self.pos_y)
                if 0 < target_vector.length() <= self.held_item.attack_range:
                    attack_vector = self.look_direction
                    angle = target_vector.angle_to(attack_vector)
                    angle = angle % 360
                    angle = (angle + 360) % 360

                    if angle > 180:
                        angle -= 360
                    if abs(angle) <= 20:
                        actor.take_damage(self.held_item.attack_damage)

    def swap_item(self, next_or_prev):
        self.held_item_index = (self.held_item_index + next_or_prev) % 3
        self.held_item = self.items[self.held_item_index]


    def get_input(self):
        dx = 0
        dy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        direction = pygame.Vector2(dx, dy)
        if direction.length() > 0:
            if self.held_item == None:
                speed_modifier = 1.3
            else:
                speed_modifier = 1
            direction.scale_to_length(speed_modifier * 2 * self.move_speed)
        self.move(direction)

        mouse_vector = pygame.mouse.get_pos()
        look_vector = pygame.Vector2((mouse_vector[0] - self.pos_x), (mouse_vector[1] + 8 - self.pos_y))
        self.look_direction = look_vector.normalize()
        if isinstance(self.held_item, Weapon):
            self.held_item.pos_x = self.pos_x
            self.held_item.pos_y = self.pos_y
            self.held_item.target_direction = self.look_direction
            self.held_item.angle = self.look_direction.angle_to(pygame.Vector2(0, -1))

        if self.game.ACTION:
            self.use_item()

        if self.game.SPECIAL:
            self.special_ability()

        if self.game.SCROLL_UP:
            self.swap_item(1)

        if self.game.SCROLL_DOWN:
            self.swap_item(-1)

        if self.game.INTERACT:
            self.open_door()

        if self.game.CONSUMABLE_1 and self.potion_1 is not None:
            self.use_consumable(1)

        if self.game.CONSUMABLE_2 and self.potion_2 is not None:
            self.use_consumable(2)

    def take_damage(self, damage):
        if pygame.time.get_ticks() - self.last_damaged >= 60:
            if self.shield > 0:
                self.shield -= damage
            if self.shield <= 0 and self.has_shield:
                temp = damage + self.shield
                damage -= temp
                self.shield = 0
                self.has_shield = False
            if not self.has_shield:
                self.health -= damage
            self.state = "hit"
            # random flinch
            self.move(pygame.Vector2(random.randint(-10, 10), random.randint(-10, 10)))
            if self.health <= 0:
                self.game.playing = False
                self.game.curr_menu = self.game.main_menu

            self.last_damaged = pygame.time.get_ticks()

    def special_ability(self):
        if self.special_charge >= 100:
            self.special_charge = 0

    def open_door(self):
        for door in self.game.curr_map.door:
            distance = pygame.Vector2(self.pos_x - door[0] * 16, self.pos_y - door[1] * 16).length()
            if distance <= 50:
                # go to the map indicated by door[2]
                self.game.change_map(door[2])

    def use_consumable(self, slot_number):
        if slot_number == 1 and len(self.potion_1) > 0:

            self.potion_1[-1].use()
        elif slot_number == 2 and len(self.potion_2) > 0:
            self.potion_2[-1].use()