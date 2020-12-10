
## Cutscene and cutscene_lookup
The CutSceneManager class handles the actors' movements, dialogue and keeps track of the completed cutscenes to avoid the accidental triggering of the same cutscene multiple times . The cutscene triggers are stored as a map tile in  `map.py`  and `mapframe.txt` while handling trigger points is done within the game loop in  `game.py` . The exact waypoints and their accompanying dialogue are stored as a dictionary of dictionaries in  `cutscene_lookup.py`. Extending or modifying cutscenes is a multistep process that requires navigating multiple files and functions as shown below:
- [The Cutscene update method](#cutscene-update)
-  [ Initializing the cutscene set in the map file ](#initializing-the-cutscene-set-in-the-map-file-and-map-frame)
-  [Adding the new cutscene scenario to the cutscene lookup.](#adding-the-cutscene-scenario-to-the-cutscene-lookup)
-  [Adding the cutscene to the game loop.](#adding-the-cutscene-to-the-game-loop)
### Cutscene update
The update function of the CutSceneManager  class handles the cutscene execution steps. It is called when a cutscene has been triggered, with the cutscene number passed as an argument, the first thing that the update function does is to store the specific cutscene details from the cutscene_lookup dictionary as shown here:
```python
cutscene = cutscene_lookup_dict[cutscene_number]  
actors = self.game.curr_actors[self.game.get_npc_index()]  
waypoints = cutscene[self.scenario_index][1]  
i = self.game.get_npc_index()  
dialogue = cutscene[self.scenario_index][2]  
target = waypoints[self.waypoint_index]  
current_dialogue = dialogue[self.dialogue_index]```
```
It then  computes the acceleration based on the position vector and the waypoint coordinates. As shown here:
```python
self.acc = (target - pos).normalize() * 0.5
```
and sets the actor's new position : 
```python
self.vel += self.acc  
if self.vel.length() > self.MAX_SPEED:  
    self.vel.scale_to_length(self.MAX_SPEED)  
pos += self.vel  
self.game.curr_actors[i].pos_x = pos[0]  
self.game.curr_actors[i].pos_y = pos[1]```
```

 In order to synchronize the dialogue with the movement, the distance from the  actor to the next target is calculated, based on that the current dialogue index is incremented and the actor starts displaying the strings stored in the dialogue array of the `cutscene_lookup` file. It's worth mentioning that when the current scenario does not contain any dialogue the actor's speed does not slow down to make the sequence smoother. 
```python
if distance_vector_length < 100 :   
    if current_dialogue != '':  
        self.MAX_SPEED = 0.8  
  text = StaticText(self.game, WHITE)  
        text.display_text_dialogue(actors, current_dialogue)  
        pygame.display.update()  
    if distance_vector_length < 20:  
        self.MAX_SPEED = 2.5  
  self.waypoint_index += 1  
  self.dialogue_index += 1  
  target = waypoints[self.waypoint_index]
```

### Initializing the cutscene set in the map file and map frame
To add a new cutscene a set needs to be created where the coordinates of the specific cutscene flag are stored, here's a subset of the current cutscene sets already in the game
```python
self.cutscene_1 = set()  
self.cutscene_2 = set()  
self.cutscene_3 = set()  
self.cutscene_4 = set()
```
Following that a patch that wasn't used before must be selected, this will work as the trigger for the cutscene. After the selection and inclusion of the patch to the `mapframe.txt` file it will need to be added to its specific set, here's an example from the existing cutscenes:
```python
elif patch == '+':  
    self.cutscene_1.add((x + self.map_offset[0], y + self.map_offset[1]))  
    self.cutscenes.add((x + self.map_offset[0], y + self.map_offset[1]))  
elif patch == '*':  
    self.cutscene_2.add((x + self.map_offset[0], y + self.map_offset[1]))  
    self.cutscenes.add((x + self.map_offset[0], y + self.map_offset[1]))
```


### Adding the cutscene scenario to the cutscene lookup

- The cutscene lookup stores cutscene details,  the new cutscene details must then have the following format 
```python
cutscene_lookup_dict = {  
    cutscene_number: {cutscene_sequence: [[actor_index], [waypoints], [dialogye]]}
    }  
	  
 `````` 
 
### Adding the cutscene to the game loop
- Within `game.py` the function  `get_cutscene()` is being called in the game loop to check if the player's current position matches a cutscene's coordinates in the map, if so it sets the cutscene number to it appropriate value and changes the cutscene trigger to true, any new cutscene will need to be added here as follows:

```python
elif player_pos in self.curr_map.cutscene_2:  
    if 2 not in completed:  
        self.current_cutscene = 2  
  self.cutscene_trigger = True
 ```



