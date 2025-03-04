import argparse
import threading

from api import api
from classes.GameState import GameState
from components.game_loop import game_loop


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--disable-logging',
        help='Disable firebase retry logging',
        action='store_false',
        dest='logging'
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    game = GameState(logging=args.logging)
    api_thread = threading.Thread(target=api, args=(game,), daemon=True)
    api_thread.start()

    # run main game loop
    game_loop(game)
