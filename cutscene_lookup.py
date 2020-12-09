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
            [(369, 313), (369, 150), (490, 168), (490, 470), (550, 470), (594, 434), (592, 365), (587, 300), (710, 317),
             (0, 0)], ['', '', '', '', '', '', 'oooh scray! this must be the sound that you just heard',
                       'Use your cursor to aim at the enemies and press the right button to hit',
                       'dont worry i cast a powerfull spell so they should be harmless', '']]},
    3: {0: [[44], [(690, 317), (668, 422), (680, 544), (0, 0)],
            ['', 'All of these enemies are conveniently placed, huh',
             'Press 2 on your keyboard to equip and use throwable objects', '']]},
    4: {0: [[44], [(690, 317), (798, 310), (798, 224), (898, 222), (0, 0)],
            ['now for something more exiting', 'Heres the first large monster you will encounter',
             ' try pressing Q for special attacks', '', '', '', '']]},
    5: {0: [[44], [(898, 222), (956, 290), (962, 446), (1070, 432), (0, 0)], ['', 'your journey is about to start',
                                                                              'speak with each of the elders and each of them will giveyou helpfull tips (here we will have multiple npcs each of them telling the player to press p for envntory exetera)',
                                                                              '', '', '', '']]}}

#         5: {  0: [[44], [(898, 222), (956, 290),(962, 446), (1070, 432),  (0,0)],[ 'your journey is about to start',  'speak with each of the elders and each of them will giveyou helpfull tips (here we will have multiple npcs each of them telling the player to press p for envntory exetera)', '', '', '', '' ]]}}

#       0: [[-1], [(369, 150),  (490, 168),  (490, 470), (550, 470),  (594, 434), (592, 365),(587, 300), (690, 317), (0,0)],['a','c', 'd','e','f','j', 'All of these enemies are conveniently, huh',  'Press 2 on your keyboard to equip and use throwable objects', '']]}}
