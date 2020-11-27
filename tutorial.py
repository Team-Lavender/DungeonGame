import pygame

# === CONSTANTS === (UPPER_CASE names)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400



class Button():

    def __init__(self, text, x=0, y=0, width=50, height=50, command=None):

        self.text = text
        self.command = command
        self.image_normal = pygame.Surface((width, height))
        color = pygame.Color('bisque4')
        self.image_normal.fill(color)
        self.image_hovered = pygame.Surface((width, height))
        color2 = pygame.Color("burlywood3")
        self.image_hovered.fill(color2)
        self.image = self.image_normal
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font('assets/pixel_font.ttf', 30)
        self.font2 = pygame.font.Font('assets/pixel_font.ttf', 26)
        text_image = self.font.render(text, True, WHITE)
        text_rect = text_image.get_rect(center=self.rect.center)
        self.image_normal.blit(text_image, text_rect)
        self.image_hovered.blit(text_image, text_rect)
        # you can't use it before `blit`
        self.rect.topleft = (x, y)
        self.hovered = False
        self.clicked = False

    def update(self):
        if self.hovered:
            self.image = self.image_hovered
        else:
            self.image = self.image_normal

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.show_text_box(surface)


    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
            #print("currenlty aimed") # the player is hovering over the button
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.clicked:
                print('Clicked:', self.text)     # we can tell him 'now shoot'
                if self.command:
                    self.command()

    def show_text_box(self,surface):

        test = pygame.draw.rect(surface, (255, 255, 255), (514,540,250,80), 2)
        textTitle = self.font2.render("", True, WHITE)
        rectTitle = textTitle.get_rect(center=surface.get_rect().center)
        surface.blit(textTitle, test)

        text = self.font2.render("PLace cursor above enemy to attack!", True, WHITE)
        text_rect = text.get_rect(center=(514 + 130, 540 + 40))
        surface.blit(text, text_rect)



