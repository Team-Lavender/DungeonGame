class Map:
    def __init__(self, map_height, map_width, map_type="square", number_of_rooms=1):
        self.map_height = map_height
        self.map_width = map_width
        self.map_type = map_type
        self.rooms = number_of_rooms
        self.floor_map = {}

        if map_type == "cave":
            self.generate_cave_map()
        elif map_type == "tunnel":
            self.generate_tunnel_map()
        else:
            self.generate_square_map()

    def generate_tunnel_map(self):
        return

    def generate_cave_map(self):
        return

    def generate_square_map(self):
        self.floor_map["wall"] = set()
        self.floor_map["floor"] = set()
        for x in range(0, self.map_width):
            for y in range(0, self.map_height):
                if x == 0 or x == self.map_width or y == 0 or y == self.map_height:
                    self.floor_map["wall"] = self.floor_map["wall"].add((x, y))
                else:
                    self.floor_map["floor"] = self.floor_map["floor"].add((x, y))
