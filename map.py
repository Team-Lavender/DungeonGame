import pygame
import config
import configparser


class Map:
    def __init__(self, game, height, width):
        self.game = game
        self.render_space = 0.7
        self.map_offset = (5, 5)
        self.map_set = {}
        self.height = height
        self.width = width
        self.unpassable = set()
        self.wall = set()
        self.chest = set()
        self.plant = set()
        self.floor = set()
        self.spawn = (0, 0)
        self.enemies = set()
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
                    self.wall.add((x + self.map_offset[0], y + self.map_offset[1]))
                    self.unpassable.add((x + self.map_offset[0], y + self.map_offset[1]))
                elif patch == '-':
                    self.floor.add((x + self.map_offset[0], y + self.map_offset[1]))
                elif patch == 'S':
                    self.floor.add((x + self.map_offset[0], y + self.map_offset[1]))
                    self.spawn = ((x + self.map_offset[0]) * 16, (y + self.map_offset[1]) * 16)
                elif patch == 'e' or patch == 'E':
                    self.floor.add((x + self.map_offset[0], y + self.map_offset[1]))
                    self.enemies.add(((x + self.map_offset[0]) * 16, (y + self.map_offset[1]) * 16, patch))
                elif patch == 'p':
                    self.plant.add((x + self.map_offset[0], y + self.map_offset[1]))
                    self.unpassable.add((x + self.map_offset[0], y + self.map_offset[1]))
                elif patch == 't':
                    self.chest.add((x + self.map_offset[0], y + self.map_offset[1]))
                    self.unpassable.add((x + self.map_offset[0], y + self.map_offset[1]))
                elif patch == 'd':
                    self.unpassable.add((x + self.map_offset[0], y + self.map_offset[1]))

    def draw_map(self):
        # extract wall tiles
        wall_mid = self.get_tiles(self.parser.get("tilesets", "wall_mid"))
        wall_left = self.get_tiles(self.parser.get("tilesets", "wall_left"))
        wall_right = self.get_tiles(self.parser.get("tilesets", "wall_right"))
        wall_top_mid = self.get_tiles(self.parser.get("tilesets", "wall_top_mid"))
        wall_top_left = self.get_tiles(self.parser.get("tilesets", "wall_top_left"))
        wall_top_right = self.get_tiles(self.parser.get("tilesets", "wall_top_right"))
        wall_side_mid_left = self.get_tiles(self.parser.get("tilesets", "wall_side_mid_left"))
        wall_side_mid_right = self.get_tiles(self.parser.get("tilesets", "wall_side_mid_right"))
        wall_inner_corner_mid_left = self.get_tiles(self.parser.get("tilesets", "wall_inner_corner_mid_left"))
        wall_inner_corner_mid_right = self.get_tiles(self.parser.get("tilesets", "wall_inner_corner_mid_right"))
        wall_corner_top_left = self.get_tiles((self.parser.get("tilesets", "wall_corner_top_left")))
        wall_corner_top_right = self.get_tiles((self.parser.get("tilesets", "wall_corner_top_right")))
        wall_side_front_left = self.get_tiles(self.parser.get("tilesets", "wall_side_front_left"))
        wall_side_front_right = self.get_tiles(self.parser.get("tilesets", "wall_side_front_right"))
        wall_side_top_left = self.get_tiles(self.parser.get("tilesets", "wall_side_top_left"))
        wall_side_top_right = self.get_tiles(self.parser.get("tilesets", "wall_side_top_right"))


        # extract other object tiles
        plant = self.get_tiles(self.parser.get("tilesets", "plant"))
        chest = self.get_tiles(self.parser.get("tilesets", "object"))
        floor = self.get_tiles(self.parser.get("tilesets", "floor"))
        # draw walls
        for x, y in self.wall:
            value = self.wall_render(x, y)
            if value == 1:  # top middle
                self.game.display.blit(wall_mid, (x * 16, y * 16))
                self.game.display.blit(wall_top_mid, (x * 16, (y - 1) * 16))
            elif value == 2:  # bottom middle
                self.game.display.blit(wall_mid, (x * 16, (y + (1 - self.render_space)) * 16))
                self.game.display.blit(wall_top_mid, (x * 16, (y - self.render_space) * 16))
            elif value == 3:  # left side
                self.game.display.blit(wall_side_mid_left, (x * 16, y * 16))
            elif value == 4:  # right side
                self.game.display.blit(wall_side_mid_right, (x * 16, y * 16))
            elif value == 5:  # inner top left corner
                self.game.display.blit(wall_left, (x * 16, y * 16))
                self.game.display.blit(wall_top_left, (x * 16, (y - 1) * 16))
            elif value == 6:  # inner bottom left corner
                self.game.display.blit(wall_inner_corner_mid_left, (x * 16, (y + (1 - self.render_space)) * 16))
                self.game.display.blit(wall_corner_top_left, (x * 16, (y - self.render_space) * 16))
            elif value == 7:  # outer top left corner
                self.game.display.blit(wall_side_mid_left, (x * 16, y * 16))
                self.game.display.blit(wall_side_top_left, (x * 16, (y - 1) * 16))
            elif value == 8:  # outer bottom left corner
                self.game.display.blit(wall_side_front_left, (x * 16, (y + (1 - self.render_space)) * 16))
                self.game.display.blit(wall_side_top_left, (x * 16, (y - self.render_space) * 16))
            elif value == 9:  # inner top right corner
                self.game.display.blit(wall_right, (x * 16, y * 16))
                self.game.display.blit(wall_top_right, (x * 16, (y - 1) * 16))
            elif value == 10:  # inner bottom right corner
                self.game.display.blit(wall_inner_corner_mid_right, (x * 16, (y + (1 - self.render_space)) * 16))
                self.game.display.blit(wall_corner_top_right, (x * 16, (y - self.render_space) * 16))
            elif value == 11:  # outer top right corner
                self.game.display.blit(wall_side_mid_right, (x * 16, y * 16))
                self.game.display.blit(wall_side_top_right, (x * 16, (y - 1) * 16))
            elif value == 12:  # outer bottom left corner
                self.game.display.blit(wall_side_front_right, (x * 16, (y + (1 - self.render_space)) * 16))
                self.game.display.blit(wall_side_top_right, (x * 16, (y - self.render_space) * 16))

        # draw other objects
        for x, y in self.plant:
            self.game.display.blit(plant, (x * 16, y * 16))
        for x, y in self.chest:
            self.game.display.blit(chest, (x * 16, y * 16))
        for x, y in self.floor:
            self.game.display.blit(floor, (x * 16, y * 16))

    def get_tiles(self, tile):
        return pygame.image.load(tile)

    def is_wall(self, x, y):
        return (x, y) in self.wall

    def is_floor(self, x, y):
        """ Check if (x, y) is floor or other objects except walls. """
        return (x, y) in self.floor or (x, y) in self.chest or (x, y) in self.plant

    def wall_render(self, x, y):
        tile_number = 0
        isWall = self.is_wall
        isFloor = self.is_floor

        if isWall(x - 1, y) and isWall(x + 1, y) and isFloor(x, y + 1):  # top middle
            tile_number = 1
        elif isWall(x - 1, y) and isWall(x + 1, y):  # bottom middle
            tile_number = 2
        elif isWall(x, y + 1) and isWall(x, y - 1) and isFloor(x + 1, y):  # left side
            tile_number = 3
        elif isWall(x, y + 1) and isWall(x, y - 1):  # right side
            tile_number = 4
        elif (isWall(x + 1, y) and isWall(x, y - 1)) and isFloor(x - 1, y + 1):  # inner top left corner
            tile_number = 5
        elif (isWall(x + 1, y) and isWall(x, y + 1)) and isFloor(x - 1, y - 1):  # inner bottom left corner
            tile_number = 6
        elif (isWall(x + 1, y) and isWall(x, y + 1)):  # outer top left corner
            tile_number = 7
        elif (isWall(x + 1, y) and isWall(x, y - 1)):  # outer bottom left corner
            tile_number = 8
        elif (isWall(x - 1, y) and isWall(x, y - 1)) and isFloor(x + 1, y + 1):  # inner top right corner
            tile_number = 9
        elif (isWall(x - 1, y) and isWall(x, y + 1)) and isFloor(x + 1, y - 1):  # inner bottom left corner
            tile_number = 10
        elif (isWall(x - 1, y) and isWall(x, y + 1)):  # outer top right corner
            tile_number = 11
        elif (isWall(x - 1, y) and isWall(x, y - 1)):  # outer bottom left corner
            tile_number = 12
        return tile_number

