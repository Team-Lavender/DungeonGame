import pygame
import config
import configparser

class Map:
    def __init__(self, game, height, width):
        self.game = game
        self.height = height
        self.width = width
        # self.unpassable = set()
        # self.wall = set((x,y), ...)
        # self.chest = set()
        # self.plant = set()
        # self.generate_map()

    def generate_map(self, filename):
        parser = configparser.ConfigParser()
        parser.read(filename)
        wall = self.get_tiles(parser.get("tilesets", "wall"))
        plant = self.get_tiles(parser.get("tilesets", "plant"))
        chest = self.get_tiles(parser.get("tilesets", "object"))
        map = parser.get("map1", "map1").split("\n")
        for y, line in enumerate(map):
            for x, patch in enumerate(line):
                if patch == 'w':
                    self.game.display.blit(wall, ((x+1) * 16, (y+1) * 16))
                elif patch == 'p':
                    self.game.display.blit(plant, ((x+1) * 16, (y+1) * 16))
                elif patch == 't':
                    self.game.display.blit(chest, ((x + 1) * 16, (y + 1) * 16))

    # draw_map

    def get_tiles(self, tile):
        return pygame.image.load(tile)


if __name__ == "__main__":
    screen = pygame.display.set_mode((config.GAME_WIDTH, config.GAME_HEIGHT))
    pygame.init()
    map = Map(config.GAME_WIDTH, config.GAME_HEIGHT)
    loop = 1
    while loop:
        screen.fill((0, 0, 0))
        map.generate_map("mapframe.txt")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
            pygame.display.update()
    pygame.quit()

