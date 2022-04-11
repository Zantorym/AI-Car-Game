from src.game import Game
from src.model import train_and_save_model

g = Game()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()

# train_and_save_model()
#
# ai_g = Game()
#
# while ai_g.running:
#     ai_g.curr_menu.display_menu()
#     ai_g.game_loop()