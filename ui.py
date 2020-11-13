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
        self.time = pygame.time
        self.game = game
        # Player reference
        # self.max_health = 0
        # self.health = 0
        self.score_x, self.score_y = (config.GAME_WIDTH - 90, 0)
        self.money_x, self.money_y = (config.GAME_WIDTH - 90, 25)
        self.hotbar_x, self.hotbar_y = (config.GAME_WIDTH / 2, config.GAME_HEIGHT - 44)
        self.initial_tile_x = self.hotbar_x - 97
        self.final_tile_x = self.hotbar_x + 97
        self.coin_index = 0
        self.coin_full_rotation = 750
        self.coin_scale = 24
        self.hotbar_bg_colour = (177, 198, 202)
        self.hotbar_main_colour = (53, 44, 43)

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

        self.coin_0 = pygame.image.load('./assets/frames/coin_anim_f0.png')
        self.coin_0 = pygame.transform.scale(self.coin_0, (self.coin_scale, self.coin_scale))
        self.coin_1 = pygame.image.load('./assets/frames/coin_anim_f1.png')
        self.coin_1 = pygame.transform.scale(self.coin_1, (self.coin_scale, self.coin_scale))
        self.coin_2 = pygame.image.load('./assets/frames/coin_anim_f2.png')
        self.coin_2 = pygame.transform.scale(self.coin_2, (self.coin_scale, self.coin_scale))
        self.coin_3 = pygame.image.load('./assets/frames/coin_anim_f3.png')
        self.coin_3 = pygame.transform.scale(self.coin_3, (self.coin_scale, self.coin_scale))

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
    def display_ui(self, max_health, curr_health, max_shields, curr_shields, money, time,
                   score, player):
        self.render_text(str(score).zfill(6), 50, self.score_x, self.score_y)
        self.render_money(str(money).zfill(6), 50, self.money_x, self.money_y)
        self.render_hearts(max_health, curr_health)
        self.render_shields(max_shields, curr_shields)
        self.coin_animation(time)
        self.draw_hotbar(player)
        # self.time.set_timer(self.update_coin, 1000)

    def draw_hotbar(self, player):
        hotbar_bg = pygame.Rect(0, 0, 250, 50)
        hotbar_bg.center = (self.hotbar_x, self.hotbar_y)
        hotbar_border = pygame.Rect(0, 0, 244, 44)
        hotbar_border.center = (self.hotbar_x, self.hotbar_y)
        tile_offset = 0
        hotbar_item_1 = player.items[0].sprite["idle"][0]
        hotbar_item_1_rect = hotbar_item_1.get_rect()
        hotbar_item_1_rect.center = (self.hotbar_x - 97, self.hotbar_y)
        pygame.draw.rect(self.game.display, self.hotbar_bg_colour, hotbar_bg)
        pygame.draw.rect(self.game.display, (0, 0, 0), hotbar_border)
        for _ in range(3):
            hotbar_tile = pygame.Rect(0, 0, 46, 40)
            hotbar_tile.center = (self.initial_tile_x + tile_offset, self.hotbar_y)
            pygame.draw.rect(self.game.display, self.hotbar_main_colour, hotbar_tile)
            tile_offset += 48

        tile_offset = 0

        for _ in range(2):
            hotbar_tile = pygame.Rect(0, 0, 46, 40)
            hotbar_tile.center = (self.final_tile_x - tile_offset, self.hotbar_y)
            pygame.draw.rect(self.game.display, self.hotbar_main_colour, hotbar_tile)
            tile_offset += 48
        tile_number = 0
        self.highlight_tile(tile_number)
        self.game.display.blit(hotbar_item_1, hotbar_item_1_rect)

    def highlight_tile(self, tile):
        hotbar_tile = pygame.Surface((46, 40))
        hotbar_tile.set_alpha(80)
        hotbar_tile.fill((252, 207, 3))
        self.game.display.blit(hotbar_tile, (self.initial_tile_x + 48 * tile - 23, self.hotbar_y - 20))

    def coin_animation(self, time):
        if time % self.coin_full_rotation < self.coin_full_rotation / 4:
            self.blit_coin(self.coin_0, self.money_x, self.money_y)
        if self.coin_full_rotation / 4 <= time % self.coin_full_rotation < self.coin_full_rotation / 2:
            self.blit_coin(self.coin_1, self.money_x, self.money_y)
        if self.coin_full_rotation / 2 <= time % self.coin_full_rotation < self.coin_full_rotation * 3 / 4:
            self.blit_coin(self.coin_2, self.money_x, self.money_y)
        if time % self.coin_full_rotation > self.coin_full_rotation * 3 / 4:
            self.blit_coin(self.coin_3, self.money_x, self.money_y)

    def blit_coin(self, coin, x, y):
        self.game.display.blit(coin, (x - 30, y + 12))

    def render_money(self, text, size, x, y):
        font = pygame.font.Font(self.game.font_name, size)
        text_surface = font.render(text, True, config.GOLD)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.game.display.blit(text_surface, (self.money_x, self.money_y))

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
        no_total = (maxi // 2) + (maxi % 2)
        no_full = curr // 2
        no_half = curr % 2
        if no_full < 0:
            no_full = 0
        if no_half == 1 and curr <= 0:
            no_half = 0
        no_empty = no_total - (no_full + no_half)
        # E.g.: [1,1,0.5,0] = [Full, Full, Half, Empty]
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
