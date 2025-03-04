import time

import wandb

from classes.GameState import GameState, Status
from classes.LetterCell import Feedback
from constants import LLM_MODEL, MAX_LLM_CONTINUOUS_CALLS

NUM_RUNS = 10


def run_game(game: GameState, run_id: int, total_tries: int, total_success: int):
    print(f"Starting run {run_id + 1}")
    game.reset()
    total_completion = 0
    completion = 0

    while game.status != Status.end:
        game.enter_word_from_ai()

        # get the feedback
        offset = 0 if game.status == Status.end else 1
        feedback = game.words[game.current_word_index -
                              offset].get_feedback()

        # check completion
        completion = 0
        for fdb in feedback:
            match fdb:
                case Feedback.incorrect:
                    completion += 0
                case Feedback.present:
                    completion += 0.5
                case Feedback.correct:
                    completion += 1

        if game.was_valid_guess:
            total_completion += completion

    avg_game_completion = total_completion / game.num_of_tries()
    total_success += 1 if game.success else 0
    total_tries += game.num_of_tries()

    print(f"Average game completion: {avg_game_completion} / 5")
    print(f"Average tries: {total_tries / (run_id + 1)}")
    print(f"Average success: {total_success / (run_id + 1)}")
    print()
    wandb.log(
        {
            "average_game_completion": avg_game_completion,
            "rolling_avg_tries": total_tries / (run_id + 1),
            "rolling_avg_success": total_success / (run_id + 1)
        },
        step=(run_id + 1)
    )

    return total_tries, total_success


def test_games():
    game = GameState(show_window=False, logging=False)
    total_success = 0
    total_tries = 0
    for i in range(NUM_RUNS):
        total_tries, total_success = run_game(
            game, i, total_tries, total_success)
        if i < NUM_RUNS - 1:
            time.sleep(45)


if __name__ == "__main__":
    wandb.init(
        project="llm-wordle",
        name=f"{LLM_MODEL}-{MAX_LLM_CONTINUOUS_CALLS}-retries"
    )
    test_games()
