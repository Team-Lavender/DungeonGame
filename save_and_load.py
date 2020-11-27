import pickle
from game import *
from weapon import *
from datetime import datetime
import equipment_list

class GameSave:
    def __init__(self):
        self.player_dict = {"score": 0, "character_class": "knight", "character_gender": "m", "health": 5, "shield": 0,
                            "level": 0, "money": 0, "stats": [0, 0, 0, 0, 0, 0], "weapons": [], "potion_1": None,
                            "potion_2": None, "inventory": []}
        self.save_name = ""
        self.score = ""
        self.save_time = ""
        self.curr_map_no = None

    def save_game(self, game, save_name=""):
        player = game.curr_actors[0]

        self.player_dict["score"] = player.score
        self.player_dict["character_class"] = game.player_character
        self.player_dict["character_gender"] = game.player_gender
        self.player_dict["health"] = player.health
        self.player_dict["shield"] = player.shield
        self.player_dict["level"] = player.entity_level
        self.player_dict["money"] = player.money
        self.player_dict["inventory"] = player.inventory
        self.player_dict["stats"] = [player.strength, player.dexterity, player.constitution, player.intellect, player.wisdom, player.charisma]
        self.player_dict["weapons"] = []
        for weapon in player.items:
            if weapon is not None:
                self.player_dict["weapons"].append(weapon.name)
        self.player_dict["potion_1"] = player.get_potion(1)
        self.player_dict["potion_2"] = player.get_potion(2)

        if save_name != "":
            self.save_name = save_name
        self.curr_map_no = game.current_map_no
        self.save_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.score = str(player.score)

        # save save state to file
        with open("game_saves/" + self.save_name, "wb") as f:
            pickle.dump(self, f)

    def load_game(self, game):
        # load save state from file
        with open("game_saves/" + self.save_name, "rb") as f:
            self.__dict__.update(pickle.load(f).__dict__)

        # update player attributes to save state
        player = game.curr_actors[0]
        game.player_gender = self.player_dict["character_gender"]
        game.player_character = self.player_dict["character_class"]
        player.character_class = game.player_classes[game.player_character]
        player.sprite = config.get_player_sprite(game.player_character, game.player_gender)
        player.strength = self.player_dict["stats"][0]
        player.dexterity = self.player_dict["stats"][1]
        player.constitution = self.player_dict["stats"][2]
        player.intellect = self.player_dict["stats"][3]
        player.wisdom = self.player_dict["stats"][4]
        player.charisma = self.player_dict["stats"][5]
        bonuses = {"str": (player.strength - 10) // 2,
                   "dex": (player.dexterity - 10) // 2,
                   "con": (player.constitution - 10) // 2,
                   "int": (player.intellect - 10) // 2,
                   "wis": (player.wisdom - 10) // 2,
                   "cha": (player.charisma - 10) // 2}

        player.move_speed = ((5 + ((player.dexterity - 10) // 2)) / 5)

        player.score = self.player_dict["score"]
        player.health = self.player_dict["health"]
        player.shield = self.player_dict["shield"]
        player.entity_level = self.player_dict["level"]
        player.money = self.player_dict["money"]
        player.inventory = self.player_dict["inventory"]
        player.items = []
        for weapon in self.player_dict["weapons"]:
            player.items.append(Weapon(game, weapon, player.pos_x, player.pos_y,
                                       config.get_weapon_sprite(weapon), 1,
                                       equipment_list.weapons_list[weapon]["cost"],
                                       equipment_list.weapons_list[weapon]["type"],
                                       equipment_list.weapons_list[weapon]["range"] * 16,
                                       equipment_list.weapons_list[weapon]["dmg"]
                                       + bonuses[equipment_list.weapons_list[weapon]["main_stat"]],
                                       1 / max((equipment_list.weapons_list[weapon]["speed"] + (bonuses["dex"] / 2)),
                                               0.1),
                                       equipment_list.weapons_list[weapon]["crit_chance"]
                                       + (bonuses["wis"] * 2)))
        for none_weapon in range(len(self.player_dict["weapons"]), 3):
            player.items.append(None)
        player.held_item = player.items[0]

        player.potion_1 = []
        player.potion_2 = []

        if self.player_dict["potion_1"] is not None:
            player.add_potions_to_slot(1, self.player_dict["potion_1"])
        if self.player_dict["potion_2"] is not None:
            player.add_potions_to_slot(2, self.player_dict["potion_2"])

        game.change_map(self.curr_map_no)

    def get_time_and_score(self, save_name):
        if save_name == "":
            pass
        # load save state from file
        try:
            with open("game_saves/" + save_name, "rb") as f:
                self.__dict__.update(pickle.load(f).__dict__)
            return [self.save_time, self.score]
        except PermissionError:
            return ["0", "0"]
