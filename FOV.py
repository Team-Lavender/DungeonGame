import pygame
import config
import game

def blurSurf(surface, amt):
    """
    Blur the given surface by the given 'amount'.  Only values 1 and greater
    are valid.  Value 1 = no blur.
    """
    if amt < 1.0:
        raise ValueError("Arg 'amt' must be greater than 1.0, passed in value is %s"%amt)
    scale = 1.0/float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf

class FOV:
    def __init__(self, game, radius):
        self.radius = radius
        self.game = game



    def draw_fov(self):
        if self.game.fov:
            fill = config.DARK
        else:
            fill = config.WHITE
        fov_surface = pygame.Surface((config.GAME_WIDTH, config.GAME_HEIGHT))
        fov_surface.fill(fill)
        player = self.game.curr_actors[0]
        pointset = self.calculate_fov(player.pos_x, player.pos_y)
        pygame.draw.polygon(fov_surface, config.FOV_COLOR, pointset)
        fov_surface = blurSurf(fov_surface, 50)
        self.game.display.blit(fov_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def calculate_fov(self, center_x, center_y):
        pointset = []
        for ray_angle in range(0, 360):
            ray = pygame.Vector2()
            for ray_length in range(0, self.radius, 10):
                ray.from_polar((ray_length, ray_angle))
                offset = pygame.Vector2(center_x, center_y)
                ray += offset
                if (ray[0] // 16, ray[1] // 16) in self.game.curr_map.wall:
                    break

            pointset.append((ray[0], ray[1]))

        return tuple(pointset)
