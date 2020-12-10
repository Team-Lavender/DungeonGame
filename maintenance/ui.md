<h1 align="center">
  <br>
  <a href="https://github.com/Team-Lavender/DungeonGame"><img src="https://media.indiedb.com/cache/images/games/1/21/20665/thumb_620x2000/titlescreen.png" alt="DungeonGame" width="500"></a>
  <br>
  DungeonGame
  <br>
</h1>

<h4 align="center">A challenging 2D roguelike game with a variety of enemies and exciting boss battles made entirely in <a href="https://www.pygame.org/" target="_blank">Pygame</a>.</h4>

<p align="center">
 </a>
  <a href="https://saythanks.io/to/amitmerchant1990">
      <img src="https://img.shields.io/badge/python-3.8-blue.svg">



<h1 align="center">
  <br>
  <a ></a>
  <br>
  Maintenance guide
  <br>
</h1>


  
  </a>

</p>

<p align="center">
  <a href="#boss">Boss battles</a> •
  <a href="#ui">UI</a> •
  <a href="#enemies">Enemies</a> •
  <a href="#cutscene">Cutscene</a> •
</p>


## UI
To extend/modify the current User Interface (UI) system either by changing the sprites used or the design of shops, inventory and the hotbar the `ui.py` file must be accessed as follow:

- [Display UI](#display-ui)
- [Changing sprites](#changing-sprites)
- [Shop](#shop)
- [Shopkeeper](#shopkeeper)
- [Boss Name and Health](#boss-name-and-health)
- [Drawing the Inventory](#drawing-the-inventory)
- [Toggling Inventory and Shop](#toggling-inventory-and-shop)
- [Buying and Selling Items](#buying-and-selling-items)

### Display UI
The `display_ui` function handles the rendering of almost everything onto the screen, and as such is the last function called in the game loop in `game.py`. If new functions are needed to be run every tick, they should be implemented in `display_ui`.  

The function is passed 2 variables other than `self`, being `time` and `player`. These represent the current game tick and the player's current state respectively, being items, health, shield, experience, etc. 

These are passed to the likes of `self.render_stats` to update the current health, shield, experience and level. Because of this, `ui.py` doesn't deal with the altering of values, it is simply passed variables, and renders them to the screen as required. 

### Changing Sprites
Each sprite is loaded in the `__init__` function call, this ensures they are only loaded once, as loading images is a resource heavy task. Below shows how you can load a sprite. 
```python
self.coin_0 = pygame.image.load('./assets/frames/coin_anim_f0.png')
```
From here, some sprites are scaled by 2x and others by a specific value to provide the correct size for the screen. We can simply scale an image by 2x with the below call. Note that this returns a new scaled image, and so must be assigned to a variable.
```python
self.coin_0 = pygame.transform.scale2x(self.coin_0)
```
And the below shows how to scale by a value. Here we have used `self.coin_scale = 24` as the value to scale by.
```python
self.coin_0 = pygame.transform.scale(self.coin_0, (self.coin_scale, self.coin_scale))
```
One could either edit the current sprites so as to change the currently displayed sprites used by the UI, requiring no changes to other aspects of the code. Alternatively, new sprites could be added to the game and the code adjusted to display as required.


### Shop
`ui.py` handles the shop's functionality, including the rendering of the player's items, the shop's stock, highlighting of currently selected items, and the buying and selling of items. 

Selecting items is handled by `shop_select_item`, which retrieves the current mouse position with `mouse = pygame.mouse.get_pos()`, and as a result, the inventory slot which the mouse position corresponds to. We can then use this information to store the current inventory index in `self.item_to_find_info = index`, which holds the selected item. The inventory tile's location is stored 
in `self.item_to_find_info_pos` so that it can be highlighted. 

Highlighting is handled by: 
```python
def highlight_item(self, tile):  
    highlight = pygame.Surface(((tile[1][0] - tile[0][0]), (tile[1][1] - tile[0][1])))  
    highlight.set_alpha(50)  
    highlight.fill((252, 207, 3))  
    self.game.display.blit(highlight, (tile[0][0], tile[0][1]))
```
This is passed the tile's location as explained above, and then provides a golden highlight, this makes it clear which item is currently selected both in the Shop when selling or buying items, and also when swapping items in the inventory.

When an item is clicked, its stats are displayed so the user can easily compare weapons and make upgrades. `draw_item_stats` takes the currently selected item, looks up its stats in `equipment_list.py`, and neatly renders them to the screen. It separately handles weapons, potions and throwables, as they all hold different stats. This means if a new item is added to the game, its stats will already render correctly when clicked.

### Shopkeeper

We currently only have one shop, and so only require one shopkeeper, and they are rendered using: 
```python
def draw_shopkeeper(self, shop_type):  
    if shop_type == 'weapon':  
        shopkeeper = self.get_shopkeeper(pygame.time.get_ticks())  
        shopkeeper = pygame.transform.scale(shopkeeper, (200, 200))  
  
        self.game.display.blit(shopkeeper, (config.GAME_WIDTH // 2 - 550, config.GAME_HEIGHT // 2 - 120))  
        self.game.display.blit(self.big_chat_bubble, (150, 160))  
        self.game.draw_text("How can I help", 40, 246, 190, (0, 0, 0))  
        self.game.draw_text("you today?", 40, 246, 214, (0, 0, 0))
```
This function was made to be useable no matter how many shops there are, due to the argument `shop_type`. For the weapon shop we initially call `self.get_shopkeeper` (explained below) to retrieve the current sprite to be rendered. It is then scaled as mentioned in [Changing sprites](#changing-sprites). Finally, it is rendered to the screen with a chat box with customisable text.

```python
def get_shopkeeper(self, time):  
    if time % self.shopkeeper_rotation < self.shopkeeper_rotation / 4:  
        return self.shopkeeper_weapons_0  
    if self.shopkeeper_rotation / 4 <= time % self.shopkeeper_rotation < self.shopkeeper_rotation / 2:  
        return self.shopkeeper_weapons_1  
    if self.shopkeeper_rotation / 2 <= time % self.shopkeeper_rotation < self.shopkeeper_rotation * 3 / 4:  
        return self.shopkeeper_weapons_2  
    if time % self.shopkeeper_rotation >= self.shopkeeper_rotation * 3 / 4:  
        return self.shopkeeper_weapons_3
```
This checks the current game time and compares it to `self.shopkeeper_rotation = 1000`. The four `if` statements represent each of the four sprites used in the shopkeeper's animation. As can be seen, this splits the 1000 by 4, thus a full rotation of the sprite animation takes 1000ms with each of the four sprites occupying the screen for 250ms per rotation. Due to this, a new shopkeeper could be added for new stores,, and the animation speed can be easily altered. Other functions act in a similar way, such as `coin_animation` and `specbar_animation`. 

### Boss Name and Health
The rendering of a boss's health and name is handled in:
```python
def display_boss_bar(self, curr_health, max_health, boss_name):  
    bg = pygame.Surface((450, 70))  
    bg.fill((0, 0, 0))  
    health_width = 436 * (curr_health / max_health)  
    if health_width > 0:  
        pygame.draw.rect(bg, self.hotbar_bg_colour, ((2, 48), (440, 16)))  
        pygame.draw.rect(bg, config.BLACK, ((4, 50), (436, 12)))  
        pygame.draw.rect(bg, (218, 78, 76), ((4, 50), (health_width, 12)))  
    self.game.display.blit(bg, (700, 6))  
    if curr_health <= 0:  
        self.game.draw_text("HAS BEEN DEFEATED", 50, 924, 50, (218, 78, 76))  
    self.game.draw_text(boss_name.upper(), 50, 924, 20)
```
Here we initial create a black background and a width for the health bar, which scales with respect to the current health (`curr_health`) and maximum health (`max_health`). While the boss is alive, the health bar is rendered to the screen, with the with corresponding to the percentage of health remaining. Once the boss is defeated, this is replaced by `"HAS BEEN DEFEATED"`. And finally, the boss's name is rendered above the health bar.

### Drawing the inventory

This is carried all handled by `draw_inventory`. First, a silver background is created, and then a smaller black surface inside this to provide the trim seen in the game. This is a reusable function and can be passed text, which is rendered above the box, and as such is how the inventory, shop and info boxes are drawn. 

If tiles are required, the keyword argument `tiles=true` should be passed into draw_inventory. It then loops through drawing a 5x5 grid, which can be altered changing `for _ in range(5):`.  Tiles are drawn and if it is for the inventory, the player's inventory is checked for items, if items are found, they are also rendered to the screen. The coordinates of each tile is added to a list, which can be indexed to find the coords of the tile containing the corresponding item from the player's inventory or shop's stock. This way we can easily highlight the tile when selected. 

### Toggling Inventory and Shop
This is carried out with a simple `True` or `False` flag.
```python
def toggle_shop(self):  
    self.shop_inventory_tile_positions = []  
    self.shop_shop_tile_positions = []  
    background_mask = pygame.Surface((config.GAME_WIDTH, config.GAME_HEIGHT))  
    background_mask.set_alpha(200)  
    background_mask.fill((0, 0, 0))  
    self.game.display.blit(background_mask, (0, 0))  
    self.draw_inventory(268, 268, config.GAME_WIDTH // 2 - (268 + 20), config.GAME_HEIGHT // 2 - 140, "Inventory", True)  
    self.draw_inventory(268, 268, config.GAME_WIDTH // 2 + 20, config.GAME_HEIGHT // 2 - 140, "Shop", True)  
    if self.item_to_find_info is not None:  
        self.draw_inventory(180, 268, config.GAME_WIDTH // 2 + 310, config.GAME_HEIGHT // 2 - 140, "Info", False)  
    self.draw_shopkeeper('weapon')
```
As we can see, any selected items are cleared when then shop or inventory is reopened. The `background_mask` simply applies a shading to the background, providing focus for the shop and inventory. `draw_inventory`, from [Drawing the Inventory](#drawing-the-inventory), is then called with locations of the width and height of the inventory and shop, x and y coordinates for rendering, a name and the tile flag.

If there is a currently selected item, as checked in:
```python 
if self.item_to_find_info is not None:
```
Then the info for the corresponding item is rendered. And finally, the shopkeeper, in this case for the weapon shop, is drawn.

### Buying and Selling Items

The transaction of items and gold between the player and shopkeeper is all dealt with in `shop_buy_or_sell`. When an item is selected, its type is checked, and if from the player inventory, a sell option is displayed, otherwise, a buy option is. Simple checks are run to check quantity owned, if there is enough gold when buying, and if there is space in the inventory. If satisfied, the transaction occurs and items are placed in the inventory and money deducted.