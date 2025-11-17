import time
import json

from pathlib import Path

import wandb

from classes.GameState import GameState, Status
from classes.LetterCell import Feedback
from constants import LLM_MODEL, MAX_LLM_CONTINUOUS_CALLS

LOG_DIR = Path("benchmarks/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / f"llm_wordle_results.json"

NUM_RUNS = 10


# Modify run_game to append per-game stats
def run_game(game: GameState, run_id: int, total_tries: int, total_success: int, total_bad_guesses: int,
             total_good_guesses: int, total_latency: float, total_guess_latency: float, total_guess_count: int,
             total_llm_calls: int, results_dict=None):
    print(f"Starting run {run_id + 1}")
    game.reset()
    total_completion = 0
    completion = 0
    game_start_time = time.time()

    while game.status != Status.end:
        guess_start_time = time.time()
        tries = game.enter_word_from_ai()
        guess_end_time = time.time()
        guess_latency = guess_end_time - guess_start_time
        total_guess_latency += guess_latency

        # get the feedback
        offset = 0 if game.status == Status.end else 1
        feedback = game.words[game.current_word_index - offset].get_feedback()

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
            total_good_guesses += 1
            total_bad_guesses += tries - 1
            total_llm_calls += tries
        else:
            total_bad_guesses += 1
            total_llm_calls += 1

        total_guess_count += 1

    game_end_time = time.time()
    game_latency = game_end_time - game_start_time
    total_latency += game_latency

    avg_game_completion = total_completion / game.num_of_tries()
    total_success += 1 if game.success else 0
    total_tries += game.num_of_tries()

    print(f"Average game completion: {avg_game_completion} / 5")
    print(f"Average tries: {total_tries / (run_id + 1)}")
    print(f"Average success: {total_success / (run_id + 1)}")
    print(f"Average latency: {total_latency / (run_id + 1):.2f}s")
    print(
        f"Average guess latency: {total_guess_latency / total_guess_count:.2f}s" if total_guess_count > 0 else "Average guess latency: N/A")
    good_bad_ratio = total_good_guesses / \
        total_bad_guesses if total_bad_guesses > 0 else total_good_guesses
    print(
        f"Good Guess Bad Guess Ratio: {good_bad_ratio:.2f}" if total_bad_guesses > 0 else f"Good Guess Bad Guess Ratio: {total_good_guesses} (no bad guesses)")
    print(
        f"Average LLM calls per guess: {total_llm_calls / total_good_guesses if total_good_guesses > 0 else 0}")
    print()
    wandb.log(
        {
            "average_game_completion": avg_game_completion,
            "rolling_avg_tries": total_tries / (run_id + 1),
            "rolling_avg_success": total_success / (run_id + 1),
            "rolling_avg_game_latency": total_latency / (run_id + 1),
            "rolling_avg_guess_latency": total_guess_latency / total_guess_count if total_guess_count > 0 else 0,
            "good_guess_bad_guess_ratio": total_good_guesses / total_bad_guesses if total_bad_guesses > 0 else total_good_guesses,
            "avg_llm_calls_per_guess": total_llm_calls / total_good_guesses if total_good_guesses > 0 else 0
        },
        step=(run_id + 1)
    )

    if results_dict is not None:
        results_dict["games"].append({
            "run_id": run_id + 1,
            "average_game_completion": avg_game_completion,
            "tries": game.num_of_tries(),
            "success": game.success,
            "latency": game_latency,
            "bad_guesses": total_bad_guesses,
            "good_guess_bad_guess_ratio": total_good_guesses / total_bad_guesses if total_bad_guesses > 0 else total_good_guesses,
            "avg_llm_calls_per_guess": total_llm_calls / total_good_guesses if total_good_guesses > 0 else 0,
            "total_llm_calls": total_llm_calls
        })

    return total_tries, total_success, total_bad_guesses, total_good_guesses, total_latency, total_guess_latency, total_guess_count, total_llm_calls


def test_games():
    game = GameState(show_window=False, logging=False)

    # set to 1 lie and 9 guesses for fibble, else it will play wordle
    # game.num_lies = 1
    # game.num_guesses = 9

    total_success = 0
    total_tries = 0
    total_bad_guesses = 0
    total_good_guesses = 0
    total_guess_count = 0
    total_latency = 0.0
    total_guess_latency = 0.0
    total_llm_calls = 0

    results = {
        "num_runs": NUM_RUNS,
        "LLM_MODEL": LLM_MODEL,
        "MAX_LLM_CONTINUOUS_CALLS": MAX_LLM_CONTINUOUS_CALLS,
        "games": []
    }

    for i in range(NUM_RUNS):
        total_tries, total_success, total_bad_guesses, total_good_guesses, total_latency, total_guess_latency, total_guess_count, total_llm_calls = run_game(
            game, i, total_tries, total_success, total_bad_guesses, total_good_guesses, total_latency, total_guess_latency, total_guess_count, total_llm_calls, results)
        if i < NUM_RUNS - 1:
            time.sleep(1)

    # Calculate final averages
    win_rate = total_success / NUM_RUNS
    avg_tries = total_tries / NUM_RUNS
    avg_latency = total_latency / NUM_RUNS
    avg_llm_calls_per_guess_overall = total_llm_calls / \
        total_good_guesses if total_good_guesses > 0 else 0

    # Save the results
    results["total_bad_guesses"] = total_bad_guesses
    results["total_good_guesses"] = total_good_guesses
    results["total_guess_latency"] = total_guess_latency
    results["total_guess_count"] = total_guess_count
    results["good_guess_bad_guess_ratio"] = total_good_guesses / \
        total_bad_guesses if total_bad_guesses > 0 else float('inf')
    results["win_rate"] = win_rate
    results["avg_tries"] = avg_tries
    results["avg_latency"] = avg_latency
    results["total_llm_calls"] = total_llm_calls
    results["avg_llm_calls_per_guess"] = avg_llm_calls_per_guess_overall

    with open(LOG_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n{'='*50}")
    print(f"FINAL RESULTS:")
    print(f"{'='*50}")
    print(f"Win Rate: {win_rate:.2%} ({total_success}/{NUM_RUNS})")
    print(f"Average Tries: {avg_tries:.2f}")
    print(f"Average Latency: {avg_latency:.2f}s")
    print(f"Total Bad Guesses: {total_bad_guesses}")
    print(f"Total Good Guesses: {total_good_guesses}")
    print(f"Total Guess Latency: {total_guess_latency:.2f}s")
    print(f"Total Guess Count: {total_guess_count}")
    if total_bad_guesses > 0:
        print(
            f"Good Guess Bad Guess Ratio: {total_good_guesses / total_bad_guesses:.2f}")
    else:
        print(
            f"Good Guess Bad Guess Ratio: {total_good_guesses} (no bad guesses)")
    print(f"Total LLM Calls: {total_llm_calls}")
    print(f"Total Good Guesses: {total_good_guesses}")
    print(
        f"Average LLM Calls per Guess: {avg_llm_calls_per_guess_overall:.2f}")
    print(f"{'='*50}")
    print(f"\nSaved benchmark results to {LOG_FILE}")


if __name__ == "__main__":
    wandb.init(
        project="llm-wordle-comp",
        name=f"{LLM_MODEL}-{MAX_LLM_CONTINUOUS_CALLS}-retries"
    )
    test_games()
