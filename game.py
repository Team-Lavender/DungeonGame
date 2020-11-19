from menu import *
from player import *
from enemy import *
from projectile import *
from consumable import *
from ui import *
from map import *
from dialogue import *
from config import *
from FOV import *
from cutscene import *
import audio
from throwable import *


class Game:

    def __init__(self):
        pygame.init()

        # make cursor x
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        self.running, self.playing, self.intro, self.cutscene_trigger = True, False, False, False
        self.display = pygame.Surface((config.GAME_WIDTH, config.GAME_HEIGHT))
        self.window = pygame.display.set_mode((config.GAME_WIDTH, config.GAME_HEIGHT), pygame.NOFRAME,
                                              pygame.OPENGLBLIT)
        pygame.event.set_grab(True)
        self.font_name = "assets/pixel_font.ttf"
        self.START_KEY, self.ESCAPE_KEY, self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.ACTION, \
        self.MODIFY, self.SCROLL_UP, self.SCROLL_DOWN, self.SPECIAL, self.INTERACT, self.CONSUMABLE_1, self.CONSUMABLE_2 = \
            False, False, False, False, False, False, False, False, False, False, False, False, False, False
        self.mouse_pos = pygame.mouse.get_pos()
        self.player_character = "knight"
        # define class names for each sprite name
        self.player_classes = {"knight": "PALADIN", "elf": "RANGER", "wizzard": "MAGE", "lizard": "ROGUE"}
        self.player_gender = "m"
        self.current_cutscene = 0
        self.curr_actors = []
        self.elemental_surfaces =[]
        self.ui = Ui(self)
        self.curr_map = Map(self, config.GAME_WIDTH, config.GAME_HEIGHT)
        self.fov = False
        self.main_menu = MainMenu(self)
        self.options_menu = OptionsMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.character_menu = CharacterMenu(self)
        self.curr_menu = self.main_menu
        self.introduction = InGameIntro(self, None)
        self.cutscenes = CutSceneManager(self)
        self.show_inventory = False
        self.show_shop = False
        # pygame.event.set_grab(True)

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
                    self.show_shop = False
                    self.show_inventory = False

                if event.key == pygame.K_w:
                    self.UP_KEY = True
                if event.key == pygame.K_s:
                    self.DOWN_KEY = True
                if event.key == pygame.K_a:
                    self.LEFT_KEY = True

                if event.key == pygame.K_1:
                    self.CONSUMABLE_1 = True
                    self.ui.consumable_1_animation = True
                    self.ui.consumable_1_timer = pygame.time.get_ticks()
                if event.key == pygame.K_2:
                    self.CONSUMABLE_2 = True
                    self.ui.consumable_2_animation = True
                    self.ui.consumable_2_timer = pygame.time.get_ticks()

                if event.key == pygame.K_i:
                    self.show_inventory = not self.show_inventory
                    self.show_shop = False
                if event.key == pygame.K_p:
                    self.show_shop = not self.show_shop
                    self.show_inventory = False

                # Toggles cutscene trigger. Only for testing. Should be removed
                if event.key == pygame.K_l:
                    self.cutscene_trigger = not self.cutscene_trigger

                if event.key == pygame.K_d:
                    self.RIGHT_KEY = True
                if event.key == pygame.K_q:
                    self.SPECIAL = True
                if event.key == pygame.K_SPACE:
                    self.INTERACT = True
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
            player = Player(self, self.curr_map.spawn[0], self.curr_map.spawn[1],
                            config.get_player_sprite(self.player_character, self.player_gender),
                            self.player_classes[self.player_character])
            self.curr_actors.append(player)
            self.spawn_enemies()
            new_fov = FOV(self, 210)

        while self.playing:
            self.check_events()
            if self.ESCAPE_KEY:
                self.playing = False
            self.display.fill(config.BLACK)
            self.draw_map()
            self.draw_actors()
            if self.MODIFY:
                self.fov = not self.fov

            if self.fov:
                new_fov.draw_fov()

            self.control_player()
            self.control_enemies()
            self.control_projectiles()
            self.control_throwables()
            self.draw_potion_fx()
            self.render_elemental_surfaces()

            # We need to be passed max health and current health from player <3 (and shields)
            # or self.ui.display(player)?
            # For testing:
            if self.show_inventory:
                self.ui.toggle_inventory()
            if self.show_shop:
                self.ui.toggle_shop()
            self.ui.display_ui(time=pygame.time.get_ticks(), player=self.curr_actors[0])
            self.window.blit(self.display, (0, 0))
            # Check current player pos for cutscene triggers
            self.get_cutscene()
            self.cutscenes.update(self.current_cutscene)


            pygame.display.update()

            self.reset_keys()
            pygame.time.Clock().tick(60)

    def reset_keys(self):
        self.START_KEY, self.ESCAPE_KEY, self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.ACTION, \
        self.MODIFY, self.SCROLL_UP, self.SCROLL_DOWN, self.SPECIAL, self.INTERACT, self.CONSUMABLE_1, self.CONSUMABLE_2 = \
            False, False, False, False, False, False, False, False, False, False, False, False, False, False

    def draw_text(self, text, size, x, y, color=config.WHITE):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
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
                actor.print_damage_numbers(config.PINK)
                # slowly increment special charge
                actor.special_charge = min(100, actor.special_charge + 0.05)
                break

    def control_enemies(self):
        for actor in self.curr_actors:
            if isinstance(actor, Enemy):
                actor.render_health()
                actor.print_damage_numbers(config.GOLD)
                # When a cutscene is playing do not use enemy AI
                if not self.cutscene_trigger:
                    actor.ai()
                if actor.entity_status == "dead":
                    self.curr_actors.remove(actor)

    def control_projectiles(self):
        for actor in self.curr_actors:
            if isinstance(actor, Projectile):
                actor.move(3)
                if actor.hit:
                    self.curr_actors.remove(actor)

    def draw_potion_fx(self):
        if len(self.curr_actors[0].potion_1) > 0:
            potion_1 = self.curr_actors[0].potion_1[-1]
            # remove potion if consumed
            if potion_1.consumed:
                self.curr_actors[0].potion_1.pop()
            if not potion_1.is_throwable:
                if potion_1.render_fx_on:
                    potion_1.render_fx()
        if len(self.curr_actors[0].potion_2) > 0:
            potion_2 = self.curr_actors[0].potion_2[-1]
            # remove potion if consumed
            if potion_2.consumed:
                self.curr_actors[0].potion_2.pop()
            if not potion_2.is_throwable:
                if potion_2.render_fx_on:
                    potion_2.render_fx()

    def control_throwables(self):
        if len(self.curr_actors[0].potion_1) > 0:
            potion_1 = self.curr_actors[0].potion_1[-1]
            if potion_1.is_throwable:
                if potion_1.targeting:
                    potion_1.render_targeting()
                if potion_1.thrown:
                    potion_1.move()
                    potion_1.render()


        if len(self.curr_actors[0].potion_2) > 0:
            potion_2 = self.curr_actors[0].potion_2[-1]
            if potion_2.is_throwable:
                if potion_2.targeting:
                    potion_2.render_targeting()
                if potion_2.thrown:
                    potion_2.move()
                    potion_2.render()

    def render_elemental_surfaces(self):
        for element_surface in self.elemental_surfaces:
            element_surface.render()

    def spawn_enemies(self):
        for enemy in self.curr_map.enemies:
            if enemy[2] == 'E':
                character = Enemy(self, enemy[0], enemy[1], "demon", "big_demon")
            else:
                character = Enemy(self, enemy[0], enemy[1], "demon", "chort")
            self.curr_actors.append(character)

    def change_map(self, map_no):
        previous_map = self.curr_map.current_map
        self.curr_map.generate_map("map" + str(map_no))
        player = self.curr_actors[0]

        def is_player_or_weapon(actor):
            if isinstance(actor, Player) or isinstance(actor, Weapon):
                return True
            else:
                return False

        self.curr_actors = list(filter(is_player_or_weapon, self.curr_actors))
        spawn = self.curr_map.spawn
        for a_door in self.curr_map.door:
            if a_door[2] == str(previous_map):
                if (a_door[0], a_door[1] - 1) in self.curr_map.floor:
                    up_or_down = -1
                else:
                    up_or_down = 2

                spawn = (a_door[0] * 16, (a_door[1] + up_or_down) * 16)

        player.pos_x = spawn[0]
        player.pos_y = spawn[1]
        self.spawn_enemies()

    def get_cutscene(self):
        player_pos = ((math.floor(self.curr_actors[0].pos_x // 16)), math.floor(self.curr_actors[0].pos_y // 16))
        completed = self.cutscenes.completed_cutscenes
        if player_pos in self.curr_map.cutscene_1:
            if 1 not in completed:
                self.current_cutscene = 1
                self.cutscene_trigger = True
        elif player_pos in self.curr_map.cutscene_2:
            if 2 not in completed:
                self.current_cutscene = 2
                self.cutscene_trigger = True
