# A dictionary that holds cutscene dictionaries
# Each cutscene dictionary contains:
# [0]: actor
#                                    # [1]: movement
#                                    # [2] dialogue ! the dialogue array must equal in length to the movement array

cutscene_lookup_dict = {

    1: {0: [[0], [(400, 360)], ['ouch!']],
        1: [[44], [(164, 307), (122, 351), (277, 310), (0, 0)],
            ['Welcome back, it must have hurt..', "I hope you didn't forget the basics",
             "Use the WASD keys to move!"]]},

    2: {0: [[44],
            [(350, 313), (350, 150), (460, 168), (460, 420), (540, 420), (544, 434), (565, 340), (587, 280),
             # (660, 280),
             (0, 0)], ['', '', '', '', '', '', ' ',
                       'Come on follow me!',
                       ' ', '']]},
    3: {0: [[44], [(660, 280), (641, 222), (709, 148), (0, 0)],
            ['Good job!', 'Now, well you look at that!',
             'Use your cursor to aim at the enemies and press the right button to hit!'
             ]]},
    4: {0: [[44], [(689, 185), (641, 214), (635, 520), (460, 501), (0, 0)],
            [' ',
             '', ' All of these enemies are conveniently placed, huh',
             'Press 2  to equip  throwable objects and right click to use them', '', '', '']]},

    5: {0: [[44], [(675, 500), (945, 500), (962, 446), (1070, 432), (0, 0)],
            ['now for something more exciting', "Here's the first large monster you will encounter",
             ' Press Q for special attacks', '', '']]},

    6: {0: [[44], [(1003, 390), (1006, 259), (1006, 162), (0, 0)],
            ['Press 1 to heal', "Press P to acces the shop,you'll find there everything you need",
             'Now you are ready, go through this door and face your destiny!'
             '']]}

}
