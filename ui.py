from player import *

# current_health // 20 -> 100 = 5 90 = 4 80 = 4 95 = 4 70 = 3
# current_health %20 -> 100 = 0 90 = 10 80 = 0 95 = 15 70 = 10
#  max_health // 20 -> 120 = 6 - (3 + 1) = 2


class Ui:
    def __init__(self, game):
        self.game = game
        # Player reference
        # self.player = game.curr_actors[0]
        self.max_health = 0
        self.health = 0
        self.score = 100
        self.score_x, self.score_y = (config.GAME_WIDTH - 90, 0)
        self.full_heart = pygame.image.load('./assets/frames/ui_heart_full.png').convert_alpha()
        self.full_heart = pygame.transform.scale2x(self.full_heart)
        self.half_heart = pygame.image.load('./assets/frames/ui_heart_half.png').convert_alpha()
        self.half_heart = pygame.transform.scale2x(self.half_heart)
        self.empty_heart = pygame.image.load('./assets/frames/ui_heart_empty.png').convert_alpha()
        self.empty_heart = pygame.transform.scale2x(self.empty_heart)

    def update(self, player_health):
        if self.max_health == 0:
            self.max_health = player_health
            self.health = player_health
        else:
            self.health = player_health

    def display_ui(self, playing, health):
        if playing:
            self.update(health)
            text_surface, text_rect = self.render_text(str(self.score).zfill(6), 50, self.score_x, self.score_y)
            hearts = self.calculate_hearts()
            self.render_hearts(hearts)
            self.blit_screen(text_surface)

    def render_text(self, text, size, x, y):
        font = pygame.font.Font(self.game.font_name, size)
        text_surface = font.render(text, True, config.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        return text_surface, text_rect

    def blit_screen(self, text_surface):
        self.game.display.blit(text_surface, (self.score_x, self.score_y))

    def calculate_hearts(self):
        heart_list = []

        no_total_hearts = self.max_health // 2
        no_full_hearts = self.health // 2
        if 1 <= self.health % 2:
            no_half_hearts = 1
        else:
            no_half_hearts = 0
        no_empty_hearts = no_total_hearts - (no_full_hearts + no_half_hearts)
        for i in range(no_full_hearts):
            heart_list.append(self.full_heart)
        for i in range(no_half_hearts):
            heart_list.append(self.half_heart)
        for i in range(no_empty_hearts):
            heart_list.append(self.empty_heart)
        return heart_list

    def render_hearts(self, hearts):
        x_coord = 10
        for heart in hearts:
            self.game.display.blit(heart, (x_coord, 10))
            x_coord += 30