
## NPC and NPC lookup

The  `NPC`  class handles the state and movement of non-hostile NPCs in the game such as the tutorial NPC. The addition of new NPCs or the modification of the behaviour of existing ones is achieved by writing into the `cutscene_lookup.py`  file, where each NPC has the following  list of attributes: 
[npc_type, npc_name, health, shield, level, move_speed, combat_style, ai_type, vision_radius, attack_radius, attack_damage, cooldown]:

```python
npcs = {"tutorial": {"wogol": [20, 5, 10, 1, "melee", "dumb", 500, 10, 3, 1000]}}
```
### Adding new NPCs

To add a new NPC a new entry must be added to the dictionary, specifying the NPC type and name, where the name should be consistent with a sprite name.
New NPC types should also be added to the  `spawn_npc`  function in  `game.py`  so they can be instantiated in the game.
There should be no need to change other functionality in this class as all NPC creation is handled through reference to the npc_lookup, to create easy NPC generation.
