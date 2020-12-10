
## Menu

The menu file contains the `Menu` super class and its subclasses:  `MainMenu`   `StartMenu ` `NewGameMenu ` `LoadGameMenu ` `OptionsMenu` `VolumeMenu ` `CreditsMenu ` `CharacterMenu ` `PauseMenu `  `InGameIntro `   `DeathMenu`.  

## # Adding new options  to the StartMenu
The `StartMenu` class handles the selection of the game mode, currently there are three options:  new game, load game and tutorial, if the game mode options are to be expanded then first it has to be added to the  `display_menu` function as follows:    (game mode or option)

```python
self.game.draw_text("new_game_mode", font, horizontal_position, vertical_position, font_color)
```
Then it need to be added to the `check_input` method which should handle all the users inputs when interacting with the new game mode in the tutorial as shown below for the "New Game" option:

```python
elif (self.game.DOWN_KEY or self.game.RIGHT_KEY):  
    audio.menu_move()  
    if self.state == "New Game":  
        self.state = "Tutorial"  
		  self.load_font_color = self.primary_font  
        self.new_font_color = self.primary_font  
        self.tutorial_font_color = self.secondary_font  
        self.cursor_rect.midtop = (self.tutorial_x + self.offset, self.tutorial_y)```
```

## # Adding a new character to the character menu

Adding a new character to the character menu can be done simply by appending it to the   `character_classes` array  which will be used by the `display_menu`  function:

```python
self.character_classes = [("PALADIN", "knight"), ("RANGER", "elf"), ("MAGE", "wizzard"), ("ROGUE", "lizard")]
```

## # Modifying the game intro

The game intro text is stored in the `IN_GAME_INTRO` variable and can be easily modified:
```python
self.IN_GAME_INTRO = '''
MANY YEARS AGO A PORTAL WAS OPENED TO THE DEPTHS OF HELL. HUMANITY HAS FINALLY FOUND ITS MATCH.

CIVILISATION HAS FALLEN TO DISARRAY AND CIVIL STRIFE. ONLY A HANDFUL ELEMENTS OF RESISTANCE DARE TO DIMINISH THE DEMONS' POWER.

JOIN OUR 4 HEROES IN THEIR HEROIC JOURNEY TO RESTORE ORDER TO THE LAND.

FIND THE LEGENDARY DEMON SLAYER KEY. FOR GLORY!
'''
```
The scrolling speed is determined by the   `starting_pos`  in the `display_intro` and can be modified as one sees fit:
```python
starting_pos = 300
```
