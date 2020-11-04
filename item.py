from actor import *


class Item(Actor):
    def __init__(self, game, pos_x, pos_y, sprite, item_level, cost, combat_style):
        super(Item, self).__init__(game, pos_x, pos_y, sprite)
        self.item_level = item_level
        self.cost = cost
        self.combat_style = combat_style

    # TODO define equip method
    def equip(self):
        pass

    # TODO define destroy method
    def destroy(self):
        pass
