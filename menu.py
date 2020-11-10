
from actor import *
from config import *
from character_classes import *

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
        self.character_classes = [("PALADIN", "knight"), ("RANGER", "elf"), ("MAGE", "wizzard"), ("ROGUE", "lizard")]
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
            self.game.draw_text("str", 40,  self.mid_w - 125, self.mid_h + 50)
            self.game.draw_text(str(character_stats[self.character_classes[self.character_class][0]]["str"]), 40,
                                self.mid_w - 125, self.mid_h + 80)
            self.game.draw_text("dex", 40, self.mid_w - 75, self.mid_h + 50)
            self.game.draw_text(str(character_stats[self.character_classes[self.character_class][0]]["dex"]), 40,
                                self.mid_w - 75, self.mid_h + 80)
            self.game.draw_text("con", 40, self.mid_w - 25, self.mid_h + 50)
            self.game.draw_text(str(character_stats[self.character_classes[self.character_class][0]]["con"]), 40,
                                self.mid_w - 25, self.mid_h + 80)
            self.game.draw_text("int", 40, self.mid_w + 25, self.mid_h + 50)
            self.game.draw_text(str(character_stats[self.character_classes[self.character_class][0]]["int"]), 40,
                                self.mid_w + 25, self.mid_h + 80)
            self.game.draw_text("wis", 40, self.mid_w + 75, self.mid_h + 50)
            self.game.draw_text(str(character_stats[self.character_classes[self.character_class][0]]["wis"]), 40,
                                self.mid_w + 75, self.mid_h + 80)
            self.game.draw_text("cha", 40, self.mid_w + 125, self.mid_h + 50)
            self.game.draw_text(str(character_stats[self.character_classes[self.character_class][0]]["cha"]), 40,
                                self.mid_w + 125, self.mid_h + 80)
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
            self.game.intro = True
        self.game.player_character = self.character_classes[self.character_class][1]
        self.game.player_gender = self.character_genders[self.character_gender]
        self.actor = Actor(self.game, self.mid_w, self.mid_h,
                           config.get_player_sprite(self.game.player_character,
                                                    self.game.player_gender))



class InGameIntro(Menu):

    def __init__(self, game, text):
        super(InGameIntro, self).__init__(game)
        self.text = text
        self.default_text = ''
        self.IN_GAME_INTRO = '''
        MANY YEARS AGO PRINCE DARKNESS "GANNON" STOLE ONE OF THE TRIFORCE WITH POWER. 
        PRINCESS ZELDA HAD ONE OF THE TRIFORCE WITH WISDOM. 
        SHE DIVIDED IT INTO 8 UNITS TO HIDE IT FROM "GANNON" BEFORE SHE WAS CAPTURED. 
        GO FIND THE "8" UNITS "LINK" TO SAVE HER.
        '''

    def display_intro(self):

        self.screen = self.game.window
        starting_pos = 300

        while self.game.intro:
            self.screen.fill(0)
            starting_pos -= 0.1
            msg_list = []
            pos_list = []
            i = 0
            font = pygame.font.Font(self.game.font_name, 15)

            # If 'START_KEY' exit intro and enter game
            self.game.check_events()
            if self.game.START_KEY:
                self.game.intro = False

            # Scrolling logic
            for line in self.IN_GAME_INTRO.split('\n'):
                msg = font.render(line, True, WHITE)
                msg_list.append(msg)
                pos = msg.get_rect(center=(self.game.window.get_rect().centerx, self.game.window.get_rect().centery + starting_pos + i * 30))
                pos_list.append(pos)

                i += 1
            for j in range(i):
                self.screen.blit(msg_list[j], pos_list[j])

            pygame.display.update()