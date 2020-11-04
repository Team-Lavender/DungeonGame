
import config
from entities import *

from weapon import*

class Player(Entity):
    def __init__(self, game, pos_x, pos_y, sprite, health, shield, has_ai, entity_level, entity_status, move_speed,
                 money):
        super(Player, self).__init__(game, pos_x, pos_y, sprite, health, shield, has_ai, entity_level, entity_status,
                                     move_speed)
        self.money = money

        self.items = \
            [Weapon(game, self.pos_x, self.pos_y, config.get_weapon_sprite("knight_sword"), 1,1, "melee", 1, 1, 2, 5),
             Weapon(game, self.pos_x, self.pos_y, config.get_weapon_sprite("rusty_sword"), 1,1, "melee", 1, 1, 1, 5),
             Weapon(game, self.pos_x, self.pos_y, config.get_weapon_sprite("bow"), 1,1, "melee", 1, 1, 0.5, 5)]
        self.held_item = self.items[0]
        self.held_item.in_inventory = False
        self.look_direction = pygame.Vector2(1, 0)

    def use_item(self):
        if isinstance(self.held_item, Weapon) and\
                pygame.time.get_ticks() - self.held_item.last_used >= 1000 * self.held_item.attack_speed:
            self.held_item.state = "blast"
            self.held_item.last_used = pygame.time.get_ticks()
            self.attack()
        else:
            pass

    def swap_item(self, next_or_prev):
        if len(self.items) > 0:
            self.held_item.in_inventory = True
            self.held_item = self.items[(self.items.index(self.held_item) + next_or_prev) % len(self.items)]
            self.held_item.in_inventory = False
        else:
            pass

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
            direction.scale_to_length(self.move_speed)
        self.move(direction)
        dx, dy = 0, 0

        mouse_vector = pygame.mouse.get_pos()
        look_vector = pygame.Vector2((mouse_vector[0] - self.pos_x), (mouse_vector[1] - self.pos_y))
        self.look_direction = look_vector.normalize()
        if isinstance(self.held_item, Weapon):
            self.held_item.pos_x = self.pos_x
            self.held_item.pos_y = self.pos_y
            self.held_item.target_direction = self.look_direction
            self.held_item.angle = self.look_direction.angle_to(pygame.Vector2(0, -1))

        if self.game.ACTION:
            self.use_item()

        if self.game.SCROLL_UP:
            self.swap_item(1)

        if self.game.SCROLL_DOWN:
            self.swap_item(-1)

    def mine(self):
        pass
