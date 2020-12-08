from game import Game

g = Game()

while g.running:
    g.change_music()
    g.curr_menu.display_menu()
    g.game_loop()
