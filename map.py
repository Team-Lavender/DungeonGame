import pygame
import random
import configparser
from config import *
from game import *


class Map:
    """The max size of map is 67*33 before multiplying the pixel."""
    def __init__(self, game, height, width):
        self.game = game
        self.render_space = 0.7
        self.map_offset = (5, 5)

        self.height = height
        self.width = width
        self.unpassable = set()
        self.wall = set()
        self.object = set()
        self.plant = set()
        self.floor = set()
        self.door = set()
        self.floor_render = set()
        self.mid_wall_render = set()

        self.cutscenes = set()
        self.cutscene_1 = set()
        self.cutscene_2 = set()

        self.spawn = (0, 0)
        self.enemies = set()

        self.parser = configparser.ConfigParser()
        self.map_parser("mapframe.txt")
        self.current_map = 0
        self.current_level = 0

        # extract wall tiles
        self.wall_mid = self.get_tiles(self.parser.get("tilesets", "wall_mid"))
        self.wall_left = self.get_tiles(self.parser.get("tilesets", "wall_left"))
        self.wall_right = self.get_tiles(self.parser.get("tilesets", "wall_right"))
        self.wall_top_mid = self.get_tiles(self.parser.get("tilesets", "wall_top_mid"))
        self.wall_top_left = self.get_tiles(self.parser.get("tilesets", "wall_top_left"))
        self.wall_top_right = self.get_tiles(self.parser.get("tilesets", "wall_top_right"))
        self.wall_side_mid_left = self.get_tiles(self.parser.get("tilesets", "wall_side_mid_left"))
        self.wall_side_mid_right = self.get_tiles(self.parser.get("tilesets", "wall_side_mid_right"))
        self.wall_inner_corner_mid_left = self.get_tiles(self.parser.get("tilesets", "wall_inner_corner_mid_left"))
        self.wall_inner_corner_mid_right = self.get_tiles(self.parser.get("tilesets", "wall_inner_corner_mid_right"))
        self.wall_corner_top_left = self.get_tiles((self.parser.get("tilesets", "wall_corner_top_left")))
        self.wall_corner_top_right = self.get_tiles((self.parser.get("tilesets", "wall_corner_top_right")))
        self.wall_side_front_left = self.get_tiles(self.parser.get("tilesets", "wall_side_front_left"))
        self.wall_side_front_right = self.get_tiles(self.parser.get("tilesets", "wall_side_front_right"))
        self.wall_side_top_left = self.get_tiles(self.parser.get("tilesets", "wall_side_top_left"))
        self.wall_side_top_right = self.get_tiles(self.parser.get("tilesets", "wall_side_top_right"))
        self.wall_hole1 = self.get_tiles(self.parser.get("tilesets", "wall_hole1"))
        self.wall_hole2 = self.get_tiles(self.parser.get("tilesets", "wall_hole2"))
        self.wall_banner_blue = self.get_tiles(self.parser.get("tilesets", "wall_banner_blue"))

        # extract other object tiles
        self.plant_tile = self.get_tiles(self.parser.get("tilesets", "plant"))
        self.object_tile = self.get_tiles(self.parser.get("tilesets", "object"))
        self.floor_tile = self.get_tiles(self.parser.get("tilesets", "floor"))
        self.door_tile = self.get_tiles(self.parser.get("tilesets", "door"))

        self.floor_tile1 = self.get_tiles(self.parser.get("tilesets", "floor1"))
        self.floor_tile2 = self.get_tiles(self.parser.get("tilesets", "floor2"))
        self.floor_tile3 = self.get_tiles(self.parser.get("tilesets", "floor3"))
        self.floor_tile4 = self.get_tiles(self.parser.get("tilesets", "floor4"))
        self.floor_tile5 = self.get_tiles(self.parser.get("tilesets", "floor5"))

        # form a tuple of versatile mid wall tiles and floor
        self.wall_mid_tuple = (self.wall_mid, self.wall_hole1, self.wall_hole2, self.wall_banner_blue)
        self.floor_tile_tuple = (
        self.floor_tile, self.floor_tile1, self.floor_tile2, self.floor_tile3, self.floor_tile4, self.floor_tile5)

        self.minimap()
        self.generate_map("map1")

    def map_width(self, map):
        width = len(map[0])
        return width

    def map_height(self, map):
        height = len(map)
        return height

    def centralise_map(self, map):
        map_offset_width = round(1280 / 16 / 2 - int(self.map_width(map) / 2))
        map_offset_height = round(720 / 16 / 2 - int(self.map_height(map) / 2))
        return (map_offset_width, map_offset_height)

    
    def map_parser(self, filename):
        """parse all maps and tiles from the file, store them in separate dict"""
        self.parser.read(filename)

    def generate_map(self, target_map):
        self.current_map = int(target_map[-1])
        # need to define how to transition to level
        self.current_level = 1
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
        self.floor_render = set()

        # for generate random wall tiles
        self.rand = random.sample(range(30, 100), 3)

        self.build_minimap()



        map = self.parser.get(str(target_map), str(target_map)).split("\n")
        self.map_offset = self.centralise_map(map)

        for y, line in enumerate(map):
            for x, patch in enumerate(line):
                if patch == 'w':
                    self.wall.add((x + self.map_offset[0], y + self.map_offset[1]))
                    self.unpassable.add((x + self.map_offset[0], y + self.map_offset[1]))
                elif patch == '-':
                    self.floor.add((x + self.map_offset[0], y + self.map_offset[1]))
                    tile_num = self.rand_tiles(len(self.floor_tile_tuple))
                    self.floor_render.add((x + self.map_offset[0], y + self.map_offset[1], tile_num))
                    # self.floor_render.add((x + self.map_offset[0], y + self.map_offset[1], 0))
                elif patch == 'S':
                    self.floor.add((x + self.map_offset[0], y + self.map_offset[1]))
                    self.floor_render.add((x + self.map_offset[0], y + self.map_offset[1], 0))
                    self.spawn = ((x + self.map_offset[0]) * 16, (y + self.map_offset[1]) * 16)
                elif patch == 'e' or patch == 'E':
                    self.floor.add((x + self.map_offset[0], y + self.map_offset[1]))
                    self.floor_render.add((x + self.map_offset[0], y + self.map_offset[1], 0))
                    self.enemies.add(((x + self.map_offset[0]) * 16, (y + self.map_offset[1]) * 16, patch))
                elif patch == 'p':
                    self.plant.add((x + self.map_offset[0], y + self.map_offset[1]))
                    self.unpassable.add((x + self.map_offset[0], y + self.map_offset[1]))
                elif patch == 't':
                    self.object.add((x + self.map_offset[0], y + self.map_offset[1]))
                    self.unpassable.add((x + self.map_offset[0], y + self.map_offset[1]))
                elif patch == 'a':
                    self.floor.add((x + self.map_offset[0], y + self.map_offset[1]))
                    self.floor_render.add((x + self.map_offset[0], y + self.map_offset[1], 0))
                    self.cutscene_1.add((x + self.map_offset[0], y + self.map_offset[1]))
                    self.cutscenes.add((x + self.map_offset[0], y + self.map_offset[1]))
                elif patch == 'b':
                    self.cutscene_2.add((x + self.map_offset[0], y + self.map_offset[1]))
                    self.cutscenes.add((x + self.map_offset[0], y + self.map_offset[1]))
                elif patch.isnumeric() and int(patch) <= 16:
                    if line[x+1].isnumeric():
                        self.wall.add((x + self.map_offset[0], y + self.map_offset[1]))
                        self.unpassable.add((x + self.map_offset[0], y + self.map_offset[1]))
                    elif line[x-1].isnumeric():
                        self.door.add((x + self.map_offset[0], y + self.map_offset[1], '1'+patch))
                        self.unpassable.add((x + self.map_offset[0], y + self.map_offset[1]))
                    else:
                        self.door.add((x + self.map_offset[0], y + self.map_offset[1], patch))
                        self.unpassable.add((x + self.map_offset[0], y + self.map_offset[1]))



    def draw_map(self):

        cutscene = self.get_tiles(self.parser.get("tilesets", "cutscene"))

        # draw non-wall objects
        for x, y in self.plant:
            self.game.display.blit(self.floor_tile, (x * 16, y * 16))
            self.game.display.blit(self.plant_tile, (x * 16, y * 16))
        for x, y in self.object:
            self.game.display.blit(self.floor_tile, (x * 16, y * 16))
            self.game.display.blit(self.object_tile, (x * 16, y * 16))
        for x, y, tilenum in self.floor_render:
            self.game.display.blit(self.floor_tile_tuple[tilenum], (x * 16, y * 16))
        for x, y in self.cutscene_1:
            self.game.display.blit(cutscene, (x * 16, y * 16))
        for x, y in self.cutscene_2:
            self.game.display.blit(cutscene, (x * 16, y * 16))



        # draw walls

        for x, y in self.wall:
            value = self.wall_render(x, y)
            if value == 1:  # top middle
                num = self.rand_wall(x, y, len(self.wall_mid_tuple))
                # num = self.rand_tiles(len(self.wall_mid_tuple))
                self.game.display.blit(self.wall_mid_tuple[num], (x * 16, y * 16))
                self.game.display.blit(self.wall_top_mid, (x * 16, (y - 1) * 16))
            elif value == 2:  # bottom middle
                self.game.display.blit(self.wall_mid, (x * 16, (y - 0.3 + (1 - self.render_space)) * 16))
                self.game.display.blit(self.wall_top_mid, (x * 16, (y - 0.3 - self.render_space) * 16))
            elif value == 3:  # left side
                self.game.display.blit(self.wall_side_mid_left, (x * 16, y * 16))
            elif value == 4:  # right side
                self.game.display.blit(self.wall_side_mid_right, (x * 16, y * 16))
            elif value == 5:  # inner top left corner
                self.game.display.blit(self.wall_left, (x * 16, y * 16))
                self.game.display.blit(self.wall_top_left, (x * 16, (y - 1) * 16))
            elif value == 6:  # inner bottom left corner
                self.game.display.blit(self.wall_inner_corner_mid_left, (x * 16, (y - 0.3 + (1 - self.render_space)) * 16))
                self.game.display.blit(self.wall_corner_top_left, (x * 16, (y - 0.3 - self.render_space) * 16))
            elif value == 7:  # outer top left corner
                self.game.display.blit(self.wall_side_mid_left, (x * 16, y * 16))
                self.game.display.blit(self.wall_side_top_left, (x * 16, (y - 1) * 16))
            elif value == 8:  # outer bottom left corner
                self.game.display.blit(self.wall_side_front_left, (x * 16, (y - 0.3 + (1 - self.render_space)) * 16))
                self.game.display.blit(self.wall_side_top_left, (x * 16, (y - 0.3 - self.render_space) * 16))
            elif value == 9:  # inner top right corner
                self.game.display.blit(self.wall_right, (x * 16, y * 16))
                self.game.display.blit(self.wall_top_right, (x * 16, (y - 1) * 16))
            elif value == 10:  # inner bottom right corner
                self.game.display.blit(self.wall_inner_corner_mid_right, (x * 16, (y - 0.3 + (1 - self.render_space)) * 16))
                self.game.display.blit(self.wall_corner_top_right, (x * 16, (y - 0.3 - self.render_space) * 16))
            elif value == 11:  # outer top right corner
                self.game.display.blit(self.wall_side_mid_right, (x * 16, y * 16))
                self.game.display.blit(self.wall_side_top_right, (x * 16, (y - 1) * 16))
            elif value == 12:  # outer bottom left corner
                self.game.display.blit(self.wall_side_front_right, (x * 16, (y - 0.3 + (1 - self.render_space)) * 16))
                self.game.display.blit(self.wall_side_top_right, (x * 16, (y - 0.3 - self.render_space) * 16))

        # draw doors
        for x, y, patch in self.door:
            door_rect = self.door_tile.get_rect()
            door_rect.midbottom = (x * 16, (y + 1) * 16)
            self.game.display.blit(self.door_tile, door_rect)

        self.render_minimap()


    def get_tiles(self, tile):
        return pygame.image.load(tile)


    def rand_wall(self, x, y, tileset_len):
        """ Return random number to select different mid wall tiles from the tile tuple. """
        self.rand.sort()
        rand_num = (x + y * self.rand[0]) % self.rand[2]

        if rand_num == 0:
            num = (x + y * self.rand[1]) % (tileset_len)
            return num
        else:
            return 0

    def rand_tiles(self, tileset_len):
        """ Return random number to select different tiles from tuple other than walls. """
        prob = .98
        incre = (1 - prob) / (tileset_len - 1)
        rand_num = random.random()
        if rand_num < prob:
            return 0
        else:
            return int((rand_num - prob)//incre) + 1



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
        self.mini_size = (125, 90)
        self.mini_img = pygame.Surface(self.mini_size)
        self.mini_img.fill((53, 44, 43))
        self.mini_rect = self.mini_img.get_rect(topleft=((config.GAME_WIDTH - self.mini_size[0])/ 2, 2))

        self.room_rect = (5, 5)
        self.room_visited = dict()
        self.room_connected = dict()
        self.corridor = dict()
        self.room_size = 16
        self.move_x = 14
        self.move_y = 5
        self.corridor_size = (3, self.move_y)
        self.player_pos = tuple()
        self.last_update = 0


    def build_minimap(self):
        # If the player has accessed the current room before, do nothing
        if self.current_map in self.room_visited.keys():
            self.build_player_pos()
            pass
        else:
            self.build_miniroom()
            self.build_player_pos()

    def draw_minimap(self):
        for room in self.room_visited.values():
            self.mini_img.blit(
                pygame.transform.scale(self.get_tiles("./assets/frames/" + ROOMS_IMG[0]),
                                        (self.room_size, self.room_size)),
                                        (room[0], room[1]))
        for connect in self.room_connected.values():
            self.mini_img.blit(
                pygame.transform.scale(self.get_tiles("./assets/frames/" + ROOMS_IMG[1]),
                                       (self.room_size, self.room_size)),
                                        (connect[0], connect[1]))
        for corridor in self.corridor.values():
            if corridor[2] == 'v':
                self.mini_img.blit(pygame.transform.scale(self.get_tiles("./assets/frames/" + ROOMS_IMG[2]),
                                       (self.corridor_size[0], self.corridor_size[1])), (corridor[0], corridor[1]))
            else:
                self.mini_img.blit(pygame.transform.scale(self.get_tiles("./assets/frames/" + ROOMS_IMG[2]),
                                       (self.move_x, self.corridor_size[0])), (corridor[0], corridor[1]))

        player = pygame.transform.scale(self.get_tiles("./assets/frames/" + ROOMS_IMG[3]), (5,5))
        player_rect = player.get_rect(center=(self.player_pos[0], self.player_pos[1]))
        now = pygame.time.get_ticks()
        if now - self.last_update > 900:
            self.last_update = now
        else:
            self.mini_img.blit(player, player_rect)


    def build_miniroom(self):
        """ Build current room and connected rooms and put the topleft rect to corresponding dict. """
        curr_room = config.ROOMS[self.current_level][self.current_map - 1]
        # clear the connected dict for new connected rooms
        self.room_connected = dict()


        # build current room
        if self.current_map > 1:
            if curr_room[0] == 'U':
                self.room_rect = (self.room_rect[0], self.room_rect[1] + self.room_size + self.move_y)
            elif curr_room[0] == 'D':
                self.room_rect = (self.room_rect[0], self.room_rect[1] - self.room_size - self.move_y)
            elif curr_room[0] == 'L':
                self.room_rect = (self.room_rect[0] + self.room_size + self.move_x, self.room_rect[1])
            elif curr_room[0] == 'R':
                self.room_rect = (self.room_rect[0] - self.room_size - self.move_x, self.room_rect[1])

        elif self.current_map == 1:
            self.mini_img.blit(pygame.transform.scale(self.get_tiles("./assets/frames/" + ROOMS_IMG[0]), (self.room_size, self.room_size)), (self.room_rect[0], self.room_rect[1]))

        self.room_visited[self.current_map] = self.room_rect

        # build connected rooms (each room only has two doors)
        room = curr_room[-1]
        if curr_room[-1] == 'U':
            connect_rect = (self.room_rect[0], self.room_rect[1] - self.room_size - self.move_y)
            corridor_rect = (connect_rect[0] + (self.room_size - self.corridor_size[0]) / 2, connect_rect[1] + self.room_size, 'v')
        elif curr_room[-1] == 'D':
            connect_rect = (self.room_rect[0], self.room_rect[1] + self.room_size + self.move_y)
            corridor_rect = (connect_rect[0] + (self.room_size - self.corridor_size[0]) / 2, connect_rect[1] - self.move_y, 'v')
        elif curr_room[-1] == 'L':
            connect_rect = (self.room_rect[0] - self.room_size - self.move_x, self.room_rect[1])
            corridor_rect = (connect_rect[0] + self.room_size, connect_rect[1] + (self.room_size - self.corridor_size[1]) / 2, 'h')
        elif curr_room[-1] == 'R':
            connect_rect = (self.room_rect[0] + self.room_size + self.move_x, self.room_rect[1])
            corridor_rect = (connect_rect[0] - self.move_x, connect_rect[1] + (self.room_size - self.corridor_size[0]) / 2, 'h')

        self.room_connected[room] = connect_rect
        self.corridor[self.current_map] = corridor_rect

    def build_player_pos(self):
        # store player position
        self.player_pos = tuple()
        room_pos = self.room_visited[self.current_map]
        self.player_pos = (room_pos[0] + self.room_size / 2, room_pos[1] + self.room_size / 2)


    def render_minimap(self):
        self.draw_minimap()
        self.game.display.blit(self.mini_img, self.mini_rect)








