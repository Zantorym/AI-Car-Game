from src.menu_game import MenuGame

g = MenuGame()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()