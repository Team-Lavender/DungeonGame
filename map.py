import pygame
import config
import configparser

LEVEL1_ROOMS = {1:(0, 0, 'T'), 2:(0, 1, 'E')}
ROOMS_IMG = {'T': 'room_top.png', 'B': 'room_bottom.png', 'R': 'room_right.png', 'L': 'room_left.png', 'E': 'room.png'}

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
        self.object = set()
        self.plant = set()
        self.floor = set()
        self.door = set()

        self.cutscenes = set()
        self.cutscene_1 = set()
        self.cutscene_2 = set()

        self.spawn = (0, 0)
        self.enemies = set()

        self.parser = configparser.ConfigParser()
        self.map_parser("mapframe.txt")
        self.current_map = 0
        self.generate_map("map1")

    def map_parser(self, filename):
        """parse all maps and tiles from the file, store them in separate dict"""
        self.parser.read(filename)

    def generate_map(self, target_map):
        self.current_map = int(target_map[-1])
        # clear current map sets
        self.unpassable = set()
        self.wall = set()
        self.object = set()
        self.plant = set()
        self.floor = set()
        self.door = set()
        self.cutscenes = set()
        self.cutscene_1 = set()
        self.cutscene_2 = set()
        self.spawn = (0, 0)
        self.enemies = set()

        map = self.parser.get(str(target_map), str(target_map)).split("\n")
        map1_width=67
        map1_height=35
        map2_width=67
        map2_height=35
        map3_width=181
        map3_height=64
        for y, line in enumerate(map):
            for x, patch in enumerate(line):
                if patch == 'w':
                    self.wall.add((x + (68/2-int(map_width/2)) + self.map_offset[0], y + (34/2-int(map_height/2)) + self.map_offset[1]))
                    self.unpassable.add((x + (68/2-int(map_width/2)) + self.map_offset[0], y + (34/2-int(map_height/2)) + self.map_offset[1]))
                elif patch == '-':
                    self.floor.add((x +(68/2-int(map_width/2)) + self.map_offset[0], y + (34/2-int(map_height/2)) + self.map_offset[1]))
                elif patch == 'S':
                    self.floor.add((x + (68/2-int(map_width/2)) + self.map_offset[0], y + (34/2-int(map_height/2)) + self.map_offset[1]))
                    self.spawn = ((x + (68/2-int(map_width/2)) + self.map_offset[0]) * 16, (y + (34/2-int(map_height/2)) + self.map_offset[1]) * 16)
                elif patch == 'e' or patch == 'E':
                    self.floor.add((x + (68/2-int(map_width/2)) + self.map_offset[0], y + (34/2-int(map_height/2)) + self.map_offset[1]))
                    self.enemies.add(((x + (68/2-int(map_width/2)) + self.map_offset[0]) * 16, (y + (34/2-int(map_height/2)) + self.map_offset[1]) * 16, patch))
                elif patch == 'p':
                    self.plant.add((x + (68/2-int(map_width/2)) + self.map_offset[0], y + (34/2-int(map_height/2)) + self.map_offset[1]))
                    self.unpassable.add((x + (68/2-int(map_width/2)) + self.map_offset[0], y + (34/2-int(map_height/2)) + self.map_offset[1]))
                elif patch == 't':
                    self.object.add((x + (68/2-int(map_width/2)) + self.map_offset[0], y + (34/2-int(map_height/2)) + self.map_offset[1]))
                    self.unpassable.add((x + (68/2-int(map_width/2)) + self.map_offset[0], y + (34/2-int(map_height/2)) + self.map_offset[1]))
                # elif patch == 'd':
                #   self.unpassable.add((x + (68/2-int(map_width/2)) + self.map_offset[0], y + (34/2-int(map_height/2)) + self.map_offset[1]))
                elif patch == 'a':
                    self.cutscene_1.add((x + (68/2-int(map_width/2)) + self.map_offset[0], y + (34/2-int(map_height/2)) + self.map_offset[1]))
                    self.cutscenes.add((x + (68/2-int(map_width/2)) + self.map_offset[0], y + (34/2-int(map_height/2)) + self.map_offset[1]))
                elif patch == 'b':
                    self.cutscene_2.add((x + (68/2-int(map_width/2)) + self.map_offset[0], y + (34/2-int(map_height/2)) + self.map_offset[1]))
                    self.cutscenes.add((x + (68/2-int(map_width/2)) + self.map_offset[0], y + (34/2-int(map_height/2)) + self.map_offset[1]))
                elif patch == '1' or patch == '2' or patch == '3':
                    self.door.add((x + (68/2-int(map_width/2)) + self.map_offset[0], y + (34/2-int(map_height/2)) + self.map_offset[1], patch))
                    self.unpassable.add((x + (68/2-int(map_width/2)) + self.map_offset[0], y + (34/2-int(map_height/2)) + self.map_offset[1]))

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
        object = self.get_tiles(self.parser.get("tilesets", "object"))
        floor = self.get_tiles(self.parser.get("tilesets", "floor"))
        door = self.get_tiles(self.parser.get("tilesets", "door"))

        cutscene = self.get_tiles(self.parser.get("tilesets", "cutscene"))

        # draw non-wall objects
        for x, y in self.plant:
            self.game.display.blit(floor, (x * 16, y * 16))
            self.game.display.blit(plant, (x * 16, y * 16))
        for x, y in self.object:
            self.game.display.blit(floor, (x * 16, y * 16))
            self.game.display.blit(object, (x * 16, y * 16))
        for x, y in self.floor:
            self.game.display.blit(floor, (x * 16, y * 16))
        for x, y in self.cutscene_1:
            self.game.display.blit(cutscene, (x * 16, y * 16))
        for x, y in self.cutscene_2:
            self.game.display.blit(cutscene, (x * 16, y * 16))

        # draw walls

        for x, y in self.wall:
            value = self.wall_render(x, y)
            if value == 1:  # top middle
                self.game.display.blit(wall_mid, (x * 16, y * 16))
                self.game.display.blit(wall_top_mid, (x * 16, (y - 1) * 16))
            elif value == 2:  # bottom middle
                self.game.display.blit(wall_mid, (x * 16, (y - 0.3 + (1 - self.render_space)) * 16))
                self.game.display.blit(wall_top_mid, (x * 16, (y - 0.3 - self.render_space) * 16))
            elif value == 3:  # left side
                self.game.display.blit(wall_side_mid_left, (x * 16, y * 16))
            elif value == 4:  # right side
                self.game.display.blit(wall_side_mid_right, (x * 16, y * 16))
            elif value == 5:  # inner top left corner
                self.game.display.blit(wall_left, (x * 16, y * 16))
                self.game.display.blit(wall_top_left, (x * 16, (y - 1) * 16))
            elif value == 6:  # inner bottom left corner
                self.game.display.blit(wall_inner_corner_mid_left, (x * 16, (y - 0.3 + (1 - self.render_space)) * 16))
                self.game.display.blit(wall_corner_top_left, (x * 16, (y - 0.3 - self.render_space) * 16))
            elif value == 7:  # outer top left corner
                self.game.display.blit(wall_side_mid_left, (x * 16, y * 16))
                self.game.display.blit(wall_side_top_left, (x * 16, (y - 1) * 16))
            elif value == 8:  # outer bottom left corner
                self.game.display.blit(wall_side_front_left, (x * 16, (y - 0.3 + (1 - self.render_space)) * 16))
                self.game.display.blit(wall_side_top_left, (x * 16, (y - 0.3 - self.render_space) * 16))
            elif value == 9:  # inner top right corner
                self.game.display.blit(wall_right, (x * 16, y * 16))
                self.game.display.blit(wall_top_right, (x * 16, (y - 1) * 16))
            elif value == 10:  # inner bottom right corner
                self.game.display.blit(wall_inner_corner_mid_right, (x * 16, (y - 0.3 + (1 - self.render_space)) * 16))
                self.game.display.blit(wall_corner_top_right, (x * 16, (y - 0.3 - self.render_space) * 16))
            elif value == 11:  # outer top right corner
                self.game.display.blit(wall_side_mid_right, (x * 16, y * 16))
                self.game.display.blit(wall_side_top_right, (x * 16, (y - 1) * 16))
            elif value == 12:  # outer bottom left corner
                self.game.display.blit(wall_side_front_right, (x * 16, (y - 0.3 + (1 - self.render_space)) * 16))
                self.game.display.blit(wall_side_top_right, (x * 16, (y - 0.3 - self.render_space) * 16))

        # draw doors
        for x, y, patch in self.door:
            door_rect = door.get_rect()
            door_rect.midbottom = (x * 16, (y + 1) * 16)
            self.game.display.blit(door, door_rect)


        self.minimap()
        
    def get_tiles(self, tile):
        return pygame.image.load(tile)

    def is_wall(self, x, y):
        return (x, y) in self.wall

    def is_floor(self, x, y):
        """ Check if (x, y) is floor or other objects except walls. """
        return (x, y) in self.floor or (x, y) in self.object or (x, y) in self.plant

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


    def minimap(self):
        size = 16
        scale = (20, 15)
        # place a minimap on the top center
        self.mini_img = pygame.Surface((int(self.map_offset[0] * scale[0]), int(self.map_offset[1] * scale[1])))
        self.mini_img.fill((53, 44, 43))
        mini_rect = self.mini_img.get_rect(center=(config.GAME_WIDTH / 2, (self.map_offset[1] * scale[1])/2))

        # draw rooms
        for room in LEVEL1_ROOMS.keys():
            spec = LEVEL1_ROOMS[room]
            self.mini_img.blit(pygame.transform.scale(self.get_tiles("./assets/frames/" + ROOMS_IMG[spec[2]]), (size, size)), ((spec[0]+1) * size, (spec[1]+1) * size))
        # self.mini_img.blit(pygame.transform.scale(self.get_tiles("./assets/frames/room.png"), (16, 16)), (4, 4))



        self.game.display.blit(self.mini_img, mini_rect)

