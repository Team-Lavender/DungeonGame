"""
add shopkeeper in the shop UI (on the left?)
fields:
shop_table = [][]
item_lookup = {sprite: x, type: x, price: x, level: x: info: x}

sell()

buy()
helper methods:
has_enough_coins()
get_level()
check_player_class()

sell(item):
get_item_price(item)
add_money_to_player(amount)
remove_item_from_inv()
# Item added to the shop?

show_info(item):
get_info(item)

"""
import equipment_list

class Shop():
    def __init__(self):
        self.shopkeeper_sprite = 0
        self.max_stock = 1
        self.money = 100000
        self.shop_inv = [None] * 25


    def get_item_cost(self, item):
        # item is [item_name, quant, type]
        if item is not None:
            if item[-1] == "weapon":
                weapon_name = item[0]
                cost = equipment_list.weapons_list[weapon_name]["cost"]

            elif item[-1] == "potion":
                potion_name = item[0]
                cost = equipment_list.potions_list[potion_name]["cost"]

            elif item[-1] == "throwable":
                throwable_name = item[0]
                cost = equipment_list.throwables_list[throwable_name]["cost"]

            return cost
        return None

    def has_enough_money(self, curr_money, item_price):
        if curr_money >= item_price:
            return True
        else:
            return False

    def buy_item(self, player, item_index):
        # item = [name, quantity, type]
        item = self.shop_inv[item_index]

        # Add multiplier
        price = int(self.get_item_cost(item))

        player_item = [item[0], 1, item[-1]]
        if self.has_enough_money(player.money, price):
            # add_to_inv checks hotbar first
            # Does this function increment potions?
            if player.add_to_inventory(player_item):
                player.money -= price
                self.money += price
                # Dec shop quant, remove if 0
                '''
                weapon[1] -= 1
                if weapon[1] == 0:
                    weapon = None

                self.shop_inv[item_index] = weapon
                '''
                return True

            else:
                # Player has no room in hotbar/inventory
                return False

        # Player not enough money
        return False

    def sell_item(self, player, item_index):
        # sell price between  cost * (0.4 to 0.7)?
        # Doesn't sell from hotbar
        # Item 'disappears'
        player_item = player.inventory[item_index]
        if player_item is not None:
            price = int(self.get_item_cost(player_item) * 0.6)
            if self.has_enough_money(self.money, price):
                self.money -= price
                player.money += price
                player_item[1] -= 1
                if player_item[1] == 0:
                    player.inventory[item_index] = None

                # Item has sold
                return True

            # Shop not enough gold
            return False

        # Item is None
        return False


class WeaponShop(Shop):
    def __init__(self):
        super().__init__()
        self.shopkeeper_sprite = 0
        self.init_shop_inv()


    def init_shop_inv(self):
        # weapon = [name, quantity, type = "weapon"]
        # Test fill for UI

        # First row - Swords
        self.shop_inv[0] = ["knight_sword", self.max_stock, "weapon"]
        self.shop_inv[1] = ["knife", self.max_stock, "weapon"]
        self.shop_inv[2] = ["katana", self.max_stock, "weapon"]
        self.shop_inv[3] = ["lavish_sword", self.max_stock, "weapon"]
        self.shop_inv[4] = ["dagger_ruby", self.max_stock, "weapon"]

        # Second row - Bows
        self.shop_inv[5] = ["bow", self.max_stock, "weapon"]
        self.shop_inv[6] = ["ricochet_bow", self.max_stock, "weapon"]
        self.shop_inv[7] = ["split_bow", self.max_stock, "weapon"]
        self.shop_inv[8] = ["staff_of_lightning", self.max_stock, "weapon"]
        self.shop_inv[9] = ["staff_of_fireball", self.max_stock, "weapon"]

        self.shop_inv[10] = ["staff_of_acid", self.max_stock, "weapon"]
        self.shop_inv[11] = ["magic_hammer", self.max_stock, "weapon"]
        self.shop_inv[12] = None
        self.shop_inv[13] = None
        self.shop_inv[14] = None
        # self.shop_inv[8] = ["seeking_bow", self.max_stock, "weapon"]

        # Third row - Staves
        self.shop_inv[15] = ["heal_small", self.max_stock, "potion"]
        self.shop_inv[16] = ["heal_large", self.max_stock, "potion"]
        self.shop_inv[17] = ["shield_small", self.max_stock, "potion"]
        self.shop_inv[18] = ["shield_large", self.max_stock, "potion"]
        self.shop_inv[19] = ["super_small", self.max_stock, "potion"]
        self.shop_inv[24] = ["super_large", self.max_stock, "potion"]

        # 6 - 18 is None

        self.shop_inv[20] = ["explosive_small", self.max_stock, "throwable"]
        self.shop_inv[21] = ["explosive_large", self.max_stock, "throwable"]
        self.shop_inv[22] = ["acid_small", self.max_stock, "throwable"]
        self.shop_inv[23] = ["acid_large", self.max_stock, "throwable"]

        # Fourth row - Empty?
        # self.shop_inv[15] = None
        # self.shop_inv[16] = None
        # self.shop_inv[17] = None
        # self.shop_inv[18] = None
        # self.shop_inv[19] = None
        #
        # # Fifth row - Powerful
        # self.shop_inv[20] = None
        # self.shop_inv[21] = None
        # self.shop_inv[22] = None
        # self.shop_inv[23] = None
        # self.shop_inv[24] = None


class SpecialShop(Shop):
    def __init__(self):
        super().__init__()
        self.shopkeeper_sprite = 1
        # self.init_shop_inv()


    # def init_shop_inv(self):
    #     # (name, quant, type = "potion" or "throwable")
    #     # Test fill for UI
    #
    #     self.shop_inv[0] = ["heal_small", self.max_stock, "potion"]
    #     self.shop_inv[1] = ["heal_large", self.max_stock, "potion"]
    #     self.shop_inv[2] = ["shield_small", self.max_stock, "potion"]
    #     self.shop_inv[3] = ["shield_large", self.max_stock, "potion"]
    #     self.shop_inv[4] = ["super_small", self.max_stock, "potion"]
    #     self.shop_inv[5] = ["super_large", self.max_stock, "potion"]
    #
    #     # 6 - 18 is None
    #
    #     self.shop_inv[19] = ["explosive_small", self.max_stock, "throwable"]
    #     self.shop_inv[20] = ["explosive_large", self.max_stock, "throwable"]
    #     self.shop_inv[21] = ["acid_small", self.max_stock, "throwable"]
    #     self.shop_inv[22] = ["acid_large", self.max_stock, "throwable"]


'''
test = []
for element in weapons_list:
    test.append(weapons_list[element])
# print(test)

for i in range(len(weapons_list)):
    print(list(weapons_list.keys())[i], test[1]['cost'], test[1]['type'],
          get_weapon_sprite(str(list(weapons_list.keys())[i]))['idle'])

print(list(weapons_list.keys())[0])  # , get_weapon_sprite(str(weapons_list.keys())[0]))
# print(weapons_list.keys , test[1]['cost'])
'''

# Shop quant doesn't matter
# Cast to int
# Weapons don't stack
# shop stock is infinite
# When you sell a weapon just remove it from player, doesn't matter what happens in shop

