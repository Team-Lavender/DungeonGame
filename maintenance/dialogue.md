
## dialogue

The  `StaticText`  class handles the rendering of all text  displayed by the  actors from the player to enemies and NPCs. The text font is gotten from the `game.py` file for consistency. There should be no need to change other functionality in this class as the text, colour, and targeted  actor parameters are set when the `StaticText` object is created and through the `display_text_dialogue` method.

The text colour is set when the class is instantiated as shown here in the class constructor with a fixed offset 
```python
def __init__(self, game, color)  
    self.game = game  
    self.offset_x = -14    
	self.offset_y = -45  
	self.color = color  
    self.font = pygame.font.Font(self.game.font_name, 25)  
    self.coordinates = (0, 0)
```

 The displayed text and target actor are passed to the `display_text_dialogue` 
```python

def display_text_dialogue(self, actor, text)  
    self.coordinates = (actor.pos_x + self.offset_x, actor.pos_y + self.offset_y)  
    screen_text = self.font.render(text, True, self.color)  
    pos = screen_text.get_rect(center=(actor.pos_x, actor.pos_y - 34))  
    self.game.window.blit(screen_text, pos)
```