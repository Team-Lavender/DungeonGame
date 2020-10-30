import pygame
import math
import config
import vectors

pygame.init()
game_display = pygame.display.set_mode((config.GAME_WIDTH, config.GAME_HEIGHT))
clock = pygame.time.Clock()
print(clock)

ACTORS = []
frame_count = 0


def in_window(x, y):
    return config.GAME_HEIGHT > y > 0 and config.GAME_WIDTH > x > 0


class Actor:

    def __init__(self, name, pos_x, pos_y, sprite):
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.sprite = sprite
        self.sprite_state = "idle"
        self.direction = (0, -1)
        ACTORS.append(self)

    def render(self):
        x_offset = 0
        y_offset = 0
        frame = self.sprite[self.sprite_state][0]
        if isinstance(self, Player):
            self.update_target_direction()
        if isinstance(self, Weapon):
            x_offset = self.direction[0] * 16
            y_offset =  self.direction[1] * 16
        image = pygame.transform.rotate(frame, vectors.get_angle(self.direction))
        if in_window(self.pos_x, self.pos_y):
            game_display.blit(image, (self.pos_x + (frame.get_width() // 2) + x_offset, self.pos_y + (frame.get_height() // 2) + y_offset))

            if frame_count == 0:
                self.update_sprite()

    def change_sprite_state(self, state="idle"):
        self.sprite_state = state

    def update_sprite(self):
        if len(self.sprite[self.sprite_state]) > 1:
            temp = self.sprite[self.sprite_state][0]
            self.sprite[self.sprite_state][0] = self.sprite[self.sprite_state][1]
            self.sprite[self.sprite_state][1] = self.sprite[self.sprite_state][2]
            self.sprite[self.sprite_state][2] = self.sprite[self.sprite_state][3]
            self.sprite[self.sprite_state][3] = temp


class Entity(Actor):
    def __init__(self, name, pos_x, pos_y, sprite, health, shield, level, move_speed):
        super(Entity, self).__init__(name, pos_x, pos_y, sprite)
        self.health = health
        self.shield = shield
        self.entity_level = level
        self.move_speed = move_speed

    def move(self, dx, dy):
        self.change_sprite_state("run")
        if dx == 0 and dy == 0:
            self.change_sprite_state()
        else:
            vector_length = math.sqrt(dx ** 2 + dy ** 2)
            self.pos_x += (dx / vector_length) * self.move_speed
            self.pos_y += (dy / vector_length) * self.move_speed

    # TODO fill in attack method
    def attack(self,):
        pass


class Player(Entity):
    def __init__(self, name, pos_x, pos_y, sprite, health, shield, level, move_speed, money):
        super(Player, self).__init__(name, pos_x, pos_y, sprite, health, shield, level, move_speed)
        self.money = money
        self.items = {}
        self.held_item = Weapon("sword", self.pos_x, self.pos_y, config.SWORD, 1, 5, "melee", 1, 3, 1, 5)
        self.target_direction = (1, 1)

    def use_item(self, direction=(1, 1)):
        if isinstance(self.held_item, Weapon):
            self.attack(direction)

    # TODO fill in swap item method
    def swap_item(self):
        pass

    def update_target_direction(self):
        self.target_direction = vectors.get_direction((self.pos_x, self.pos_y), pygame.mouse.get_pos())

    def get_input(self):
        dx = 0
        dy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_s]:
            dy = 1
        if keys[pygame.K_d]:
            dx = 1
        self.move(dx, dy)
        self.held_item.pos_x = self.pos_x
        self.held_item.pos_y = self.pos_y + 8
        buttons = pygame.mouse.get_pressed(3)
        self.target_direction = vectors.get_direction((self.pos_x, self.pos_y), pygame.mouse.get_pos())
        self.held_item.direction = self.target_direction



class Item(Actor):
    def __init__(self, name, pos_x, pos_y, sprite, item_level, cost, combat_style):
        super(Item, self).__init__(name, pos_x, pos_y, sprite)
        self.item_level = item_level
        self.cost = cost
        self.combat_style = combat_style

    # TODO define equip method
    def equip(self):
        pass

    # TODO define destroy method
    def destroy(self):
        pass


class Weapon(Item):
    def __init__(self, name, pos_x, pos_y, sprite, item_level, cost, combat_style, attack_range, dmg, speed,
                 crit_chance):
        super(Weapon, self).__init__(name, pos_x, pos_y + 8, sprite, item_level, cost, combat_style)
        self.attack_range = attack_range
        self.attack_damage = dmg
        self.attack_speed = speed
        self.crit_chance = crit_chance


class Game:

    def __init__(self):
        main_loop()


def main_loop():
    global frame_count
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game_display.fill(config.BLACK)
        for actor in ACTORS:
            player.get_input()
            actor.render()
        pygame.display.flip()
        frame_count = (frame_count + 1) % 6

        clock.tick(60)


player = Player("player", 10, 10, config.PLAYER, 10, 10, 1, 2.5, 0)
Game()
