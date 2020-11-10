import pygame
import config
import configparser

class Map:
    def __init__(self, game, height, width):
        self.game = game
        self.map_set = {}
        self.height = height
        self.width = width
        self.unpassable = set()
        self.wall = set()
        self.chest = set()
        self.plant = set()
        self.floor = set()
        self.parser = configparser.ConfigParser()
        self.map_parser("mapframe.txt")
        self.generate_map("map1")

    def map_parser(self, filename):
        """parse all maps and tiles from the file, store them in separate dict"""
        self.parser.read(filename)

    def generate_map(self, target_map):
        map = self.parser.get(str(target_map), str(target_map)).split("\n")
        for y, line in enumerate(map):
            for x, patch in enumerate(line):
                if patch == 'w':
                    self.wall.add((x + 1, y + 1))
                    self.unpassable.add((x + 1, y + 1))
                elif patch == '-':
                    self.floor.add((x + 1, y + 1))
                    #self.unpassable.add((x + 1, y + 1))
                elif patch == 'p':
                    self.plant.add((x + 1, y + 1))
                    self.unpassable.add((x + 1, y + 1))
                elif patch == 't':
                    self.wall.add((x + 1, y + 1))
                    self.unpassable.add((x + 1, y + 1))
                elif patch == 'd':
                    self.unpassable.add((x + 1, y + 1))


    def draw_map(self):
        wall = self.get_tiles(self.parser.get("tilesets", "wall"))
        plant = self.get_tiles(self.parser.get("tilesets", "plant"))
        chest = self.get_tiles(self.parser.get("tilesets", "object"))
        floor = self.get_tiles(self.parser.get("tilesets", "floor"))
        for x, y in self.wall:
            self.game.display.blit(wall, (x * 16, y * 16))
        for x, y in self.plant:
            self.game.display.blit(plant, (x * 16, y * 16))
        for x, y in self.chest:
            self.game.display.blit(chest, (x * 16, y * 16))
        for x, y in self.floor:
            self.game.display.blit(floor, (x * 16, y * 16))


    def get_tiles(self, tile):
        return pygame.image.load(tile)


# if __name__ == "__main__":
#     screen = pygame.display.set_mode((config.GAME_WIDTH, config.GAME_HEIGHT))
#     pygame.init()
#     map = Map(config.GAME_WIDTH, config.GAME_HEIGHT)
#     loop = 1
#     while loop:
#         screen.fill((0, 0, 0))
#         map.generate_map("mapframe.txt")
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 loop = 0
#             pygame.display.update()
#     pygame.quit()

