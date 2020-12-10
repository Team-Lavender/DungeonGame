## levelling.py
`levelling.py` contains the methods for levelling up the player character as well as applying the consequences for player death. `level_up` increases the players level, incrementing their next xp target as well as increasing all of their stats by 1 level. the player health and shield are then recalculated and their weapon damage is reclaculated for all of the items in their hotbar.
```python
def level_up(player, amount):
    if amount > 0:
        audio.level_up()
    player.xp = 0
    player.max_xp *= 1.05
    player.entity_level += amount
    player.strength += amount
    player.dexterity += amount
    player.constitution += amount * 2
    player.intellect += amount
    player.wisdom += amount
    player.charisma += amount

    bonuses = {"str": (player.strength - 10) // 2,
               "dex": (player.dexterity - 10) // 2,
               "con": (player.constitution - 10) // 2,
               "int": (player.intellect - 10) // 2,
               "wis": (player.wisdom - 10) // 2,
               "cha": (player.charisma - 10) // 2}

    player.max_health = 5 + player.entity_level + bonuses["con"]
    overshield = max(player.shield - player.max_shield, 0)
    player.max_shield = round(player.armor["AC"] * (1.005 * player.entity_level))
    player.health = player.max_health
    player.shield = player.max_shield + overshield
    if player.shield > 0:
        player.has_shield = True

    player.special_damage += amount * 5

    # update player weapon stats
    for weapon in player.items:
        if weapon is not None:
            weapon.attack_damage = equipment_list.weapons_list[weapon.name]["dmg"] + bonuses[
                equipment_list.weapons_list[weapon.name]["main_stat"]] + player.entity_level // 2
            weapon.attack_speed = 1 / max((equipment_list.weapons_list[weapon.name]["speed"] + (bonuses["dex"] / 2)),
                                          0.01)
            weapon.crit_chance = equipment_list.weapons_list[weapon.name]["crit_chance"] + (bonuses["wis"] * 2)
```

the death function sets the player back to the starting room, and they liose some of their gold and items as well as all their potions. they also lose a number of levels up to a max level, as long as this is not greater than their current level.

```python
# death has chance to lose player levels up to amount given,
# and items may be dropped based on chance to drop. all potions and throwables are lost.
def death(player, chance_to_drop, max_levels_lost):
    player.game.level = 1
    player.game.curr_map.current_map = 0
    player.game.change_map(1)
    player.xp //= (100 // chance_to_drop)
    player.money //= (100 // chance_to_drop)
    level_loss = random.randint(0, max_levels_lost)
    if level_loss >= player.entity_level:
        level_loss = 0
    level_up(player, -level_loss)
    for idx, item in enumerate(player.inventory):
        if item is not None:
            if item[-1] == "potion" or item[-1] == "throwable":
                # lose all potions
                player.inventory[idx] = None
            else:
                # chance to lose weapons
                roll_to_drop = random.randint(0, 101)
                if chance_to_drop >= roll_to_drop:
                    player.inventory[idx] = None
    # lose held potions
    player.potion_1 = []
    player.potion_2 = []
```
