from actor import *
from config import *
from character_classes import *
import save_and_load
import audio

class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = config.GAME_WIDTH / 2, config.GAME_HEIGHT / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100
        self.previous_menu = ""

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
        self.options_x, self.options_y = self.mid_w, self.mid_h + 60
        self.credits_x, self.credits_y = self.mid_w, self.mid_h + 90
        self.quit_x, self.quit_y = self.mid_w, self.mid_h + 120
        self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
        self.primary_font = config.WHITE
        self.secondary_font = config.GOLD
        self.start_font_color = self.secondary_font
        self.credits_font_color = self.primary_font
        self.options_font_color = self.primary_font
        self.quit_font_color = self.primary_font

    def display_menu(self):
        self.game.previous_menu = ""
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(config.BLACK)
            self.game.draw_text("Main Menu", 50, self.mid_w, self.mid_h - 20, self.primary_font)
            self.game.draw_text("Start", 50, self.start_x, self.start_y, self.start_font_color)
            self.game.draw_text("Options", 50, self.options_x, self.options_y, self.options_font_color)
            self.game.draw_text("Credits", 50, self.credits_x, self.credits_y, self.credits_font_color)
            self.game.draw_text("Quit Game", 50, self.quit_x, self.quit_y, self.quit_font_color)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY or self.game.RIGHT_KEY:
            audio.menu_move()
            if self.state == "Start":
                self.cursor_rect.midtop = (self.options_x + self.offset, self.options_y)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.credits_x + self.offset, self.credits_y)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.quit_x + self.offset, self.quit_y)
                self.state = "QUIT"
            elif self.state == "QUIT":
                self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = "Start"


        elif self.game.UP_KEY or self.game.LEFT_KEY:
            audio.menu_move()
            if self.state == "Start":
                self.cursor_rect.midtop = (self.quit_x + self.offset, self.quit_y)
                self.state = "QUIT"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = "Start"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.options_x + self.offset, self.options_y)
                self.state = "Options"
            elif self.state == "QUIT":
                self.cursor_rect.midtop = (self.credits_x + self.offset, self.credits_y)
                self.state = "Credits"

        if self.state == "Start":
            self.start_font_color = self.secondary_font
            self.credits_font_color = self.primary_font
            self.options_font_color = self.primary_font
            self.quit_font_color = self.primary_font
        elif self.state == "Options":
            self.start_font_color = self.primary_font
            self.credits_font_color = self.primary_font
            self.options_font_color = self.secondary_font
            self.quit_font_color = self.primary_font
        elif self.state == "Credits":
            self.start_font_color = self.primary_font
            self.credits_font_color = self.secondary_font
            self.options_font_color = self.primary_font
            self.quit_font_color = self.primary_font
        elif self.state == "QUIT":
            self.start_font_color = self.primary_font
            self.credits_font_color = self.primary_font
            self.options_font_color = self.primary_font
            self.quit_font_color = self.secondary_font

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            audio.menu_select()
            if self.state == "Start":
                self.game.curr_menu = self.game.start_menu
            elif self.state == "Options":
                self.game.curr_menu = self.game.options_menu
            elif self.state == "Credits":
                self.game.curr_menu = self.game.credits_menu
            elif self.state == "QUIT":
                self.game.running, self.game.playing = False, False
            self.run_display = False


class StartMenu(Menu):
    def __init__(self, game):
        super(StartMenu, self).__init__(game)
        self.state = "New Game"
        self.new_x, self.new_y = self.mid_w, self.mid_h + 20
        self.load_x, self.load_y = self.mid_w, self.mid_h + 50
        self.cursor_rect.midtop = (self.new_x + self.offset, self.new_y)
        self.primary_font = config.WHITE
        self.secondary_font = config.GOLD
        self.load_font_color = self.primary_font
        self.new_font_color = self.secondary_font

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(config.BLACK)
            self.game.draw_text("New Game", 50, self.new_x, self.new_y, self.new_font_color)
            if len(self.game.saves) > 0:
                self.game.draw_text("Load Game", 50, self.load_x, self.load_y, self.load_font_color)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.ESCAPE_KEY:
            audio.menu_back()
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif (self.game.UP_KEY or self.game.DOWN_KEY or self.game.LEFT_KEY or self.game.RIGHT_KEY) and len(
                self.game.saves) > 0:
            audio.menu_move()
            if self.state == "New Game":
                self.state = "Load Game"
                self.load_font_color = self.secondary_font
                self.new_font_color = self.primary_font
                self.cursor_rect.midtop = (self.load_x + self.offset, self.load_y)
            elif self.state == "Load Game":
                self.state = "New Game"
                self.load_font_color = self.primary_font
                self.new_font_color = self.secondary_font
                self.cursor_rect.midtop = (self.new_x + self.offset, self.new_y)
        elif self.game.START_KEY:
            audio.menu_select()
            if self.state == "New Game":
                self.game.curr_menu = self.game.character_menu
            elif self.state == "Load Game":
                self.game.curr_menu = self.game.load_game_menu
            self.run_display = False


class NewGameMenu(Menu):
    def __init__(self, game):
        super(NewGameMenu, self).__init__(game)
        self.new_x, self.new_y = self.mid_w, self.mid_h + 20
        self.save_name = ""
        self.cursor_rect.midtop = (self.new_x + self.offset, self.new_y)

    def display_menu(self):
        secondary_font = config.GOLD
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(config.BLACK)
            self.game.draw_text("Enter Save Name:", 50, self.new_x, self.new_y - 30)
            self.game.draw_text(self.save_name, 60, self.new_x, self.new_y, secondary_font)
            self.game.draw_text("Press ENTER to Begin Your Adventure", 50, self.new_x, self.new_y + 60)
            self.blit_screen()
            pygame.time.wait(110)

    def check_input(self):

        if self.game.ESCAPE_KEY:
            audio.menu_back()
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

        elif self.game.START_KEY and self.save_name != "":
            self.game.saves.append(self.save_name)
            self.game.selected_save = len(self.game.saves) - 1
            self.game.new_game()
            self.game.intro = True
            self.run_display = False

        else:
            press = pygame.key.get_pressed()
            # remove last character from name if backspace is pressed
            if press[pygame.K_BACKSPACE] and len(self.save_name) > 0:
                self.save_name = self.save_name[:-1]

            for i in range(pygame.K_a, pygame.K_z + 1):
                if press[i]:
                    audio.menu_type()
                    self.save_name += pygame.key.name(i)


class LoadGameMenu(Menu):
    def __init__(self, game):
        super(LoadGameMenu, self).__init__(game)
        self.load_x, self.load_y = self.mid_w, self.mid_h + 10
        self.save_name = ""
        self.selected = self.game.selected_save

        if len(self.game.saves) > 0:
            self.save_name = self.game.saves[self.selected]

        self.save = save_and_load.GameSave()
        self.time_and_score = self.save.get_time_and_score(self.save_name)



    def display_menu(self):
        secondary_font = config.GOLD
        self.run_display = True
        while self.run_display:
            self.save_name = self.game.saves[self.selected]
            self.time_and_score = self.save.get_time_and_score(self.save_name)
            self.game.check_events()
            self.check_input()
            self.game.display.fill(config.BLACK)
            self.game.draw_text("Use W or S to Select Save to Load:", 50, self.load_x, self.load_y - 60)

            self.game.draw_text(self.save_name, 50, self.load_x, self.load_y, secondary_font)
            self.game.draw_text("Score: " + self.time_and_score[1], 50, self.load_x, self.load_y + 40, secondary_font)
            self.game.draw_text("Last Saved: " + self.time_and_score[0], 50, self.load_x, self.load_y + 65, secondary_font)
            self.game.draw_text("Press ENTER to Begin", 50, self.load_x, self.load_y + 100)


            self.blit_screen()

    def check_input(self):
        if self.game.ESCAPE_KEY:
            audio.menu_back()
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            audio.menu_move()
            if self.game.UP_KEY:
                self.selected = (self.selected + 1) % len(self.game.saves)
            else:
                self.selected = (self.selected - 1) % len(self.game.saves)

            self.save_name = self.game.saves[self.selected]
            self.time_and_score = self.save.get_time_and_score(self.save_name)

        elif self.game.START_KEY:
            audio.menu_select()
            self.game.selected_save = self.selected
            self.game.save_state.save_name = self.game.saves[self.game.selected_save]
            self.game.playing = True
            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game):
        super(OptionsMenu, self).__init__(game)
        self.state = "Volume"
        self.vol_x, self.vol_y = self.mid_w, self.mid_h + 20
        self.controls_x, self.controls_y = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.vol_x + self.offset, self.vol_y)
        self.primary_font = config.WHITE
        self.secondary_font = config.GOLD
        self.vol_font_color = self.secondary_font
        self.con_font_color = self.primary_font

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(config.BLACK)
            self.game.draw_text("Options", 50, self.mid_w, self.mid_h - 20, self.primary_font)
            self.game.draw_text("Volume", 50, self.vol_x, self.vol_y, self.vol_font_color)
            self.game.draw_text("Controls", 50, self.controls_x, self.controls_y, self.con_font_color)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.ESCAPE_KEY:
            audio.menu_back()
            if self.game.previous_menu == "PauseMenu":
                self.game.curr_menu = self.game.pause_menu
                self.run_display = False
            else:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False

        elif self.game.UP_KEY or self.game.DOWN_KEY or self.game.LEFT_KEY or self.game.RIGHT_KEY:
            audio.menu_move()
            if self.state == "Volume":
                self.state = "Controls"
                self.vol_font_color = self.primary_font
                self.con_font_color = self.secondary_font
                self.cursor_rect.midtop = (self.controls_x + self.offset, self.controls_y)
            elif self.state == "Controls":
                self.state = "Volume"
                self.vol_font_color = self.secondary_font
                self.con_font_color = self.primary_font
                self.cursor_rect.midtop = (self.vol_x + self.offset, self.vol_y)
        elif self.game.START_KEY:
            audio.menu_select()
            if self.state == "Volume":
                self.game.curr_menu = self.game.volume_menu
            elif self.state == "Controls":
                pass
            self.run_display = False


class VolumeMenu(Menu):
    def __init__(self, game):
        super(VolumeMenu, self).__init__(game)
        self.temp_volume = self.game.music_volume


    def display_menu(self):
        secondary_font = config.GOLD
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(config.BLACK)
            self.game.draw_text("Music volume", 50, config.GAME_WIDTH / 2, config.GAME_HEIGHT / 2 - 20)
            self.game.draw_text(str(self.game.music_volume), 60, config.GAME_WIDTH / 2, config.GAME_HEIGHT / 2 + 30, secondary_font)
            self.game.draw_text("< A", 40, config.GAME_WIDTH / 2 - 60, config.GAME_HEIGHT / 2 + 30)
            self.game.draw_text("D >", 40, config.GAME_WIDTH / 2 + 60, config.GAME_HEIGHT / 2 + 30)
            self.blit_screen()

    def check_input(self):
        self.game.change_music()
        if self.game.ESCAPE_KEY:
            audio.menu_back()
            # reset game volume to previous
            self.game.music_volume = self.temp_volume
            self.game.curr_menu = self.game.options_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.RIGHT_KEY:
            audio.menu_move()
            # increase volume to 100
            self.game.music_volume = min(self.game.music_volume + 5, 100)
        elif self.game.DOWN_KEY or self.game.LEFT_KEY:
            audio.menu_move()
            # decrease volume down to 0
            self.game.music_volume = max(self.game.music_volume - 5, 0)
        elif self.game.START_KEY:
            audio.menu_select()
            self.game.curr_menu = self.game.options_menu
            self.temp_volume = self.game.music_volume
            self.run_display = False


class CreditsMenu(Menu):
    def __init__(self, game):
        super(CreditsMenu, self).__init__(game)


    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.ESCAPE_KEY:
                audio.menu_back()
                if self.game.previous_menu == "PauseMenu":
                    self.game.curr_menu = self.game.pause_menu
                    self.run_display = False
                else:
                    self.game.curr_menu = self.game.main_menu
                    self.run_display = False

            self.game.display.fill(config.BLACK)
            self.game.draw_text("Credits", 50, config.GAME_WIDTH / 2, config.GAME_HEIGHT / 2 - 20)
            self.game.draw_text("George Welch", 30, config.GAME_WIDTH / 2, config.GAME_HEIGHT / 2 + 10, config.GOLD)
            self.game.draw_text("Mehdi Oudra", 30, config.GAME_WIDTH / 2, config.GAME_HEIGHT / 2 + 40, config.GOLD)
            self.game.draw_text("James Hendry", 30, config.GAME_WIDTH / 2, config.GAME_HEIGHT / 2 + 70, config.GOLD)
            self.game.draw_text("Xiaoyu Chen", 30, config.GAME_WIDTH / 2 - 200, config.GAME_HEIGHT / 2 + 10, config.GOLD)
            self.game.draw_text("Marios Pastos", 30, config.GAME_WIDTH / 2 - 200, config.GAME_HEIGHT / 2 + 40, config.GOLD)
            self.game.draw_text("Matt Horder", 30, config.GAME_WIDTH / 2 - 200, config.GAME_HEIGHT / 2 + 70, config.GOLD)
            self.game.draw_text("Duong Phat Cao", 30, config.GAME_WIDTH / 2 + 200, config.GAME_HEIGHT / 2 + 10, config.GOLD)
            self.game.draw_text("Hanyu Shen", 30, config.GAME_WIDTH / 2 + 200, config.GAME_HEIGHT / 2 + 40, config.GOLD)
            self.game.draw_text("Hsuan-Yin Chen", 30, config.GAME_WIDTH / 2 + 200, config.GAME_HEIGHT / 2 + 70, config.GOLD)


            self.blit_screen()


class CharacterMenu(Menu):

    def __init__(self, game):
        super(CharacterMenu, self).__init__(game)
        self.character_class = 0
        self.character_gender = 0
        self.character_classes = [("PALADIN", "knight"), ("RANGER", "elf"), ("MAGE", "wizzard"), ("ROGUE", "lizard")]
        self.character_genders = ["m", "f"]
        self.actor = Actor(self.game, self.mid_w, self.mid_h + 10,
                           config.get_player_sprite(self.game.player_character,
                                                    self.game.player_gender))

    def display_menu(self):
        secondary_font = config.GOLD
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(config.BLACK)
            self.actor.render()
            self.game.draw_text("CHOOSE YOUR HERO!", 70, self.mid_w, self.mid_h - 100)
            self.game.draw_text("< A", 40, self.mid_w - 60, self.mid_h)
            self.game.draw_text("D >", 40, self.mid_w + 60, self.mid_h)
            self.game.draw_text(self.character_classes[self.character_class][0], 50, self.mid_w, self.mid_h - 50, secondary_font)
            self.game.draw_text("str", 40, self.mid_w - 125, self.mid_h + 50, secondary_font)
            self.game.draw_text(str(character_stats[self.character_classes[self.character_class][0]]["str"]), 40,
                                self.mid_w - 125, self.mid_h + 80, secondary_font)
            self.game.draw_text("dex", 40, self.mid_w - 75, self.mid_h + 50, secondary_font)
            self.game.draw_text(str(character_stats[self.character_classes[self.character_class][0]]["dex"]), 40,
                                self.mid_w - 75, self.mid_h + 80, secondary_font)
            self.game.draw_text("con", 40, self.mid_w - 25, self.mid_h + 50, secondary_font)
            self.game.draw_text(str(character_stats[self.character_classes[self.character_class][0]]["con"]), 40,
                                self.mid_w - 25, self.mid_h + 80, secondary_font)
            self.game.draw_text("int", 40, self.mid_w + 25, self.mid_h + 50, secondary_font)
            self.game.draw_text(str(character_stats[self.character_classes[self.character_class][0]]["int"]), 40,
                                self.mid_w + 25, self.mid_h + 80, secondary_font)
            self.game.draw_text("wis", 40, self.mid_w + 75, self.mid_h + 50, secondary_font)
            self.game.draw_text(str(character_stats[self.character_classes[self.character_class][0]]["wis"]), 40,
                                self.mid_w + 75, self.mid_h + 80, secondary_font)
            self.game.draw_text("cha", 40, self.mid_w + 125, self.mid_h + 50, secondary_font)
            self.game.draw_text(str(character_stats[self.character_classes[self.character_class][0]]["cha"]), 40,
                                self.mid_w + 125, self.mid_h + 80, secondary_font)
            self.game.draw_text("Press ENTER to Confirm", 60, self.mid_w, self.mid_h + 120)
            self.blit_screen()

    def check_input(self):
        if self.game.ESCAPE_KEY:
            audio.menu_back()
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            audio.menu_move()
            self.character_gender = (self.character_gender + 1) % 2
        elif self.game.LEFT_KEY:
            audio.menu_move()
            self.character_class = (self.character_class - 1) % 4
        elif self.game.RIGHT_KEY:
            audio.menu_move()
            self.character_class = (self.character_class + 1) % 4
        elif self.game.START_KEY:
            audio.menu_select()
            self.game.curr_menu = self.game.new_game_menu
            self.run_display = False

        self.game.player_character = self.character_classes[self.character_class][1]
        self.game.player_gender = self.character_genders[self.character_gender]
        self.actor = Actor(self.game, self.mid_w, self.mid_h,
                           config.get_player_sprite(self.game.player_character,
                                                    self.game.player_gender))

class PauseMenu(Menu):

    def __init__(self, game):
        super(PauseMenu, self).__init__(game)
        self.state = "Resume"
        self.start_x, self.start_y = self.mid_w, self.mid_h + 30
        self.options_x, self.options_y = self.mid_w, self.mid_h + 60
        self.credits_x, self.credits_y = self.mid_w, self.mid_h + 90
        self.quit_x, self.quit_y = self.mid_w, self.mid_h + 120
        self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
        self.primary_font = config.WHITE
        self.secondary_font = config.GOLD
        self.start_font_color = self.secondary_font
        self.credits_font_color = self.primary_font
        self.options_font_color = self.primary_font
        self.quit_font_color = self.primary_font
        self.previous_menu = self.previous_menu


    def display_menu(self):
        self.game.previous_menu = "PauseMenu"
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(config.BLACK)
            self.game.draw_text("Game Paused", 50, self.mid_w, self.mid_h - 20, self.primary_font)
            self.game.draw_text("Resume", 50, self.start_x, self.start_y, self.start_font_color)
            self.game.draw_text("Options", 50, self.options_x, self.options_y, self.options_font_color)
            self.game.draw_text("Credits", 50, self.credits_x, self.credits_y, self.credits_font_color)
            self.game.draw_text("Exit to Main Menu", 50, self.quit_x, self.quit_y, self.quit_font_color)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY or self.game.RIGHT_KEY:
            audio.menu_move()
            if self.state == "Resume":
                self.cursor_rect.midtop = (self.options_x + self.offset, self.options_y)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.credits_x + self.offset, self.credits_y)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.quit_x + self.offset, self.quit_y)
                self.state = "Main Menu"
            elif self.state == "Main Menu":
                self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = "Resume"


        elif self.game.UP_KEY or self.game.LEFT_KEY:
            audio.menu_move()
            if self.state == "Resume":
                self.cursor_rect.midtop = (self.quit_x + self.offset, self.quit_y)
                self.state = "Main Menu"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = "Resume"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.options_x + self.offset, self.options_y)
                self.state = "Options"
            elif self.state == "Main Menu":
                self.cursor_rect.midtop = (self.credits_x + self.offset, self.credits_y)
                self.state = "Credits"

        if self.state == "Resume":
            self.start_font_color = self.secondary_font
            self.credits_font_color = self.primary_font
            self.options_font_color = self.primary_font
            self.quit_font_color = self.primary_font
        elif self.state == "Options":
            self.start_font_color = self.primary_font
            self.credits_font_color = self.primary_font
            self.options_font_color = self.secondary_font
            self.quit_font_color = self.primary_font
        elif self.state == "Credits":
            self.start_font_color = self.primary_font
            self.credits_font_color = self.secondary_font
            self.options_font_color = self.primary_font
            self.quit_font_color = self.primary_font
        elif self.state == "Main Menu":
            self.start_font_color = self.primary_font
            self.credits_font_color = self.primary_font
            self.options_font_color = self.primary_font
            self.quit_font_color = self.secondary_font

    def check_input(self):
        self.move_cursor()
        if self.game.ESCAPE_KEY:
            self.game.paused = False
            self.run_display = False
        if self.game.START_KEY:
            audio.menu_select()
            if self.state == "Resume":
                self.game.paused = False
            elif self.state == "Options":
                self.game.curr_menu = self.game.options_menu
            elif self.state == "Credits":
                self.game.curr_menu = self.game.credits_menu
            elif self.state == "Main Menu":
                self.game.running, self.game.playing = True, False
                self.game.paused = False
                self.game.curr_menu = self.game.main_menu
            self.run_display = False





class InGameIntro(Menu):

    def __init__(self, game, text):
        super(InGameIntro, self).__init__(game)
        self.text = text
        self.default_text = ''
        self.IN_GAME_INTRO = '''
        MANY YEARS AGO A PORTAL WAS OPENED TO THE DEPTHS OF HELL. HUMANiTY HAS FINALLY FOUND ITS MATCH. 
        CIVILISATION HAS FALLEN TO DISARRAY AND CIVIL STRIFE. ONLY A HANDFUL ELEMENTS OF RESISTANCE DARE TO DIMINISH THE DEMONS' POWER. 
        JOIN OUR 4 HEROES IN THEIR HEROIC JOURNEY TO RESTORE ORDER TO THE LAND. 
        FIND THE LEGENDARY DEMON SLAYER KEY. FOR GLORY!
        '''

    def display_intro(self):

        self.screen = self.game.window
        starting_pos = 300

        while self.game.intro:
            self.screen.fill(0)
            starting_pos -= 0.3
            msg_list = []
            pos_list = []
            i = 0
            font = pygame.font.Font(self.game.font_name, 15)

            # If 'START_KEY' exit intro and enter game
            self.game.check_events()
            if self.game.START_KEY:
                audio.menu_select()
                self.game.intro = False
                self.game.playing = True
            elif self.game.ESCAPE_KEY:
                audio.menu_back()
                self.game.intro = False
                self.game.playing = False

            font = pygame.font.Font(self.game.font_name, 35)

            screen_text = font.render("Press ENTER to skip.", True, WHITE)
            pos = screen_text.get_rect(topleft=(self.game.window.get_rect().x, self.game.window.get_rect().y))
            self.game.window.blit(screen_text, pos)
            color = pygame.Color('darkgoldenrod1')

            # Scrolling logic
            for line in self.IN_GAME_INTRO.split('\n'):
                msg = font.render(line, True, color)
                msg_list.append(msg)
                pos = msg.get_rect(center=(
                self.game.window.get_rect().centerx, self.game.window.get_rect().centery + starting_pos + i * 30))
                pos_list.append(pos)

                i += 1
            for j in range(i):
                self.screen.blit(msg_list[j], pos_list[j])

            pygame.display.update()
