from src.game import Game


def main(track_num: int):
    game = Game(track_num)
    game.start()


if __name__ == "__main__":
    main(2)
