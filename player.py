import equipment_list
import character_classes
from weapon import *
from consumable import *
import audio
from projectile import *
from throwable import *
from enemy import *
import levelling

class Player(Entity):
    def __init__(self, game, pos_x, pos_y, sprite, character_class):

        # in combat indicator for music control
        self.in_combat = False

        # initial character stats from character class
        self.score = 0
        self.xp = 0

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

        self.max_xp = 50 * self.entity_level * 1.5
        self.money = 0
        self.last_damaged = pygame.time.get_ticks()
        self.special_charge = 0
        self.special_damage = 10
        self.rendering_special = False
        self.special_sprite = None
        self.special_cast_sprite = config.special_cast
        self.special_sprite_offset = 0
        self.special_frame = 0
        self.footstep_counter = 0
        self.invisible = False
        self.display_crit = False
        self.show_level_up = False
        self.last_level = pygame.time.get_ticks()

        starting_weapon = character_classes.starting_equipment[self.character_class]["weapon"]

        bonuses = {"str": (self.strength - 10) // 2,
                   "dex": (self.dexterity - 10) // 2,
                   "con": (self.constitution - 10) // 2,
                   "int": (self.intellect - 10) // 2,
                   "wis": (self.wisdom - 10) // 2,
                   "cha": (self.charisma - 10) // 2}

        self.items = \
            [Weapon(game, starting_weapon, self.pos_x, self.pos_y,
                    config.get_weapon_sprite(starting_weapon), 1,
                    equipment_list.weapons_list[starting_weapon]["cost"],
                    equipment_list.weapons_list[starting_weapon]["type"],
                    equipment_list.weapons_list[starting_weapon]["range"] * 16,
                    equipment_list.weapons_list[starting_weapon]["dmg"]
                    + bonuses[equipment_list.weapons_list[starting_weapon]["main_stat"]],
                    1 / max((equipment_list.weapons_list[starting_weapon]["speed"] + (bonuses["dex"] / 2)), 0.1),
                    equipment_list.weapons_list[starting_weapon]["crit_chance"]
                    + (bonuses["wis"] * 2)),
             None,
             None]
        self.inventory = [None] * 25
        # = [(knife,1,weapon), (heal_pot, 3, potion)]
        self.held_item_index = 0
        self.held_item = self.items[self.held_item_index]

        self.potion_1 = []
        self.potion_2 = []
        self.add_potions_to_slot(1, character_classes.starting_equipment[self.character_class]["potion_1"])
        self.add_potions_to_slot(2, character_classes.starting_equipment[self.character_class]["potion_2"])

        self.look_direction = pygame.Vector2(1, 0)
        self.has_shield = False
        if self.shield > 0:
            self.has_shield = True

        self.open_door_timer = pygame.time.get_ticks()

    def use_item(self):
        if isinstance(self.held_item, Weapon) and \
                pygame.time.get_ticks() - self.held_item.last_used >= 1000 * self.held_item.attack_speed:
            self.held_item.state = "blast"
            self.invisible = False

            crit_roll = random.randint(0, 100)
            crit = False
            if crit_roll <= self.held_item.crit_chance:
                crit = True
                self.display_crit = True
                audio.critical_attack()

                self.held_item.attack_damage *= 2
            if self.held_item.combat_style == "melee":
                self.attack()
                self.held_item.slash = True
                audio.sword_swing()
            elif self.held_item.combat_style == "ranged":
                self.held_item.ranged_attack()
                audio.arrow_launch()
            elif self.held_item.combat_style == "magic":
                self.held_item.magic_attack()
                audio.magic_spell_cast()

            # reset attack damage after previous crit
            if crit:
                self.held_item.attack_damage /= 2

            self.held_item.last_used = pygame.time.get_ticks()
        else:
            pass

    def attack(self):
        for actor in self.game.curr_actors:
            if isinstance(actor, Enemy):
                target_vector = pygame.Vector2(actor.pos_x - self.held_item.weapon_pos[0],
                                               actor.pos_y - (actor.height // 4) - self.held_item.weapon_pos[1])
                if 0 < target_vector.length() <= (self.held_item.weapon_length + actor.width / 2) / 2:
                    actor.take_damage(self.held_item.attack_damage)

                    # play hit sound
                    audio.sword_hit()

    def swap_item(self, next_or_prev):
        holding_item = self.held_item is not None
        self.held_item_index = (self.held_item_index + next_or_prev) % 3
        self.held_item = self.items[self.held_item_index]
        if self.held_item is None:
            if holding_item:
                audio.sheathe_weapon()
        else:
            audio.draw_weapon()

    def get_input(self):

        dx = 0
        dy = 0
        keys = pygame.key.get_pressed()
        # If a cutscene is triggered, do not allow a played to move
        if not self.game.cutscene_trigger:
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
            if self.held_item is None:
                speed_modifier = 1.3
            else:
                speed_modifier = 1
            direction.scale_to_length(speed_modifier * 2 * self.move_speed)
        self.move(direction)
        if direction.length() != 0:
            self.footstep(round(10 / direction.length()))

        mouse_vector = pygame.mouse.get_pos()
        look_vector = pygame.Vector2((mouse_vector[0] - self.pos_x), (mouse_vector[1] + 8 - self.pos_y))
        self.look_direction = look_vector.normalize()
        if isinstance(self.held_item, Weapon):
            self.held_item.pos_x = self.pos_x
            self.held_item.pos_y = self.pos_y
            self.held_item.target_direction = self.look_direction
            self.held_item.angle = self.look_direction.angle_to(pygame.Vector2(0, -1))

        # If a cutscene is triggered, do not allow the player to perform actions
        if not self.game.cutscene_trigger:
            if self.game.ACTION:
                self.use_item()

        if self.game.SPECIAL:
            self.special_ability()
        if self.rendering_special:
            self.render_special()

        if self.game.SCROLL_UP:
            self.swap_item(1)

        if self.game.SCROLL_DOWN:
            self.swap_item(-1)

        if self.game.INTERACT and pygame.time.get_ticks() - self.open_door_timer >= 1000:
            self.open_door()
            self.open_door_timer = pygame.time.get_ticks()

        if self.game.LOOT:
            self.open_mob_pouch()

        if self.game.CONSUMABLE_1 and self.potion_1 is not None:
            self.use_consumable(1)


        if self.game.CONSUMABLE_2 and self.potion_2 is not None:
            self.use_consumable(2)

        if self.game.MODIFY:
            if len(self.potion_1) != 0:
                if isinstance(self.potion_1[-1], Throwable):
                    if self.potion_1[-1].targeting:
                        if not self.potion_1[-1].thrown:
                            self.potion_1[-1].thrown = True
                            self.potion_1[-1].targeting = not self.potion_1[-1].targeting
                            audio.throw()
            if len(self.potion_2) != 0:
                if isinstance(self.potion_2[-1], Throwable):
                    if self.potion_2[-1].targeting:
                        if not self.potion_2[-1].thrown:
                            self.potion_2[-1].thrown = True
                            self.potion_2[-1].targeting = not self.potion_2[-1].targeting
                            audio.throw()


        # display crit message
        if isinstance(self.held_item, Weapon) and \
                self.held_item.state != "idle" and \
                self.display_crit:
            self.game.draw_text("Crit!", 20, self.pos_x, self.pos_y - 25)
        if isinstance(self.held_item, Weapon) and \
                self.held_item.state == "idle":
            self.display_crit = False

        # level up if xp is max
        if self.xp >= self.max_xp:
            levelling.level_up(self, 1)
            self.show_level_up = True
            self.last_level = pygame.time.get_ticks()
        self.display_level_up()

    def display_level_up(self):

            if pygame.time.get_ticks() - self.last_level >= 400:
                self.show_level_up = False

            string = "Level: " + str(self.entity_level)

            x = self.pos_x
            y = self.pos_y - self.sprite["idle"][0].get_height() - 8
            if self.show_level_up:
                self.game.draw_text(string, 50, x, y, config.GOLD)



    def take_damage(self, damage):
        if pygame.time.get_ticks() - self.last_damaged >= 60:
            self.is_hit = True
            self.last_hit = pygame.time.get_ticks()
            self.hit_damage = damage
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
                if damage > 0:
                    audio.player_health_damage()
            self.state = "hit"
            # random flinch
            self.move(pygame.Vector2(random.randint(-10, 10), random.randint(-10, 10)))
            if self.health <= 0:
                levelling.death(self, 50, 5)
                self.game.save_state.save_game(self.game)
                self.game.playing = False
                self.game.curr_menu = self.game.main_menu

            self.last_damaged = pygame.time.get_ticks()

    def special_ability(self):
        if self.special_charge >= 100:
            self.special_charge = 0
            self.rendering_special = True
            audio.special_move()
            if self.character_class == "ROGUE":
                self.invisible = True
            if self.character_class == "RANGER":
                self.arrow_spray()
            if self.character_class == "PALADIN":
                self.special_sprite = config.get_special_sprite("spin_attack")
                self.spin_attack()
            if self.character_class == "MAGE":
                self.special_sprite = config.get_special_sprite("magic_blast")
                self.special_sprite_offset = -50
                self.magic_blast()

    def arrow_spray(self):
        for angle in range(0, 360, 12):
            direction = pygame.Vector2()
            direction.from_polar((1, angle))
            missile = Projectile(self.game, self.pos_x, self.pos_y,
                                 config.get_projectile_sprite("standard_arrow"),
                                 self.special_damage, direction)
            self.game.curr_actors.append(missile)

    def spin_attack(self):
        audio.sword_swing()
        attack_width = self.special_sprite[0].get_width()
        attack_height = self.special_sprite[0].get_height()
        for actor in self.game.curr_actors:
            if isinstance(actor, Enemy):
                if abs(actor.pos_x - self.pos_x) <= attack_width / 2 and abs(
                        actor.pos_y - self.pos_y) <= attack_height / 2:
                    actor.take_damage(self.special_damage)
                    audio.sword_hit()

    def magic_blast(self):
        attack_width = self.special_sprite[0].get_width()
        attack_height = self.special_sprite[0].get_height()
        for actor in self.game.curr_actors:
            if isinstance(actor, Enemy):
                if abs(actor.pos_x - self.pos_x) <= attack_width / 2 and (
                        actor.pos_y - self.pos_y) <= attack_height / 2:
                    actor.take_damage(self.special_damage)

    def render_special(self):
        special_cast_frames = self.special_cast_sprite
        frames = self.special_sprite
        anim_length = len(special_cast_frames)

        cast_frame = special_cast_frames[self.special_frame]
        cast_rect = cast_frame.get_rect()
        # offset cast animation to sit just below player
        cast_rect.midbottom = (self.pos_x, self.pos_y + 7)

        self.game.display.blit(cast_frame, cast_rect)

        # render extra animation if it exists
        if frames is not None:
            curr_frame = frames[self.special_frame]
            frame_rect = curr_frame.get_rect()
            frame_rect.center = (self.pos_x, self.pos_y + self.special_sprite_offset)
            self.game.display.blit(curr_frame, frame_rect)

        if self.update_frame == 0:
            self.special_frame = (self.special_frame + 1) % anim_length
        if self.special_frame == anim_length - 1:
            self.rendering_special = False
            self.special_frame = 0


    def open_door(self):
        for a_door in self.game.curr_map.door:
            distance = pygame.Vector2(self.pos_x - a_door[0] * 16, self.pos_y - a_door[1] * 16).length()
            if distance <= 50:
                # go to the map indicated by door[2]
                self.game.change_map(a_door[2])
                audio.open_door()
                break

    def open_mob_pouch(self):
        for pouch in self.game.mob_drops:
            # If a pouch location on map the map matches a pouch object at that point
            if ((pouch.pos_x - self.pos_x) ** 2 + (pouch.pos_y - self.pos_y) ** 2) <= 2000:
                self.loot_items(pouch)
                break

    def loot_items(self, pouch):
        removed = True
        if pouch.status != "removed":
            for item in pouch.items:
                # If the item in the pouch is coins, add quantity to balance
                if item[0] == "coins":
                    self.money += item[1]
                    pouch.coins = item[1]
                    pouch.items.remove(item)
                elif not self.add_to_inventory(item):
                    self.game.inventory_full_error = True
                    removed = False
        if removed:
            pouch.status = "removed"



    def use_consumable(self, slot_number):
        if slot_number == 1 and len(self.potion_1) > 0:

            self.potion_1[-1].use()
        elif slot_number == 2 and len(self.potion_2) > 0:
            self.potion_2[-1].use()

    def add_potions_to_slot(self, potion_slot, potion_type_and_quantity):
        if potion_slot == 1:
            slot = self.potion_1
        elif potion_slot == 2:
            slot = self.potion_2
        potion_tuple = potion_type_and_quantity
        for i in range(0, potion_tuple[1]):
            # if potion is not a throwable add the consumable, else add a throwable
            if potion_tuple[0] != "explosive_large" and potion_tuple[0] != "explosive_small" and potion_tuple[0] != "acid_large" and potion_tuple[0] != "acid_small":
                slot.append(Consumable(self.game, potion_tuple[0]))
            else:
                slot.append(Throwable(self.game, potion_tuple[0]))

    def get_potion(self, potion_slot):
        if potion_slot == 1:
            slot = self.potion_1
        elif potion_slot == 2:
            slot = self.potion_2
        if len(slot) > 0:
            return (slot[0].name, len(slot))
        else:
            return None

    def footstep(self, speed):
        if speed != 0:
            if self.footstep_counter == 0:
                audio.play_footstep()
            self.footstep_counter = (self.footstep_counter + 1) % (speed * 3)
        else:
            self.footstep_counter = 0

    def add_to_inventory(self, item_list):
        # takes list in the form [item_name, quantity, item_type]
        if self.add_to_hotbar(item_list):
            return True
        if item_list[-1] == "weapon":
            for idx, slot in enumerate(self.inventory):
                # add weapon to empty slot
                if slot is None:
                    self.inventory[idx] = item_list
                    return True
        elif item_list[-1] == "potion" or item_list[-1] == "throwable":
            for slot in self.inventory:
                if slot is None:
                    continue
                # if name is the same, increment quantity
                if slot[0] == item_list[0]:
                    slot[1] += item_list[1]
                    return True
            for idx, slot in enumerate(self.inventory):
                if slot is None:
                    self.inventory[idx] = item_list
                    return True
        # cannot add to inventory
        return False

    def add_to_hotbar(self, item_in):
        if item_in is not None:
            if item_in[-1] == "weapon":
                weapon_name = item_in[0]
                for idx, item in enumerate(self.items):
                    if item is None:
                        bonuses = {"str": (self.strength - 10) // 2,
                                   "dex": (self.dexterity - 10) // 2,
                                   "con": (self.constitution - 10) // 2,
                                   "int": (self.intellect - 10) // 2,
                                   "wis": (self.wisdom - 10) // 2,
                                   "cha": (self.charisma - 10) // 2}
                        self.items[idx] = Weapon(self.game, weapon_name, self.pos_x, self.pos_y,
                        config.get_weapon_sprite(weapon_name), 1,
                        equipment_list.weapons_list[weapon_name]["cost"],
                        equipment_list.weapons_list[weapon_name]["type"],
                        equipment_list.weapons_list[weapon_name]["range"] * 16,
                        equipment_list.weapons_list[weapon_name]["dmg"]
                        + bonuses[equipment_list.weapons_list[weapon_name]["main_stat"]],
                        1 / max((equipment_list.weapons_list[weapon_name]["speed"] + (bonuses["dex"] / 2)), 0.1),
                        equipment_list.weapons_list[weapon_name]["crit_chance"]
                        + (bonuses["wis"] * 2))
                        return True
            if item_in[-1] == "potion" or item_in[-1] == "throwable":
                item_name = item_in[0]
                if len(self.potion_1) == 0 and len(self.potion_2) == 0:
                    self.add_potions_to_slot(1, (item_name, item_in[1]))
                elif len(self.potion_1) == 0:
                    if self.potion_2[0].name == item_name:
                        self.add_potions_to_slot(2, (item_name, item_in[1]))
                    else:
                        self.add_potions_to_slot(1, (item_name, item_in[1]))
                elif len(self.potion_2) == 0:
                    if self.potion_1[0].name == item_name:
                        self.add_potions_to_slot(1, (item_name, item_in[1]))
                    else:
                        self.add_potions_to_slot(2, (item_name, item_in[1]))
                else:
                    # both slots contain potions
                    if self.potion_1[0].name == item_name:
                        self.add_potions_to_slot(1, (item_name, item_in[1]))
                    elif self.potion_2[0].name == item_name:
                        self.add_potions_to_slot(2, (item_name, item_in[1]))
                    else:
                        # current potions are of different type and cannot be added to
                        return False

            return False

    def remove_from_hotbar(self, index):
        if index <= 2:
            # item is weapon
            if self.items[index] is not None:
                item_name = self.items[index].name
                self.items[index] = None
                return [item_name, 1, "weapon"]
        else:
            # item is consumable or throwable
            if index == 3:
                if len(self.potion_1) != 0:
                    item_name = self.potion_1[0].name
                    quantity = len(self.potion_1)
                    if self.potion_1[0].is_throwable:
                        self.potion_1 = []
                        return [item_name, quantity, "throwable"]
                    else:
                        self.potion_1 = []
                        return [item_name, quantity, "potion"]
            if index == 4:
                if len(self.potion_2) != 0:
                    item_name = self.potion_2[0].name
                    quantity = len(self.potion_2)
                    if self.potion_2[0].is_throwable:
                        self.potion_2 = []
                        return [item_name, quantity, "throwable"]
                    else:
                        self.potion_2 = []
                        return [item_name, quantity, "potion"]
        # nothing to remove
        return None

    def swap_inventory(self, item_1_location, item_2_location):
        # hotbar 0-4, inventory_5-30, shop 31+
        item = None
        if item_1_location < 5:
            if item_2_location < 5:
                return False
            removed = self.remove_from_hotbar(item_1_location)
            if 4 < item_2_location < 30:
                self.add_to_hotbar(self.inventory[item_2_location - 5])
                self.inventory[item_2_location - 5] = removed
            else:
                pass
        elif 4 < item_1_location < 30:
            item = self.inventory[item_1_location - 5]
            if item_2_location < 5:
                removed = self.remove_from_hotbar(item_2_location)
                self.inventory[item_1_location - 5] = removed
                self.add_to_hotbar(item)
            elif 4 < item_2_location < 30:
                self.inventory[item_1_location - 5] = self.inventory[item_2_location - 5]
                self.inventory[item_2_location - 5] = item
            else:
                pass
        else:
            pass

