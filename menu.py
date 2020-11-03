import pygame
from actor import *


class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = config.GAME_WIDTH / 2, config.GAME_HEIGHT / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        self.game.draw_text("*", 30, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        super(MainMenu, self).__init__(game)
        self.state = "Start"
        self.start_x, self.start_y = self.mid_w, self.mid_h + 30
        self.options_x, self.options_y = self.mid_w, self.mid_h + 50
        self.credits_x, self.credits_y = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(config.BLACK)
            self.game.draw_text("Main Menu", 50, self.mid_w, self.mid_h - 20)
            self.game.draw_text("Start", 50, self.start_x, self.start_y)
            self.game.draw_text("Options", 50, self.options_x, self.options_y)
            self.game.draw_text("Credits", 50, self.credits_x, self.credits_y)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY or self.game.RIGHT_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.options_x + self.offset, self.options_y)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.credits_x + self.offset, self.credits_y)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = "Start"

        elif self.game.UP_KEY or self.game.LEFT_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.credits_x + self.offset, self.credits_y)
                self.state = "Credits"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = "Start"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.options_x + self.offset, self.options_y)
                self.state = "Options"

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == "Start":
                self.game.curr_menu = self.game.character_menu
            elif self.state == "Options":
                self.game.curr_menu = self.game.options_menu
            elif self.state == "Credits":
                self.game.curr_menu = self.game.credits_menu
            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game):
        super(OptionsMenu, self).__init__(game)
        self.state = "Volume"
        self.vol_x, self.vol_y = self.mid_w, self.mid_h + 20
        self.controls_x, self.controls_y = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.vol_x + self.offset, self.vol_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(config.BLACK)
            self.game.draw_text("Options", 50, self.mid_w, self.mid_h - 20)
            self.game.draw_text("Volume", 50, self.vol_x, self.vol_y)
            self.game.draw_text("Controls", 50, self.controls_x, self.controls_y)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.ESCAPE_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY or self.game.LEFT_KEY or self.game.RIGHT_KEY:
            if self.state == "Volume":
                self.state = "Controls"
                self.cursor_rect.midtop = (self.controls_x + self.offset, self.controls_y)
            elif self.state == "Controls":
                self.state = "Volume"
                self.cursor_rect.midtop = (self.vol_x + self.offset, self.vol_y)
        elif self.game.START_KEY:
            pass


class CreditsMenu(Menu):
    def __init__(self, game):
        super(CreditsMenu, self).__init__(game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.ESCAPE_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(config.BLACK)
            self.game.draw_text("Credits", 50, config.GAME_WIDTH / 2, config.GAME_HEIGHT / 2 - 20)
            self.game.draw_text("George Welch", 20, config.GAME_WIDTH / 2, config.GAME_HEIGHT / 2 + 10)
            self.blit_screen()


class CharacterMenu(Menu):

    def __init__(self, game):
        super(CharacterMenu, self).__init__(game)
        self.character_class = 0
        self.character_gender = 0
        self.character_classes = [("Paladin", "knight"), ("Ranger", "elf"), ("Mage", "wizzard"), ("Rogue", "lizard")]
        self.character_genders = ["m", "f"]
        self.actor = Actor(self.game, self.mid_w, self.mid_h,
                           config.get_player_sprite(self.game.player_character,
                                                    self.game.player_gender))

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(config.BLACK)
            self.actor.render()
            self.game.draw_text(self.character_classes[self.character_class][0], 50, self.mid_w, self.mid_h - 50)
            self.blit_screen()

    def check_input(self):
        if self.game.ESCAPE_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            self.character_gender = (self.character_gender + 1) % 2
        elif self.game.LEFT_KEY:
            self.character_class = (self.character_class - 1) % 4
        elif self.game.RIGHT_KEY:
            self.character_class = (self.character_class + 1) % 4
        elif self.game.START_KEY:
            self.game.playing = True
            self.run_display = False
        self.game.player_character = self.character_classes[self.character_class][1]
        self.game.player_gender = self.character_genders[self.character_gender]
        self.actor = Actor(self.game, self.mid_w, self.mid_h,
                           config.get_player_sprite(self.game.player_character,
                                                    self.game.player_gender))
