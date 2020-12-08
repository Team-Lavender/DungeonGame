

# Levels key: number of level, value: map filename
Levels = {-1: "mapframe_tutorial.txt", 1: "mapframe.txt", 2: "mapframe2.txt", 3: "mapframe3.txt"}

# ROOMS has level as key and doors position of each room as one element of value
ROOMS = {1:('D', 'UD', 'UD', 'UR', 'LU', 'DU', 'DU', 'DR', 'LD', 'UD', 'UD', 'UR', 'LU', 'DU', 'DU', 'D'),
         2:('R', 'LD', 'UL', 'RD', 'UD', 'UR', 'LU', 'DR', 'LD', 'UR', 'LU', 'DU', 'DL', 'RU', 'DR', 'L'),
         3:('R', 'LR', 'LD', 'UL', 'RL', 'RD', 'UD', 'UR', 'LU', 'DR', 'LD', 'UR', 'LU', 'DU', 'DU', 'D')}

# minimap images
ROOMS_IMG = ['room.png', 'connect_room.png', 'hor_corridor.png', 'player_symbol.png']

# [Basemap]
Basemap='''wwwwwwwwwwwwwwwwwwwwwww..................wwwwwwwwwwwwwwwwwwwww
w------O--------------w..................w----P--------------w
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
........w------wwwwwwwwwwwwwww-S-wwwwwwwwwwwwwww------w.......
........w----------------------L0---------------------w.......
........w------wwwwwwwwwwwwwww---wwwwwwwwwwwwwww------w.......
........w------w.............w---w.............w------w.......
wwwwwwwww------wwwwwwww......w---w.......wwwwwww------wwwwwwww
w---------------------w......w---w.......w---Q---------------w
w-----M---------------w......w---w.......w-------------------w
w---------------------w......w---w.......w-------------------w
w---------------------wwwwwwww---wwwwwwwww-------------------w
w------------------------------------------------------------w
w------------------------------------------------------------w
w---------------------wwwwwwwwwwwwwwwwwwww-------------------w
w---------------------w..................w-------------------w
w---------------------w..................w-------------------w
wwwwwwwwwwwwwwwwwwwwwww..................wwwwwwwwwwwwwwwwwwwww'''


# [tutorial]
tutorial = '''map1 = wwwwwwwwwwwwwwwwwwww.......wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
       w------------------w.......w---------------tt---------------------w
       w------------------w.......w--------------------------------------w
       w-------r----------w.......w--------------------------------------w
       w------------------w.......w----p-------e-------------------------w
       w------------------w.......w---------------------------S----------w
       w---------E--------wwwwwwwww--------------------------------------w
       w-----------------------------------------------------------------w
       w----------------------r------------------------------------------w
       w-----------------------------------------------------------------w
       w---------------wwwwwwwwww----------e-----------------------------w
       w---------------w........w----------------------------------------w
       w---------------w........wwwwwwwwwwwwwwww------wwwwwwwwwwwwwwwwwwww
       wwwwwww---------w.......................w------w...................
       ......w---------w.......................w------w...................
       ......w---R-----w.......................w-r----w...................
       ......w---------w.......................w------w...................
       ......w---------wwwwwwwwwwwwwwwwwwwwwwwww------wwwwwwwwwwwwwwwwwwww
       wwwwwww--------------pp-------------------------------------------w
       wt-------------------------------------------e--------------------w
       wt----------------------------------------------------------------w
       w---------E--------------------R----------------------------------w
       w----------------e------------------------------------------------w
       w-----------------------------------------------------------------w
       w---------------------------------------e--------------E----------w
       w-----------------------------------------------------------------w
       w-----------------------------------------------------------------w
       wp------e-------------------------R-------------------------------w
       wt----------------------------------------------------------------w
       w-----------------wwwwwwwww---------------------------------------w
       w-----------------w.......w---------------------------------------w
       w-----------------w.......w-----------pp--------------------------w
       wwwwww2wwwwwwwwwwww.......wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'''