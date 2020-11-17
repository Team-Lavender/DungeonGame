# A dictionary that holds cutscene dictionaries
# Each cutscene dictionary contains:
# [0]: actor
#                                    # [1]: movement
#                                    # [2] dialogue ! the dialogue array must equal in length to the movement array

cutscene_lookup_dict = {
    1: {0: [[0], [(184, 280), (368, 280), (368, 350), (368, 370) ,(0, 0)],
            ['Stop right there criminal scum!', 'Nobody breaks the law on my watch!', "I'm confiscating your stolen goods", "Now pay your fine or it's off to jail.", '']],
        1: [[-3], [(762, 324), (630, 341),  (0, 0)],
            ['Well.. well..', 'We have a guest..', '']],

        2:[[-1], [(762, 324), (630, 330), (630, 341), (0, 0)],
            ['No daddy..', "Don't do it", "We'll both die..", '']]

        },

    2: {0: [[-1], [(1050, 350), (700, 350), (700, 160), (200, 160), (200, 500), (0, 0)],
            ['hello', 'it;s me', ' i was wondering', '', '', '']]}
}