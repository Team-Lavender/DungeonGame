from entities import *
import config
import npc_lookup

class NPC(Entity):

    def __init__(self, game, pos_x, pos_y, npc_type, npc_name):
        self.lookup = npc_lookup.npcs[npc_type][npc_name]
        super(NPC, self).__init__(game, pos_x, pos_y, config.get_npc_sprite(npc_name),
                                  self.lookup[0], self.lookup[1], True, self.lookup[2], "alive",
                                  self.lookup[3])
        self.flip_sprite = False
        self.npc_status = "alive"
        self.move_direction = random.randint(0, 360)
        self.vision_radius = self.lookup[6]
        self.game = game

    def ai(self):
        player = self.game.curr_actors[0]
        self.linear_path(player)


    def linear_path(self, target):
        target_vector = pygame.Vector2(target.pos_x - self.pos_x, target.pos_y - self.pos_y)
        if 0 < target_vector.length() <= self.vision_radius and not target.invisible:
            self.sees_target = True
            target_vector.scale_to_length(self.move_speed)
            self.move(target_vector)
        else:
            angle = self.move_direction
            move_vector = pygame.Vector2(1,1)
            move_vector.from_polar((self.move_speed, angle))
            self.move(move_vector)
            if not self.can_move(move_vector):
                self.update_move_direction()

    def update_move_direction(self):
        self.move_direction = random.randint(0, 360)

    def take_damage(num, nums):
        pass
