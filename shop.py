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
from config import *
from equipment_list import *

class Shop():
    def __init__(self, shop_level):
        self.shop_level = shop_level
        self.shopkeeper_sprite = 0
        self.weapons_dict = weapons_list
        self.potions_dict = potions_list
        self.test = []

    def sell(self):
        pass

    def buy(self):
        pass
    def has_enough_coins(self):
        pass
    def get_player_level(self):
        pass
    def get_player_class(self):
        pass
    def printElements(self):
        for element in self.weapons_dict:
            self.test.append(self.weapons_dict[element].values())

test = []
for element in weapons_list:
     test.append(weapons_list[element])
#print(test)

for i in range(len(weapons_list)):
    print(list(weapons_list.keys())[i],test[1]['cost'], test[1]['type'], get_weapon_sprite(str(list(weapons_list.keys())[i]))['idle'])



print(list(weapons_list.keys())[0])#, get_weapon_sprite(str(weapons_list.keys())[0]))
#print(weapons_list.keys , test[1]['cost'])

