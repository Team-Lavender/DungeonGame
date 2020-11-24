import pygame
import config
from item import *
import elemental_effects
import equipment_list
import audio

class Throwable(Item):
    def __init__(self, game, throwable_name):
        self.game = game
        self.player = self.game.curr_actors[0]
        self.name = throwable_name
        self.potion_type = equipment_list.throwables_list[self.name]["type"]
        super(Throwable, self).__init__(self.game, self.player.pos_x, self.player.pos_y,
                                        config.get_potion_sprite(equipment_list.throwables_list[self.name]["sprite_name"]),
                                        equipment_list.throwables_list[self.name]["level"], "none",
                                        equipment_list.throwables_list[self.name]["cost"])
        self.damage = equipment_list.throwables_list[self.name]["damage"]
        self.size = equipment_list.throwables_list[self.name]["element_size"]

        self.pos_x = self.player.pos_x
        self.pos_y = self.player.pos_y

        self.target_pos = (self.pos_x, self.pos_y)
        self.x_speed = 2
        self.y_speed = 1

        self.trajectory = []
        self.thrown = False
        self.is_throwable = True
        self.consumed = False
        self.targeting = False

    def use(self):
        if self.thrown:
            pass
        else:
            if self.targeting:
                self.thrown = True
                audio.throw()
            self.targeting = not self.targeting

    def parabola_step(self, x):

        t = x / self.x_speed
        g = 0.01
        y = (self.y_speed * t) - (0.5 * g * (t ** 2))
        return y

    def move(self):
        if len(self.trajectory) == 0:
            self.splash()
            self.thrown = False
        else:
            self.pos_x = self.trajectory[0][0]
            self.pos_y = self.trajectory[0][1]
            self.trajectory.pop(0)

    def splash(self):
        audio.bottle_break()
        if self.potion_type == "acid":
            self.acid_pool()
        elif self.potion_type == "explosive":
            self.explosion()
        else:
            pass
        self.consumed = True

    def acid_pool(self):
        elemental_effects.AcidPool(self.game, self.damage, self.size, self.target_pos[0], self.target_pos[1])

    def explosion(self):
        elemental_effects.Explosion(self.game, self.damage, self.size, self.target_pos[0], self.target_pos[1])

    def render(self):
        if self.thrown:
            self.game.display.blit(self.sprite["idle"][0], (self.pos_x, self.pos_y))

    def render_targeting(self):
        self.trajectory = []
        self.target_pos = pygame.mouse.get_pos()
        self.target_pos = self.stop_at_walls()
        self.x_speed = 2
        self.y_speed = 2

        y_offset = -1 * (self.target_pos[1] - self.player.pos_y)

        x_max = max(abs(self.target_pos[0] - self.player.pos_x), 20)
        self.x_speed *= x_max * 0.002
        self.y_speed = (y_offset * self.x_speed / x_max) + (0.5 * 0.01 * x_max / self.x_speed)

        for x_1 in range(0, round(x_max), math.ceil(7 * self.x_speed)):
            y_1 = -1 * self.parabola_step(abs(x_1))
            if self.target_pos[0] < self.player.pos_x:
                x_1 *= -1
            self.trajectory.append((x_1 + self.player.pos_x, y_1 + self.player.pos_y))
            pygame.draw.circle(self.game.display, config.GREEN, (x_1 + self.player.pos_x, y_1 + self.player.pos_y), 1)

    def stop_at_walls(self):
        target_vector = pygame.Vector2(self.target_pos[0], self.target_pos[1])
        target_vector -= pygame.Vector2(self.player.pos_x, self.player.pos_y)
        length = target_vector.length()
        for i in range(10, min(int(length), 500), 10):
            target_vector.scale_to_length(i)

            wall_hit = False
            for wall_pos in self.game.curr_map.wall:
                wall_vector = pygame.Vector2(wall_pos[0] * 16, wall_pos[1] * 16)

                wall_vector -= (target_vector + pygame.Vector2(self.player.pos_x, self.player.pos_y))

                if wall_vector.length() <= 16:
                    wall_hit = True
                    break
            if wall_hit:
                print(target_vector.length())
                break
        target_vector += pygame.Vector2(self.player.pos_x, self.player.pos_y)
        return tuple((target_vector[0], target_vector[1]))
