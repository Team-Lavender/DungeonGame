import pygame
import config
import configparser


class Map:
    def __init__(self, game, height, width):
        self.game = game
        self.tool_bar = 5
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
                    self.wall.add((x, y + self.tool_bar))
                    self.unpassable.add((x, y + self.tool_bar))
                elif patch == '-':
                    self.floor.add((x, y + self.tool_bar))
                elif patch == 'p':
                    self.plant.add((x, y + self.tool_bar))
                    self.unpassable.add((x, y + self.tool_bar))
                elif patch == 't':
                    self.chest.add((x, y + self.tool_bar))
                    self.unpassable.add((x, y + self.tool_bar))
                elif patch == 'd':
                    self.unpassable.add((x, y + self.tool_bar))

    def draw_map(self):

        wall_mid = self.get_tiles(self.parser.get("tilesets", "wall_mid"))
        # wall_side_front_left = self.get_tiles(self.parser.get("tilesets", "wall_side_front_left"))
        # wall_side_front_right = self.get_tiles(self.parser.get("tilesets", "wall_side_front_right"))
        wall_side_mid_left = self.get_tiles(self.parser.get("tilesets", "wall_side_mid_left"))
        wall_side_mid_right = self.get_tiles(self.parser.get("tilesets", "wall_side_mid_right"))
        wall_inner_corner_mid_left = self.get_tiles(self.parser.get("tilesets", "wall_inner_corner_mid_left"))
        wall_top_left = self.get_tiles(self.parser.get("tilesets", "wall_top_left"))
        wall_inner_corner_mid_rigth = self.get_tiles(self.parser.get("tilesets", "wall_inner_corner_mid_rigth"))
        wall_top_right = self.get_tiles(self.parser.get("tilesets", "wall_top_right"))
        wall_top_mid = self.get_tiles(self.parser.get("tilesets", "wall_top_mid"))
        plant = self.get_tiles(self.parser.get("tilesets", "plant"))
        chest = self.get_tiles(self.parser.get("tilesets", "object"))
        floor = self.get_tiles(self.parser.get("tilesets", "floor"))
        for x, y in self.wall:

            value = self.wall_render(x, y)
            if value == 1:
                self.game.display.blit(wall_mid, (x * 16, y * 16))
                self.game.display.blit(wall_top_mid, (x * 16, (y - 1) * 16))
            # elif value == 2:
            #     self.game.display.blit(wall_side_front_left, (x * 16, y * 16))
            # elif value == 3:
            #     self.game.display.blit(wall_side_front_right, (x * 16, y * 16))
            elif value == 4:
                self.game.display.blit(wall_side_mid_left, ((x-0.7) * 16, y * 16))
            elif value == 5:
                self.game.display.blit(wall_side_mid_right, ((x+0.7) * 16, y * 16))
            elif value == 6:
                self.game.display.blit(wall_inner_corner_mid_left, (x * 16, y * 16))
                self.game.display.blit(wall_top_left, (x * 16, (y - 1) * 16))
            elif value == 7:
                self.game.display.blit(wall_inner_corner_mid_rigth, (x * 16, y * 16))
                self.game.display.blit(wall_top_right, (x * 16, (y - 1) * 16))

        for x, y in self.plant:
            self.game.display.blit(plant, (x * 16, y * 16))
        for x, y in self.chest:
            self.game.display.blit(chest, (x * 16, y * 16))
        for x, y in self.floor:
            self.game.display.blit(floor, (x * 16, y * 16))

    def get_tiles(self, tile):
        return pygame.image.load(tile)

    def is_wall(self, x, y):
        test = set()
        test.add((x, y))
        return self.wall.issuperset(test)

    def is_floor(self, x, y):
        test = set()
        test.add((x, y))
        return self.floor.issuperset(test)

    def wall_render(self, x, y):
        tile_number = 0
        isWall = self.is_wall
        isFloor = self.is_floor

        if isWall(x - 1, y) and isWall(x + 1, y):
            tile_number = 1
        elif isWall(x, y + 1) and isWall(x, y - 1) and isFloor(x + 1, y):
            tile_number = 4
        elif isWall(x, y + 1) and isWall(x, y - 1) and isFloor(x - 1, y):
            tile_number = 5
        elif (isWall(x + 1, y) and isWall(x, y + 1)) or (isWall(x + 1, y) and isWall(x, y - 1)):
            tile_number = 6
        elif (isWall(x - 1, y) and isWall(x, y + 1)) or (isWall(x + 1, y) and isWall(x, y - 1)):
            tile_number = 7
        return tile_number

