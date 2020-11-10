from menu import *
from player import *
from enemy import *
from projectile import *
from ui import *
from map import *
from dialogue import *
from config import *

class Game:

    def __init__(self):
        pygame.init()
        # make cursor x
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        self.running, self.playing, self.intro = True, False, False
        self.display = pygame.Surface((config.GAME_WIDTH, config.GAME_HEIGHT))
        self.window = pygame.display.set_mode((config.GAME_WIDTH, config.GAME_HEIGHT))
        self.font_name = "assets/pixel_font.ttf"
        self.START_KEY, self.ESCAPE_KEY, self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.ACTION, \
            self.MODIFY, self.SCROLL_UP, self.SCROLL_DOWN = \
            False, False, False, False, False, False, False, False, False, False
        self.mouse_pos = pygame.mouse.get_pos()
        self.player_character = "knight"
        # define class names for each sprite name
        self.player_classes = {"knight": "PALADIN", "elf": "RANGER", "wizzard": "MAGE", "lizard": "ROGUE"}
        self.player_gender = "m"
        self.curr_actors = []
        self.ui = Ui(self)
        self.curr_map = Map(self, config.GAME_WIDTH, config.GAME_HEIGHT)
        self.main_menu = MainMenu(self)
        self.options_menu = OptionsMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.character_menu = CharacterMenu(self)
        self.curr_menu = self.main_menu
        self.text_dialogue = StaticText(self, 'Stop there criminal scum!', WHITE)
        self.introduction = InGameIntro(self, None)

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
        if self.intro:
            self.introduction.display_intro()
        if self.playing:
            self.curr_actors = []
            player = Player(self, config.GAME_WIDTH / 2, config.GAME_HEIGHT / 2,
                            config.get_player_sprite(self.player_character, self.player_gender),
                            self.player_classes[self.player_character])
            self.curr_actors.append(player)
            enemy1 = Enemy(self, config.GAME_WIDTH / 4, config.GAME_HEIGHT / 2, "demon", "big_demon")
            enemy2 = Enemy(self, config.GAME_WIDTH / 4, config.GAME_HEIGHT / 4, "demon", "chort")
            enemy3 = Enemy(self, config.GAME_WIDTH / 6, config.GAME_HEIGHT / 5, "demon", "chort")
            enemy4 = Enemy(self, config.GAME_WIDTH / 5, config.GAME_HEIGHT / 6, "demon", "chort")
            self.curr_actors.append(enemy1)
            self.curr_actors.append(enemy2)
            self.curr_actors.append(enemy3)
            self.curr_actors.append(enemy4)
        while self.playing:
            self.check_events()
            if self.ESCAPE_KEY:
                self.playing = False
            self.display.fill(config.BLACK)
            self.draw_actors()
            self.control_player()
            self.control_enemies()
            self.control_projectiles()
            self.draw_map()
            # We need to be passed max health and current health from player <3 (and shields)
            # or self.ui.display(player)?
            # For testing:
            self.ui.display_ui(max_health=player.max_health, curr_health=player.health, max_shields=player.max_shield,
                               curr_shields=player.shield, money=player.money, time=pygame.time.get_ticks())
            self.window.blit(self.display, (0, 0))
            self.text_dialogue.display_text(self.curr_actors)
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
        self.curr_map.draw_map()
        # self.curr_map.render()

    def draw_actors(self):
        for actor in self.curr_actors:
            actor.render()

    def control_player(self):
        for actor in self.curr_actors:
            if isinstance(actor, Player):
                actor.get_input()

    def control_enemies(self):
        for actor in self.curr_actors:
            if isinstance(actor, Enemy):
                actor.ai()
                if actor.entity_status == "dead":
                    self.curr_actors.remove(actor)

    def control_projectiles(self):
        for actor in self.curr_actors:
            if isinstance(actor, Projectile):
                actor.move(3)
                if actor.hit:
                    self.curr_actors.remove(actor)
