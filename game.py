
from menu import *
from actor import *


class Game:

    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.display = pygame.Surface((config.GAME_WIDTH, config.GAME_HEIGHT))
        self.window = pygame.display.set_mode((config.GAME_WIDTH, config.GAME_HEIGHT))
        self.font_name = "assets/pixel_font.ttf"
        self.START_KEY, self.ESCAPE_KEY, self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY =\
            False, False, False, False, False, False
        self.player_character = "knight"
        self.player_gender = "m"
        self.curr_actors = []
        self.curr_map = None
        self.main_menu = MainMenu(self)
        self.options_menu = OptionsMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.character_menu = CharacterMenu(self)
        self.curr_menu = self.main_menu



    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.ESCAPE_KEY = True
                if event.key == pygame.K_w:
                    self.UP_KEY = True
                if event.key == pygame.K_s:
                    self.DOWN_KEY = True
                if event.key == pygame.K_a:
                    self.LEFT_KEY = True
                if event.key == pygame.K_d:
                    self.RIGHT_KEY = True

    def game_loop(self):
        # render tests
        if self.playing:
            self.curr_actors = []
            Actor(self, config.GAME_WIDTH / 2, config.GAME_HEIGHT / 2,
                  config.get_player_sprite(self.player_character, self.player_gender))
        while self.playing:
            self.check_events()
            if self.ESCAPE_KEY:
                self.playing = False
            self.display.fill(config.BLACK)
            self.draw_actors()
            self.draw_map()
            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.reset_keys()
            pygame.time.Clock().tick(60)

    def reset_keys(self):
        self.START_KEY, self.ESCAPE_KEY, self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY =\
            False, False, False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, config.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def draw_map(self):
        pass
        # self.curr_map.render()

    def draw_actors(self):
        for actor in self.curr_actors:
            actor.render()
