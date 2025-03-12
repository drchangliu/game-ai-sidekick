import itertools
import random
import copy
from game import Connect_Four_Game
import csv

def generate_moves(num_games=10000):
    all_moves = [0,1,2,3,4,5,6]
    histories = []

    for _ in range(num_games):
        game = Connect_Four_Game()

        while not game.is_over():
            move = random.choice(all_moves)  # Choose a random column
            if game.is_legal(move):
                game.move(move)

        histories.append(game.history)

    # Flatten array
    histories = list(itertools.chain(*histories))

    with open("games.txt", "w") as file:
        for move in histories:
            file.write(move + "\n")

    # with open('games.csv', 'w') as file:
        # csv_writer = csv.writer(file, delimiter=',')
        # csv_writer.writerows(histories)

    print(f"Saved {num_games} games to the games.txt")

if __name__ == "__main__":
    generate_moves()
