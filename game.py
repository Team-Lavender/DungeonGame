from menu import *

from player import *
from ui import *

from map import *

class Game:

    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.display = pygame.Surface((config.GAME_WIDTH, config.GAME_HEIGHT))
        self.window = pygame.display.set_mode((config.GAME_WIDTH, config.GAME_HEIGHT))
        self.font_name = "assets/pixel_font.ttf"
        self.START_KEY, self.ESCAPE_KEY, self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.ACTION,\
            self.MODIFY, self.SCROLL_UP, self.SCROLL_DOWN = \
            False, False, False, False, False, False, False, False, False, False
        self.mouse_pos = pygame.mouse.get_pos()
        self.player_character = "knight"
        self.player_gender = "m"
        self.curr_actors = []
        self.ui = Ui(self)
        self.curr_map = Map(self, config.GAME_WIDTH, config.GAME_HEIGHT)
        self.main_menu = MainMenu(self)
        self.options_menu = OptionsMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.character_menu = CharacterMenu(self)
        self.curr_menu = self.main_menu

    def check_events(self):
        self.mouse_pos = pygame.mouse.get_pos()
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    self.ACTION = True
                if event.button == pygame.BUTTON_RIGHT:
                    self.MODIFY = True
                if event.button == pygame.BUTTON_WHEELUP:
                    self.SCROLL_UP = True
                if event.button == pygame.BUTTON_WHEELDOWN:
                    self.SCROLL_DOWN = True

    def game_loop(self):
        # render tests
        if self.playing:
            self.curr_actors = []
            player = Player(self, config.GAME_WIDTH / 2, config.GAME_HEIGHT / 2,
                            config.get_player_sprite(self.player_character, self.player_gender), 10, 0, False, 1,
                            "Alive", 1, 0)
            self.curr_actors.append(player)
        while self.playing:
            self.check_events()
            if self.ESCAPE_KEY:
                self.playing = False
            self.display.fill(config.BLACK)
            self.draw_actors()
            self.control_player()
            self.draw_map()
            # We need to be passed max health and current health from player <3
            self.ui.display_ui(self.playing, player.health)
            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.reset_keys()
            pygame.time.Clock().tick(60)

    def reset_keys(self):
        self.START_KEY, self.ESCAPE_KEY, self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.ACTION, \
            self.MODIFY, self.SCROLL_UP, self.SCROLL_DOWN = \
            False, False, False, False, False, False, False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, config.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def draw_map(self):
        self.curr_map.generate_map("mapframe.txt")
        # self.curr_map.render()

    def draw_actors(self):
        for actor in self.curr_actors:
            actor.render()

    def control_player(self):
        for actor in self.curr_actors:
            if isinstance(actor, Player):
                actor.get_input()
