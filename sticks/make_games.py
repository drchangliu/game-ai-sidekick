import itertools
import random
import copy
from sticks import Sticks_Game
import csv

def generate_moves():
    all_moves = ["A:A C", "A:A D", "A:B C", "A:B D", "S:A", "S:B"]

    histories = []

    def play_game(current_game):
        if current_game.is_over() or len(current_game.history) > 9:
            if not current_game.is_over():
                current_game.history.append("Game Over, Revisitation.")
            # Longest possible game is 9 moves, with revisitation it is infinite
            histories.append(current_game.history)
            return
        for move in all_moves:
            new_game = copy.deepcopy(current_game)
            if new_game.is_legal(move):
                new_game.move(move)
                play_game(new_game)

    game = Sticks_Game()
    play_game(game)

    num_games = len(histories)

    # Shuffle games dataset
    random.shuffle(histories)

    # Flatten array
    histories = list(itertools.chain(*histories))

    with open("games.txt", "w") as file:
        for move in histories:
            file.write(move + "\n")

    # with open('games.csv', 'w') as file:
    #     csv_writer = csv.writer(file, delimiter=',')
    #     csv_writer.writerows(histories)

    print(f"Saved {num_games} games to the games.txt")

if __name__ == "__main__":
    generate_moves()
