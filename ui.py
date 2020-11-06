from player import *

# current_health // 20 -> 100 = 5 90 = 4 80 = 4 95 = 4 70 = 3
# current_health %20 -> 100 = 0 90 = 10 80 = 0 95 = 15 70 = 10
#  max_health // 20 -> 120 = 6 - (3 + 1) = 2

'''
TODO
Refactor image loading
Refactor blit function to be used in shields and hearts?
Fix confusing names Hearts/Health?
Healing animation?
x and y spacing constants?
Enemy health bars
'''


class Ui:
    def __init__(self, game):
        self.game = game
        # Player reference
        # self.player = game.curr_actors[0]
        # self.max_health = 0
        # self.health = 0
        self.score = 100
        self.score_x, self.score_y = (config.GAME_WIDTH - 90, 0)

        # Load graphics outside class?
        self.full_heart = pygame.image.load('./assets/frames/ui_heart_full.png').convert_alpha()
        self.full_heart = pygame.transform.scale2x(self.full_heart)
        self.half_heart = pygame.image.load('./assets/frames/ui_heart_half.png').convert_alpha()
        self.half_heart = pygame.transform.scale2x(self.half_heart)
        self.empty_heart = pygame.image.load('./assets/frames/ui_heart_empty.png').convert_alpha()
        self.empty_heart = pygame.transform.scale2x(self.empty_heart)

        self.heart_dict = {0: self.empty_heart,
                           0.5: self.half_heart,
                           1: self.full_heart}

        # PLACEHOLDER SHIELD IMAGE
        self.full_shield = pygame.image.load('./assets/frames/ui_shield_full.png').convert_alpha()
        self.full_shield = pygame.transform.scale2x(self.full_shield)
        self.half_shield = pygame.image.load('./assets/frames/ui_shield_half.png').convert_alpha()
        self.half_shield = pygame.transform.scale2x(self.half_shield)
        self.empty_shield = pygame.image.load('./assets/frames/ui_shield_empty.png').convert_alpha()
        self.empty_shield = pygame.transform.scale2x(self.empty_shield)

        self.shield_dict = {0: self.empty_shield,
                            0.5: self.half_shield,
                            1: self.full_shield}

    # Is this what future display_ui class should look like?
    '''
    def display_ui(self, player):
        text_surface, text_rect = self.render_text(str(player.score).zfill(6), 50, self.score_x, self.score_y)
        self.render_hearts(player.max_hearts, player.curr_hearts)
        self.render_shields(player.max_shields, player.curr_shields)
        self.render_gold(player.curr_gold)
        self.blit_screen(text_surface)    
    '''

    # For testing
    def display_ui(self, max_health, curr_health, max_shields, curr_shields):
        self.render_text(str(self.score).zfill(6), 50, self.score_x, self.score_y)
        self.render_hearts(max_health, curr_health)
        self.render_shields(max_shields, curr_shields)

    def render_text(self, text, size, x, y):
        font = pygame.font.Font(self.game.font_name, size)
        text_surface = font.render(text, True, config.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.game.display.blit(text_surface, (self.score_x, self.score_y))

    '''
    @staticmethod
    def calculate_half_list(maxi, curr):
        half_list = []

        no_total = maxi // 2
        no_full = curr // 2
        if 1 <= curr % 2:
            no_half = 1
        else:
            no_half = 0
        no_empty = no_total - (no_full + no_half)
        for i in range(no_full):
            half_list.append(1)
        for i in range(no_half):
            half_list.append(0.5)
        for i in range(no_empty):
            half_list.append(0)
        return half_list
    '''

    # Only works if damage is integer
    @staticmethod
    def calculate_half_list(maxi, curr):
        no_total = maxi // 2
        no_full = curr // 2
        no_half = curr % 2
        if no_full < 0:
            no_full = 0
        no_empty = no_total - (no_full + no_half)

        # [1,1,0.5,0] = [Full, Full, Half, Empty]
        half_list = [1] * no_full + [0.5] * no_half + [0] * no_empty

        return half_list

    def render_hearts(self, max_health, curr_health):
        x_coord = 10
        hearts = self.calculate_half_list(max_health, curr_health)
        for heart in hearts:
            self.game.display.blit(self.heart_dict[heart], (x_coord, 10))
            x_coord += 30

    def render_shields(self, max_shields, curr_shields):
        x_coord = 8
        shields = self.calculate_half_list(max_shields, curr_shields)
        for shield in shields:
            self.game.display.blit(self.shield_dict[shield], (x_coord, 40))
            x_coord += 30