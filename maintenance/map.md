


## Map  
To modify the design of rooms or add new game levels, the following files are involved:  
* Main control of maps: `map.py`  
* Level design: `map_list.py`  
* Tiles: `mapframe.txt`  
* Rooms design: `mapframe.txt`, `mapframe2.txt`, `mapframe3.txt`  

The instructions:
- [Adding more tiles.](#adding-more-tiles)
- [Changing design of a room.](#changing-design-of-a-room)
- [Adding new game level.](#adding-new-game-level)
- [Changing floor color for each level.](#changing-floor-color-for-each-level)

### Adding more tiles 
Tiles are accessed through `mapframe.txt` under the `[tilesets]` section. Add the source path of new tiles here and call it from the constructor of class `Map`. 
To use the new tile, change the tile accessed in `draw_map`.
```python
    for x, y in self.symbol_set_name:  
        self.game.display.blit(self.floor_tile_tuple[0], (x * 16, y * 16))  
        self.game.display.blit(self.your_tile_name, (x * 16, y * 16))
```
If the new tile is indicated by new symbol in map, the symbol need to be identified. Add a new empty symbol set in `_init_` and `generate_map`. Then a condition is needed in `generate_map` to locate the tile position in map.
```python
    if patch == 'new symbol':  
	    self.your_tile_set.add((x + self.map_offset[0], y + self.map_offset[1]))  
	    self.unpassable.add((x + self.map_offset[0], y + self.map_offset[1]))
```

### Changing design of a room  
The size of room should be no more than **67*33**. Edit the specification of a room in corresponding file (Level 1: `mapframe.txt`, Level2: `mapframe2.txt`, Level 3: `mapframe2.txt`).
 - `w`: wall
 - `p`: plant
 - `t`: any object
 - `-`: floor
 - `.`: empty space
 - `L` + number: ladder to the lower map level
 - `H` + number: ladder to the higher map level
 - numbers: door to the room indicated
 

    ```
     wwwwwwwwwwwwwwwwwwwwwww..................wwwwwwwwwwwwwwwwwwwww  
     w------p--------------w..................w------------------w  
     w---------------------w..................w-------------------w  
     w---------------------w..................w-------------------w  
     w---------------------wwwwwwwwwwwwwwwwwwww-------------------w  
     w------------------------------------------------------------w  
     w------------------------------------------------------------w  
     w---------------------wwwwwwww---wwwwwwwww-------------------w  
     w---------------------w......w---w.......w-------------------w  
     w---------------------w......w---w.......w-------------------w  
     w---------------------w......w---w.......w-------------------w  
     wwwwwwwww------wwwwwwww......w---w.......wwwwwww------wwwwwwww  
     ........w------w.............w---w.............w------w.......  
     ........w------wwwwwwwwwwwwwww---wwwwwwwwwwwwwww------w.......  
     ........w---------------------------------------------w.......  
     ........w------wwwwwwwwwwwwwww---wwwwwwwwwwwwwww------w.......  
     ........w------w.............w---w.............w------w.......  
     wwwwwwwww------wwwwwwww......w---w.......wwwH2ww------wwwwwwww  
     w---------------------w......w---w.......w-------------------w  
     w-----t---------------w......w---w.......w---L1--------------w  
     w---------------------w......w---w.......w-------------------w  
     w---------------------wwwwwwww---wwwwwwwww-------------------w  
     w------------------------------------------------------------w  
     w------------------------------------------------------------w  
     w---------------------wwwwwwww10wwwwwwwwww-------------------w  
     w---------------------w..................w-------------------w  
     w---------------------w..................w-------------------w  
     wwwwwwwwwwwwwwwwwwwwwww..................wwwwwwwwwwwwwwwwwwwww```

### Adding new game level
To add a new game level, create a new file named `mapefram[level_number].txt` and make your design of the rooms!!

### Changing floor color for each level
To change the featured color of floor, modify the rgb value of the level in `set_color`.

   ```python 
   elif self.current_level == level_number:  
	   for tile in floor_tiles:  
	        tile.fill((r_value, g_value, b_value), special_flags=pygame.BLEND_RGBA_MULT)  
	        self.floor_tile_tuple = self.floor_tile_tuple + (tile,)
  ```