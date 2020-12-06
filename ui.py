from player import *
import config
import pygame
import equipment_list
# current_health // 20 -> 100 = 5 90 = 4 80 = 4 95 = 4 70 = 3
# current_health %20 -> 100 = 0 90 = 10 80 = 0 95 = 15 70 = 10
#  max_health // 20 -> 120 = 6 - (3 + 1) = 2

'''
TODO
Refactor image loading
Refactor blit function to be used in shields and hearts?
Fix confusing names Hearts/Health?
Healing animation?
x and y spacing constants?
Enemy health bars
'''


class Ui:
    def __init__(self, game):
        self.time = pygame.time
        self.game = game
        self.score_x, self.score_y = (config.GAME_WIDTH - 90, 0)
        self.money_x, self.money_y = (config.GAME_WIDTH - 90, 25)
        self.hotbar_x, self.hotbar_y = (config.GAME_WIDTH / 2, config.GAME_HEIGHT - 44)
        self.initial_tile_x = self.hotbar_x - 97
        self.final_tile_x = self.hotbar_x + 97
        self.coin_index = 0
        self.coin_full_rotation = 750
        self.shopkeeper_rotation = 1000
        self.coin_scale = 24
        self.hotbar_bg_colour = (177, 198, 202)
        self.hotbar_main_colour = (53, 44, 43)
        self.specbar_colour = (128, 0, 128)
        self.specbar_animation_time = 1000
        self.consumable_1_animation = False
        self.consumable_2_animation = False
        self.consumable_1_timer = 0
        self.consumable_2_timer = 0
        self.hotbar_tile_positions = []
        self.inventory_tile_positions = []
        self.shop_inventory_tile_positions = []
        self.shop_shop_tile_positions = []
        self.item_to_swap = None
        self.item_to_swap_pos = None
        self.item_to_find_info = None
        self.item_to_find_info_pos = None
        self.item_is_inv = False
        self.item_is_shop = False
        self.shop_stock = game.weapon_shop.shop_inv

        # Load graphics outside class?
        self.full_heart = pygame.image.load('./assets/frames/ui_heart_full.png').convert_alpha()
        self.full_heart = pygame.transform.scale2x(self.full_heart)
        self.half_heart = pygame.image.load('./assets/frames/ui_heart_half.png').convert_alpha()
        self.half_heart = pygame.transform.scale2x(self.half_heart)
        self.empty_heart = pygame.image.load('./assets/frames/ui_heart_empty.png').convert_alpha()
        self.empty_heart = pygame.transform.scale2x(self.empty_heart)

        self.heart_dict = {0: self.empty_heart,
                           0.5: self.half_heart,
                           1: self.full_heart}

        # PLACEHOLDER SHIELD IMAGE
        self.full_shield = pygame.image.load('./assets/frames/ui_shield_full.png').convert_alpha()
        self.full_shield = pygame.transform.scale2x(self.full_shield)
        self.half_shield = pygame.image.load('./assets/frames/ui_shield_half.png').convert_alpha()
        self.half_shield = pygame.transform.scale2x(self.half_shield)
        self.empty_shield = pygame.image.load('./assets/frames/ui_shield_empty.png').convert_alpha()
        self.empty_shield = pygame.transform.scale2x(self.empty_shield)

        self.shield_dict = {0: self.empty_shield,
                            0.5: self.half_shield,
                            1: self.full_shield}

        self.shopkeeper_weapons_0 = pygame.image.load('./assets/frames/necromancer_idle_anim_f0.png')
        self.shopkeeper_weapons_1 = pygame.image.load('./assets/frames/necromancer_idle_anim_f1.png')
        self.shopkeeper_weapons_2 = pygame.image.load('./assets/frames/necromancer_idle_anim_f2.png')
        self.shopkeeper_weapons_3 = pygame.image.load('./assets/frames/necromancer_idle_anim_f3.png')

        self.spec_0 = pygame.image.load('./assets/frames/spec_bar_lightning_0.png')
        self.spec_1 = pygame.image.load('./assets/frames/spec_bar_lightning_1.png')
        self.spec_2 = pygame.image.load('./assets/frames/spec_bar_lightning_2.png')
        self.spec_3 = pygame.image.load('./assets/frames/spec_bar_lightning_3.png')
        self.spec_4 = pygame.image.load('./assets/frames/spec_bar_lightning_4.png')
        self.spec_5 = pygame.image.load('./assets/frames/spec_bar_lightning_5.png')

        self.coin_0 = pygame.image.load('./assets/frames/coin_anim_f0.png')
        self.coin_0 = pygame.transform.scale(self.coin_0, (self.coin_scale, self.coin_scale))
        self.coin_1 = pygame.image.load('./assets/frames/coin_anim_f1.png')
        self.coin_1 = pygame.transform.scale(self.coin_1, (self.coin_scale, self.coin_scale))
        self.coin_2 = pygame.image.load('./assets/frames/coin_anim_f2.png')
        self.coin_2 = pygame.transform.scale(self.coin_2, (self.coin_scale, self.coin_scale))
        self.coin_3 = pygame.image.load('./assets/frames/coin_anim_f3.png')
        self.coin_3 = pygame.transform.scale(self.coin_3, (self.coin_scale, self.coin_scale))

        self.big_chat_bubble = pygame.image.load('./assets/frames/big_chat_bubble.png')
        self.buy_button = pygame.image.load('./assets/frames/buy_icon.png')
        self.sell_button = pygame.image.load('./assets/frames/sell_icon.png')

    # Is this what future display_ui class should look like?
    '''
    def display_ui(self, player):
        text_surface, text_rect = self.render_text(str(player.score).zfill(6), 50, self.score_x, self.score_y)
        self.render_hearts(player.max_hearts, player.curr_hearts)
        self.render_shields(player.max_shields, player.curr_shields)
        self.render_gold(player.curr_gold)
        self.blit_screen(text_surface)    
    '''

    # For testing
    def display_ui(self, time, player):
        if not self.game.show_inventory:
            self.item_to_swap = None
        if not self.game.show_shop:
            self.item_to_find_info_pos = None
        self.render_text(str(player.score).zfill(6), 50, self.score_x, self.score_y)
        self.render_money(str(player.money).zfill(6), 50, self.money_x, self.money_y)
        self.render_stats(player.max_health, player.health, 'health')
        self.render_stats(player.max_shield, player.shield, 'shield')
        self.render_stats(player.max_xp, player.xp, 'xp')
        self.coin_animation(time)
        self.draw_hotbar(player)
        if not self.game.show_inventory:
            self.draw_specbar(player)
        if self.item_to_swap_pos is not None and self.item_to_swap is not None:
            self.highlight_item(self.item_to_swap_pos)
        if self.item_to_find_info_pos is not None and self.item_to_find_info_pos is not None:
            self.highlight_item(self.item_to_find_info_pos)
        if self.item_to_find_info is not None and self.item_is_shop:
            self.draw_item_stats(equipment_list.weapons_list[self.shop_stock[self.item_to_find_info][0]], 'shop')
        elif self.item_to_find_info is not None and self.item_is_inv:
            self.draw_item_stats(equipment_list.weapons_list[self.game.curr_actors[0].inventory[self.item_to_find_info][0]], 'inv')
        if not self.game.show_shop:
            self.item_to_find_info = None
            self.item_to_find_info_pos = None


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

    def render_stats(self, max_stat, stat, bar_type):
        background = pygame.Surface((340, 32))
        if bar_type == 'xp':
            background = pygame.Surface((220, 32))
        background.fill(config.BLACK)
        if bar_type == 'health':
            background.blit(self.full_heart, (0, 0))
            pygame.draw.rect(background, self.hotbar_bg_colour, ((52, 8), (204, 16)))
            pygame.draw.rect(background, config.BLACK, ((54, 10), (200, 12)))
            health_width = 200 * stat/max_stat
            if health_width != 0:
                pygame.draw.rect(background, (218, 78, 76), ((54, 10), (health_width, 12)))
            self.game.display.blit(background, (10, 10))
            self.game.draw_text((str(stat) + '/' + str(max_stat)), 32, 300, 23, (240, 240, 240))
        if bar_type == 'shield':
            background.blit(self.full_shield, (-2, 0))
            pygame.draw.rect(background, self.hotbar_bg_colour, ((52, 8), (204, 16)))
            pygame.draw.rect(background, config.BLACK, ((54, 10), (200, 12)))
            over_shield = 0
            if max_stat == 0 and stat == 0:
                shield_width = 0
            elif stat > max_stat == 0:
                shield_width = 0
                over_shield = 200 * (stat - max_stat) / (5 + self.game.curr_actors[0].entity_level)
            elif stat > max_stat != 0:
                shield_width = 200
                over_shield = 200 * (stat - max_stat) / (5 + self.game.curr_actors[0].entity_level)
            else:
                shield_width = 200 * stat / max_stat
            if shield_width != 0:
                pygame.draw.rect(background, (0, 171, 255), ((54, 10), (shield_width, 12)))
            if over_shield != 0:
                pygame.draw.rect(background, (0, 221, 255), ((54, 10), (over_shield, 12)))
            self.game.display.blit(background, (10, 46))
            self.game.draw_text((str(stat) + '/' + str(max_stat)), 32, 300, 59, (240, 240, 240))
        if bar_type == 'xp':
            pygame.draw.rect(background, self.hotbar_bg_colour, ((2, 8), (204, 16)))
            pygame.draw.rect(background, config.BLACK, ((4, 10), (200, 12)))
            if stat > max_stat:
                stat = max_stat
            xp_width = 200 * stat / max_stat
            if xp_width != 0:
                pygame.draw.rect(background, (107, 176, 51), ((4, 10), (xp_width, 12)))
            self.game.display.blit(background, (348, 46))
            self.game.draw_text(("Level: " + str(self.game.curr_actors[0].entity_level)), 32, 380, 23, (240, 240, 240))
            self.game.draw_text((str(stat) + '/' + str(int(max_stat))), 32, 460, 59, (240, 240, 240))

    def select_item(self):
        mouse = pygame.mouse.get_pos()
        for index, tile in enumerate(self.hotbar_tile_positions):
            if tile[0][0] < mouse[0] < tile[1][0] and tile[0][1] < mouse[1] < tile[1][1]:
                if self.item_to_swap is None:
                    self.item_to_swap = index
                    self.item_to_swap_pos = tile
                elif self.item_to_swap is not None:
                    self.game.curr_actors[0].swap_inventory(self.item_to_swap, index)
                    self.item_to_swap = None
                    self.item_to_swap_pos = None
                self.game.ACTION = False
                return
        for index, tile in enumerate(self.inventory_tile_positions):
            if tile[0][0] < mouse[0] < tile[1][0] and tile[0][1] < mouse[1] < tile[1][1]:
                # highlight tile
                if self.item_to_swap is None:
                    self.item_to_swap = index + 5
                    self.item_to_swap_pos = tile
                elif self.item_to_swap is not None:
                    self.game.curr_actors[0].swap_inventory(self.item_to_swap, index + 5)
                    self.item_to_swap = None
                    self.item_to_swap_pos = None
                self.game.ACTION = False
                return

    def shop_select_item(self):
        mouse = pygame.mouse.get_pos()
        for index, tile in enumerate(self.shop_inventory_tile_positions):
            if tile[0][0] < mouse[0] < tile[1][0] and tile[0][1] < mouse[1] < tile[1][1]:
                if self.game.curr_actors[0].inventory[index] is not None:
                    # if self.game.curr_actors[0].inventory[index][-1] == "weapon":
                    #     print(equipment_list.weapons_list[self.game.curr_actors[0].inventory[index][0]])
                    self.item_to_find_info = index
                    self.item_to_find_info_pos = tile
                    self.item_is_inv = True
                    self.item_is_shop = False
                return
            else:
                self.item_to_find_info = None
                self.item_to_find_info_pos = None
        for index, tile in enumerate(self.shop_shop_tile_positions):
            if tile[0][0] < mouse[0] < tile[1][0] and tile[0][1] < mouse[1] < tile[1][1]:
                if self.shop_stock[index] is not None:
                    self.item_to_find_info = index
                    self.item_to_find_info_pos = tile
                    self.item_is_inv = False
                    self.item_is_shop = True
                return
            else:
                self.item_to_find_info = None
                self.item_to_find_info_pos = None

    def draw_item_stats(self, item, type):
        self.game.draw_text(item['name'], 36, config.GAME_WIDTH // 2 + 400, config.GAME_HEIGHT // 2 - 120, (252, 207, 3))
        self.game.draw_text('Main Stat: ' + item['main_stat'], 30, config.GAME_WIDTH // 2 + 400, config.GAME_HEIGHT // 2 - 90)
        self.game.draw_text('Damage: ' + str(item['dmg']), 30, config.GAME_WIDTH // 2 + 400, config.GAME_HEIGHT // 2 - 65)
        self.game.draw_text('Speed: ' + str(item['speed']), 30, config.GAME_WIDTH // 2 + 400, config.GAME_HEIGHT // 2 - 40)
        self.game.draw_text('Crit Chance: ' + str(item['crit_chance']), 30, config.GAME_WIDTH // 2 + 400, config.GAME_HEIGHT // 2 - 15)
        self.game.draw_text('Type: ' + item['type'], 30, config.GAME_WIDTH // 2 + 400, config.GAME_HEIGHT // 2 + 10)
        if type == 'shop':
            self.game.draw_text('Cost: ' + str(item['cost']), 40, config.GAME_WIDTH // 2 + 400, config.GAME_HEIGHT // 2 + 35)
            self.game.display.blit(self.buy_button, (config.GAME_WIDTH // 2 + 340, config.GAME_HEIGHT // 2 + 60))
            self.game.draw_text('Buy', 80, config.GAME_WIDTH // 2 + 404, config.GAME_HEIGHT // 2 + 78)
        if type == 'inv':
            self.game.draw_text('Sell for: ' + str(int(item['cost'] * .6)), 40, config.GAME_WIDTH // 2 + 400, config.GAME_HEIGHT // 2 + 35)
            self.game.display.blit(self.sell_button, (config.GAME_WIDTH // 2 + 340, config.GAME_HEIGHT // 2 + 60))
            self.game.draw_text('Sell', 80, config.GAME_WIDTH // 2 + 404, config.GAME_HEIGHT // 2 + 82)

    def highlight_item(self, tile):
        highlight = pygame.Surface(((tile[1][0] - tile[0][0]), (tile[1][1] - tile[0][1])))
        highlight.fill((252, 207, 3, 50))
        self.game.display.blit(highlight, (tile[0][0], tile[0][1]))

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

    def draw_shopkeeper(self, shop_type):
        if shop_type == 'weapon':
            shopkeeper = self.get_shopkeeper(pygame.time.get_ticks())
            shopkeeper = pygame.transform.scale(shopkeeper, (200, 200))

            self.game.display.blit(shopkeeper, (config.GAME_WIDTH // 2 - 550, config.GAME_HEIGHT // 2 - 120))
            self.game.display.blit(self.big_chat_bubble, (150, 160))
            self.game.draw_text("How can I help", 40, 246, 190, (0, 0, 0))
            self.game.draw_text("you today?", 40, 246, 214, (0, 0, 0))

    def get_shopkeeper(self, time):
        if time % self.shopkeeper_rotation < self.shopkeeper_rotation / 4:
            return self.shopkeeper_weapons_0
        if self.shopkeeper_rotation / 4 <= time % self.shopkeeper_rotation < self.shopkeeper_rotation / 2:
            return self.shopkeeper_weapons_1
        if self.shopkeeper_rotation / 2 <= time % self.shopkeeper_rotation < self.shopkeeper_rotation * 3 / 4:
            return self.shopkeeper_weapons_2
        if time % self.shopkeeper_rotation >= self.shopkeeper_rotation * 3 / 4:
            return self.shopkeeper_weapons_3

    def draw_tile(self, width, height, x, y, inventory, text):
        tile = pygame.Surface((width, height))
        tile.fill(self.hotbar_main_colour)
        inventory.blit(tile, (x, y))

    def flash_consumable(self, i):
        hotbar_tile = pygame.Surface((46, 40))
        hotbar_tile.set_alpha(150)
        hotbar_tile.fill((50, 97, 168))
        self.game.display.blit(hotbar_tile, (self.final_tile_x - i * 48 - 23, self.hotbar_y - 20))

    def draw_inventory(self, height, width, x, y, text="", tiles=False):
        inventory = pygame.Surface((height, width))
        inventory.fill(self.hotbar_bg_colour)
        inventory_border = pygame.Rect(3, 3, height - 6, width - 6)
        pygame.draw.rect(inventory, (0, 0, 0), inventory_border)
        counter = 0
        inventory_list = self.game.curr_actors[0].inventory
        # shop_list = self.game.shop_inventory
        # initial_inventory_tile_x = x
        if tiles:
            tile_offset_y = 5
            for _ in range(5):
                tile_offset_x = 5
                for _ in range(5):
                    self.draw_tile(50, 50, tile_offset_x, tile_offset_y, inventory, text)
                    if text == "Inventory":
                        tl = (x + tile_offset_x, y + tile_offset_y)
                        br = (x + tile_offset_x + 50, y + tile_offset_y + 50)
                        self.shop_inventory_tile_positions.append((tl, br))
                        if inventory_list[counter] is not None:
                            if inventory_list[counter][-1] == 'weapon':
                                hotbar_item = config.get_weapon_sprite(inventory_list[counter][0])["idle"][0]
                                hotbar_item = pygame.transform.rotate(hotbar_item, 45)
                            elif inventory_list[counter][-1] == 'potion':
                                hotbar_item = config.get_potion_sprite(equipment_list.potions_list[inventory_list[counter][0]]["sprite_name"])["idle"][0]
                                hotbar_item = pygame.transform.scale2x(hotbar_item)

                            elif inventory_list[counter][-1] == 'throwable':
                                hotbar_item = config.get_potion_sprite(
                                    equipment_list.throwables_list[inventory_list[counter][0]]["sprite_name"])["idle"][0]
                                hotbar_item = pygame.transform.scale2x(hotbar_item)
                            else:
                                hotbar_item = pygame.Surface((0, 0))
                            hotbar_item_rect = hotbar_item.get_rect()
                            hotbar_item_rect.center = (30 + (counter % 5) * 52, 30 + (counter // 5) * 52)
                            # hotbar_item_rect.center = (initial_inventory_tile_x + tile_offset_x, config.GAME_HEIGHT // 2 + tile_offset_y)
                            inventory.blit(hotbar_item, hotbar_item_rect)
                    if text == "Shop":
                        tl = (x + tile_offset_x, y + tile_offset_y)
                        br = (x + tile_offset_x + 50, y + tile_offset_y + 50)
                        self.shop_shop_tile_positions.append((tl, br))
                        # Change below for shop inventory
                        if self.shop_stock[counter] is not None:
                            if self.shop_stock[counter][-1] == 'weapon':
                                hotbar_item = config.get_weapon_sprite(self.shop_stock[counter][0])["idle"][0]
                                hotbar_item = pygame.transform.rotate(hotbar_item, 45)
                            elif self.shop_stock[counter][-1] == 'potion':
                                hotbar_item = config.get_potion_sprite(equipment_list.potions_list[self.shop_stock[counter][0]]["sprite_name"])["idle"][0]
                                hotbar_item = pygame.transform.scale2x(hotbar_item)
                            elif self.shop_stock[counter][-1] == 'throwable':
                                hotbar_item = config.get_potion_sprite(
                                    equipment_list.throwables_list[self.shop_stock[counter][0]]["sprite_name"])["idle"][0]
                                hotbar_item = pygame.transform.scale2x(hotbar_item)
                            else:
                                hotbar_item = pygame.Surface((0, 0))
                            hotbar_item_rect = hotbar_item.get_rect()
                            hotbar_item_rect.center = (30 + (counter % 5) * 52, 30 + (counter // 5) * 52)
                            # hotbar_item_rect.center = (initial_inventory_tile_x + tile_offset_x, config.GAME_HEIGHT // 2 + tile_offset_y)
                            inventory.blit(hotbar_item, hotbar_item_rect)

                    tile_offset_x += 52
                    counter += 1
                tile_offset_y += 52
        self.game.display.blit(inventory, (x, y))
        if text == "Inventory":
            for i, tile in enumerate(self.shop_inventory_tile_positions):
                curr_item = inventory_list[i]
                if curr_item is not None and curr_item[1] > 1:
                    self.game.draw_text(str(curr_item[1]), 20, tile[0][0] + 44, tile[0][1] + 4)
                    # print(tile[0][0], tile[0][1])
            # for i, item in enumerate(inventory_list):
            #     if item is not None and item[1] > 1:
            #         self.game.draw_text(str(item[1]), 20, initial_inventory_tile_x + ,
            #                             config.GAME_HEIGHT // 2)
        self.game.draw_text(text, 50, x + inventory.get_width() // 2, y - 30)

    def toggle_inventory(self):
        self.inventory_tile_positions = []
        background_mask = pygame.Surface((config.GAME_WIDTH, config.GAME_HEIGHT))
        background_mask.set_alpha(200)
        background_mask.fill((0, 0, 0))
        self.game.display.blit(background_mask, (0, 0))
        self.game.draw_text("Inventory", 50, config.GAME_WIDTH // 2, config.GAME_HEIGHT // 2)
        self.game.draw_text("Equipped", 50, config.GAME_WIDTH // 2, config.GAME_HEIGHT // 2 + 264)
        self.game.draw_text("Click", 40, config.GAME_WIDTH // 2 + 210, config.GAME_HEIGHT // 2 + 120)
        self.game.draw_text("to Rearrange", 40, config.GAME_WIDTH // 2 + 210, config.GAME_HEIGHT // 2 + 150)
        self.game.draw_text("Weapons", 40, self.hotbar_x - 180, self.hotbar_y - 6)
        self.game.draw_text("Consumables", 40, self.hotbar_x + 200, self.hotbar_y - 6)
        inventory_bg = pygame.Rect(0, 0, 248, 218)
        inventory_bg.center = (config.GAME_WIDTH // 2, config.GAME_HEIGHT // 2 + 140)
        inventory_border = pygame.Rect(0, 0, 242, 212)
        inventory_border.center = (config.GAME_WIDTH // 2, config.GAME_HEIGHT // 2 + 140)
        pygame.draw.rect(self.game.display, self.hotbar_bg_colour, inventory_bg)
        pygame.draw.rect(self.game.display, (0, 0, 0), inventory_border)
        tile_y_offset = 56
        initial_inventory_tile_x = config.GAME_WIDTH // 2 - 96
        counter = 0
        inventory = self.game.curr_actors[0].inventory
        for _ in range(5):
            tile_x_offset = 0
            for _ in range(5):
                quantity = 0
                inventory_tile = pygame.Rect(0, 0, 46, 40)
                inventory_tile.center = (initial_inventory_tile_x + tile_x_offset,
                                         config.GAME_HEIGHT // 2 + tile_y_offset)
                tl = inventory_tile.topleft
                br = inventory_tile.bottomright
                self.inventory_tile_positions.append((tl, br))
                pygame.draw.rect(self.game.display, self.hotbar_main_colour, inventory_tile)
                if inventory[counter] is not None:
                    if inventory[counter][-1] == 'weapon':
                        hotbar_item = config.get_weapon_sprite(inventory[counter][0])["idle"][0]
                        hotbar_item = pygame.transform.rotate(hotbar_item, 45)
                    elif inventory[counter][-1] == 'potion':
                        quantity = inventory[counter][1]
                        hotbar_item = config.get_potion_sprite(equipment_list.potions_list[inventory[counter][0]]["sprite_name"])["idle"][0]
                        hotbar_item = pygame.transform.scale2x(hotbar_item)
                    elif inventory[counter][-1] == 'throwable':
                        quantity = inventory[counter][1]
                        hotbar_item = config.get_potion_sprite(equipment_list.throwables_list[inventory[counter][0]]["sprite_name"])["idle"][0]
                        hotbar_item = pygame.transform.scale2x(hotbar_item)
                    else:
                        hotbar_item = pygame.Surface((0, 0))
                    hotbar_item_rect = hotbar_item.get_rect()
                    hotbar_item_rect.center = (initial_inventory_tile_x + tile_x_offset, config.GAME_HEIGHT // 2 + tile_y_offset)
                    self.game.display.blit(hotbar_item, hotbar_item_rect)
                    if quantity > 0:
                        self.game.draw_text(str(quantity), 20, initial_inventory_tile_x + tile_x_offset + 18, config.GAME_HEIGHT // 2 + tile_y_offset - 14)

                tile_x_offset += 48
                counter += 1
            tile_y_offset += 42

    def draw_hotbar(self, player):
        self.hotbar_tile_positions = []
        hotbar_bg = pygame.Rect(0, 0, 250, 50)
        hotbar_bg.center = (self.hotbar_x, self.hotbar_y)
        hotbar_border = pygame.Rect(0, 0, 244, 44)
        hotbar_border.center = (self.hotbar_x, self.hotbar_y)
        tile_offset = 0

        pygame.draw.rect(self.game.display, self.hotbar_bg_colour, hotbar_bg)
        pygame.draw.rect(self.game.display, (0, 0, 0), hotbar_border)
        for _ in range(3):
            hotbar_tile = pygame.Rect(0, 0, 46, 40)
            hotbar_tile.center = (self.initial_tile_x + tile_offset, self.hotbar_y)
            pygame.draw.rect(self.game.display, self.hotbar_main_colour, hotbar_tile)
            tile_offset += 48
            tl = hotbar_tile.topleft
            br = hotbar_tile.bottomright
            self.hotbar_tile_positions.append((tl, br))

        tile_offset = 0

        for _ in range(2):
            hotbar_tile = pygame.Rect(0, 0, 46, 40)
            hotbar_tile.center = (self.final_tile_x - tile_offset, self.hotbar_y)
            pygame.draw.rect(self.game.display, self.hotbar_main_colour, hotbar_tile)
            tl = hotbar_tile.topleft
            br = hotbar_tile.bottomright
            self.hotbar_tile_positions.append((tl, br))
            tile_offset += 48
        # Fix for opposite items tiles
        self.hotbar_tile_positions[3], self.hotbar_tile_positions[4] = self.hotbar_tile_positions[4], self.hotbar_tile_positions[3]
        tile_number = player.held_item_index
        if not self.game.show_inventory:
            self.highlight_tile(tile_number)
        else:
            self.inventory_highlight()
        if self.consumable_1_animation and len(player.potion_1) != 0:
            self.flash_consumable(1)
            if pygame.time.get_ticks() - self.consumable_1_timer >= 480:
                self.consumable_1_animation = False

        if self.consumable_2_animation and len(player.potion_2) != 0:
            self.flash_consumable(0)
            if pygame.time.get_ticks() - self.consumable_2_timer >= 480:
                self.consumable_2_animation = False
        for i, item in enumerate(player.items):
            if item is not None:
                hotbar_item = player.items[i].sprite["idle"][0]
                hotbar_item = pygame.transform.rotate(hotbar_item, 45)
                hotbar_item_rect = hotbar_item.get_rect()
                hotbar_item_rect.center = (self.hotbar_x - 97 + i * 48, self.hotbar_y)
                self.game.display.blit(hotbar_item, hotbar_item_rect)
        self.draw_item(player.potion_1, 1)
        self.draw_item(player.potion_2, 0)

    def draw_item(self, items, i):
        if len(items) > 0:
            item = items[0]
            if item is not None:
                hotbar_item = item.sprite["idle"][0]
                hotbar_item = pygame.transform.scale2x(hotbar_item)
                hotbar_item_rect = hotbar_item.get_rect()
                hotbar_item_rect.center = (self.final_tile_x - i * 48, self.hotbar_y - 3)
                self.game.display.blit(hotbar_item, hotbar_item_rect)
                self.game.draw_text(str(len(items)), 20, self.final_tile_x + 15 - i * 48, self.hotbar_y - 15)

    def inventory_highlight(self):
        weapon_tile = pygame.Surface((46, 40))
        weapon_tile.set_alpha(80)
        weapon_tile.fill((255, 80, 12))
        consumable_tile = pygame.Surface((46, 40))
        consumable_tile.set_alpha(80)
        consumable_tile.fill((12, 242, 12))
        self.game.display.blit(weapon_tile, (self.initial_tile_x - 23, self.hotbar_y - 20))
        self.game.display.blit(weapon_tile, (self.initial_tile_x + 48 - 23, self.hotbar_y - 20))
        self.game.display.blit(weapon_tile, (self.initial_tile_x + 48 * 2 - 23, self.hotbar_y - 20))
        self.game.display.blit(consumable_tile, (self.initial_tile_x + 48 * 3 - 21, self.hotbar_y - 20))
        self.game.display.blit(consumable_tile, (self.initial_tile_x + 48 * 4 - 21, self.hotbar_y - 20))

    def highlight_tile(self, tile):
        hotbar_tile = pygame.Surface((46, 40))
        hotbar_tile.set_alpha(80)
        hotbar_tile.fill((252, 207, 3))
        self.game.display.blit(hotbar_tile, (self.initial_tile_x + 48 * tile - 23, self.hotbar_y - 20))

        # draw special attack bar relative to hotbar
    def draw_specbar(self, player):
        specbar_height = 16
        specbar_width = 246  # Same as hotbar
        y_dist_from_hotbar = 40
        spec = player.special_charge
        spec_percent = (spec / 100) * specbar_width
        spec_outline = pygame.Surface((250, 20))
        spec_outline.fill(self.hotbar_bg_colour)
        spec_background = pygame.Surface((246, 16))
        spec_background.fill((0, 0, 0))
        spec_outline.blit(spec_background, (2, 2))
        spec_filling = pygame.Rect(2, 2, spec_percent, specbar_height)
        if spec < 100:
            pygame.draw.rect(spec_outline, self.specbar_colour, spec_filling)
        else:
            self.specbar_animation(pygame.time.get_ticks(), spec_outline)
        self.game.display.blit(spec_outline, (self.hotbar_x - 250 // 2,
                                              self.hotbar_y - (specbar_height // 2 + y_dist_from_hotbar)))

    def specbar_animation(self, time, spec_outline):
        if time % self.specbar_animation_time < self.specbar_animation_time / 6:
            self.blit_full_specbar(self.spec_0, spec_outline)
        if self.specbar_animation_time / 6 <= time % self.specbar_animation_time < self.specbar_animation_time / 3:
            self.blit_full_specbar(self.spec_1, spec_outline)
        if self.specbar_animation_time / 3 <= time % self.specbar_animation_time < self.specbar_animation_time / 2:
            self.blit_full_specbar(self.spec_2, spec_outline)
        if self.specbar_animation_time / 2 <= time % self.specbar_animation_time < self.specbar_animation_time * 2 / 3:
            self.blit_full_specbar(self.spec_3, spec_outline)
        if self.specbar_animation_time * 2 / 3 <= time % self.specbar_animation_time < self.specbar_animation_time * 5 / 6:
            self.blit_full_specbar(self.spec_4, spec_outline)
        if time % self.specbar_animation_time > self.specbar_animation_time * 5 / 6:
            self.blit_full_specbar(self.spec_5, spec_outline)

    def blit_full_specbar(self, image, spec_outline):
        spec_outline.blit(image, (0, 0))

    def coin_animation(self, time):
        if time % self.coin_full_rotation < self.coin_full_rotation / 4:
            self.blit_coin(self.coin_0, self.money_x, self.money_y)
        if self.coin_full_rotation / 4 <= time % self.coin_full_rotation < self.coin_full_rotation / 2:
            self.blit_coin(self.coin_1, self.money_x, self.money_y)
        if self.coin_full_rotation / 2 <= time % self.coin_full_rotation < self.coin_full_rotation * 3 / 4:
            self.blit_coin(self.coin_2, self.money_x, self.money_y)
        if time % self.coin_full_rotation > self.coin_full_rotation * 3 / 4:
            self.blit_coin(self.coin_3, self.money_x, self.money_y)

    def blit_coin(self, coin, x, y):
        self.game.display.blit(coin, (x - 30, y + 12))

    def render_money(self, text, size, x, y):
        font = pygame.font.Font(self.game.font_name, size)
        text_surface = font.render(text, True, config.GOLD)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.game.display.blit(text_surface, (self.money_x, self.money_y))

    def render_text(self, text, size, x, y):
        font = pygame.font.Font(self.game.font_name, size)
        text_surface = font.render(text, True, config.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.game.display.blit(text_surface, (self.score_x, self.score_y))

    '''
    @staticmethod
    def calculate_half_list(maxi, curr):
        half_list = []

        no_total = maxi // 2
        no_full = curr // 2
        if 1 <= curr % 2:
            no_half = 1
        else:
            no_half = 0
        no_empty = no_total - (no_full + no_half)
        for i in range(no_full):
            half_list.append(1)
        for i in range(no_half):
            half_list.append(0.5)
        for i in range(no_empty):
            half_list.append(0)
        return half_list
    '''

    # Only works if damage is integer
    @staticmethod
    def calculate_half_list(maxi, curr):
        no_total = (maxi // 2) + (maxi % 2)
        no_full = curr // 2
        no_half = curr % 2
        if no_full < 0:
            no_full = 0
        if no_half == 1 and curr <= 0:
            no_half = 0
        no_empty = no_total - (no_full + no_half)
        # E.g.: [1,1,0.5,0] = [Full, Full, Half, Empty]
        half_list = [1] * no_full + [0.5] * no_half + [0] * no_empty

        return half_list

    def render_hearts(self, max_health, curr_health):
        x_coord = 10
        hearts = self.calculate_half_list(max_health, curr_health)
        for heart in hearts:
            self.game.display.blit(self.heart_dict[heart], (x_coord, 10))
            x_coord += 30

    def render_shields(self, max_shields, curr_shields):
        x_coord = 8
        shields = self.calculate_half_list(max_shields, curr_shields)
        for shield in shields:
            self.game.display.blit(self.shield_dict[shield], (x_coord, 40))
            x_coord += 30
