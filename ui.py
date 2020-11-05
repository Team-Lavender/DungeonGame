from player import *

#Hello James
class Ui:
    def __init__(self, game):
        self.game = game
        # Player reference
        # self.player = game.curr_actors[0]
        self.score = 0
        self.score_x, self.score_y = (config.GAME_WIDTH - 90, 0)

    def blit_screen(self, text_surface):
        self.game.display.blit(text_surface, (self.score_x, self.score_y))

    def display_score(self, playing):
        if playing:
            text_surface, text_rect = self.render_text(str(self.score).zfill(6), 50, self.score_x, self.score_y)
            self.blit_screen(text_surface)

    def render_text(self, text, size, x, y):
        font = pygame.font.Font(self.game.font_name, size)
        text_surface = font.render(text, True, config.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        return text_surface, text_rect

    def render(self):
        # TODO fill in render method
        pass
