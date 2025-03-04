import re

from pygame import time

from assets.valid_words import VALID_WORDS
from classes.GameState import GameState, Status
from constants import ANIMATION_DURATION, FEEDBACK_DIFF_DURATION


def matches_regex(pattern, string):
    return bool(re.fullmatch(pattern, string))


def api(game: GameState):
    while True:
        string_input = input()
        cmd, *args = string_input.split()
        print()

        match cmd:
            case 'guess':
                if args[0] and args[0].lower() in VALID_WORDS:
                    if game.status != Status.game:
                        print("Error: No active game\n")
                        continue

                    guess_word = args[0].lower()
                    game.enter_word_from_solver(guess_word)
                    delay = FEEDBACK_DIFF_DURATION * 4 + ANIMATION_DURATION + \
                        100 if not game.disable_animations else 0
                    time.delay(delay)
                    offset = 0 if game.status == Status.end else 1
                    feedback = game.words[game.current_word_index -
                                          offset].get_feedback()

                    # print game status
                    print(
                        f"status: {'Completed' if game.status == Status.end else 'In progress'}\n"
                        f"tries: {game.num_of_tries()} / {game.num_guesses}\n"
                        f"success: {game.success if game.status == Status.end else 'NA'}\n"
                    )

                    # print feedback from guess
                    for idx, fdb in enumerate(feedback):
                        print(f"{guess_word[idx]}: {fdb.value}")
                else:
                    print("Invalid guess input")
            case 'new-game':
                if game.status == Status.start:
                    game.status = Status.game
                else:
                    game.reset()

                print("Starting game")
            case 'config':
                if args[0] and args[0] == "lies" and args[1] and matches_regex(r"\b[0-5]\b", args[1]):
                    game.status = Status.config
                    lies = int(args[1])
                    game.num_lies = lies

                    print(f"Number of lies -> {args[1]}")
                elif args[0] and args[0] == "guesses" and args[1] and matches_regex(r"\b[6-9]\b", args[1]):
                    game.status = Status.config
                    guesses = int(args[1])
                    game.num_guesses = guesses

                    print(f"Number of guesses -> {args[1]}")
                else:
                    print("Error: Invalid config")
            case _:
                print("Error: Invalid command")

        print()  # newline for spacing
