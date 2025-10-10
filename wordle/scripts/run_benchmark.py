# Run with: python scripts/run_benchmark.py --games 10
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.llm.client import LocalLLMClient  # noqa: E402
from src.utils.wordle_engine import (  # noqa: E402
    WordleState,
    is_solved,
    legal_guesses,
    new_game,
    step,
)

SYSTEM_PROMPT = (
    "You are helping to solve Wordle. Reply with exactly one 5-letter uppercase word. "
    "Do not include punctuation, explanations, or extra words."
)
WORD_REGEX = re.compile(r"\b[A-Za-z]{5}\b")


def parse_args() -> argparse.Namespace:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Run a batch of Wordle games via a local LLM.")
    parser.add_argument(
        "--provider",
        default=os.getenv("LLM_PROVIDER", "ollama"),
        help="LLM provider name (default: env LLM_PROVIDER).",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("LLM_MODEL", "llama3.2:3b"),
        help="LLM model name (default: env LLM_MODEL).",
    )
    parser.add_argument(
        "--games",
        type=int,
        default=10,
        help="Number of Wordle games to simulate.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Base random seed for reproducibility.",
    )
    parser.add_argument(
        "--output-dir",
        default="logs",
        help="Directory for JSONL and CSV outputs (created if missing).",
    )
    return parser.parse_args()


def sanitize_for_path(value: str) -> str:
    clean = re.sub(r"[^A-Za-z0-9]+", "-", value)
    clean = clean.strip("-")
    return clean.lower() or "default"


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def build_user_prompt(history: List[Dict[str, Any]], turns_left: int) -> str:
    lines = []
    if history:
        lines.append("Previous guesses with feedback (G=correct, Y=present, B=absent):")
        for turn in history:
            lines.append(f"{turn['guess']} -> {turn['feedback']}")
    else:
        lines.append("This is the first guess.")
    lines.append(f"Turns remaining: {turns_left}")
    lines.append("Respond with one 5-letter uppercase word only; no commentary.")
    return "\n".join(lines)


def extract_guess(text: str) -> Optional[str]:
    if not text:
        return None
    match = WORD_REGEX.search(text.upper())
    return match.group(0) if match else None


def pick_fallback_guess(state: WordleState, legal_words: Sequence[str]) -> str:
    available = [word for word in legal_words if word not in state.guesses]
    if not available:
        available = list(legal_words)
    return state.rng.choice(available)


def resolve_guess(
    llm_output: Optional[str],
    state: WordleState,
    legal_set: set[str],
    legal_words: Sequence[str],
    error_message: Optional[str],
) -> Tuple[str, Optional[str], Optional[str]]:
    candidate = extract_guess(llm_output or "")
    reason: Optional[str] = None
    extracted = candidate

    if error_message:
        reason = f"llm_error: {error_message}"
        candidate = None

    if candidate:
        if candidate.upper() in legal_set:
            return candidate.upper(), reason, extracted
        reason = "invalid_llm_guess"

    guess = pick_fallback_guess(state, legal_words)
    return guess, reason, extracted


def play_single_game(
    client: LocalLLMClient,
    legal_words: Sequence[str],
    legal_set: set[str],
    base_rng: random.Random,
    base_seed: Optional[int],
    game_index: int,
) -> Dict[str, Any]:
    game_seed = base_rng.randint(0, 2**32 - 1) if base_seed is not None else None
    state = new_game(seed=game_seed)
    history: List[Dict[str, Any]] = []
    turn_logs: List[Dict[str, Any]] = []
    start_time = time.perf_counter()
    first_latency: Optional[float] = None

    for turn_idx in range(state.max_turns):
        turns_left = state.max_turns - turn_idx
        user_prompt = build_user_prompt(history, turns_left)
        llm_output = None
        latency = None
        error_message = None

        try:
            response = client.chat(SYSTEM_PROMPT, user_prompt)
            llm_output = response.get("text", "")
            latency = response.get("latency_s")
            if first_latency is None and latency is not None:
                first_latency = latency
        except Exception as exc:  # noqa: BLE001
            error_message = str(exc)
            if first_latency is None:
                first_latency = None

        guess, reason, extracted = resolve_guess(
            llm_output,
            state,
            legal_set,
            legal_words,
            error_message,
        )

        state, feedback = step(state, guess)
        history.append({"guess": guess, "feedback": feedback})

        turn_data: Dict[str, Any] = {
            "turn": turn_idx + 1,
            "guess": guess,
            "feedback": feedback,
            "turns_left_after": state.max_turns - len(state.guesses),
        }
        if llm_output is not None:
            turn_data["llm_output"] = llm_output
        if extracted:
            turn_data["extracted_candidate"] = extracted
        if latency is not None:
            turn_data["latency_s"] = latency
        if reason:
            turn_data["fallback_reason"] = reason
        if error_message:
            turn_data["llm_error"] = error_message

        turn_logs.append(turn_data)

        if is_solved(state):
            break

    duration = time.perf_counter() - start_time
    return {
        "game_index": game_index,
        "seed": game_seed,
        "answer": state.answer,
        "win": is_solved(state),
        "turns": len(state.guesses),
        "duration_s": duration,
        "first_token_latency_s": first_latency,
        "history": turn_logs,
    }


def run_benchmark(args: argparse.Namespace) -> Tuple[Path, Path]:
    output_dir = ensure_directory((ROOT_DIR / args.output_dir).resolve())
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    provider_safe = sanitize_for_path(args.provider)
    model_safe = sanitize_for_path(args.model)
    jsonl_path = output_dir / f"wordle_{provider_safe}_{model_safe}_{timestamp}.jsonl"
    csv_path = output_dir / f"wordle_{provider_safe}_{model_safe}_{timestamp}.csv"

    os.environ["LLM_PROVIDER"] = args.provider
    os.environ["LLM_MODEL"] = args.model

    legal_words = legal_guesses()
    legal_set = set(legal_words)

    client = LocalLLMClient()
    base_rng = random.Random(args.seed)

    records: List[Dict[str, Any]] = []
    durations: List[float] = []
    turns_taken: List[int] = []
    wins = 0

    for game_idx in tqdm(range(args.games), desc="Running Wordle games"):
        record = play_single_game(
            client,
            legal_words,
            legal_set,
            base_rng,
            args.seed,
            game_idx,
        )
        records.append(record)
        durations.append(record["duration_s"])
        turns_taken.append(record["turns"])
        if record["win"]:
            wins += 1

    with jsonl_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record))
            handle.write("\n")

    summary_row = {
        "provider": args.provider,
        "model": args.model,
        "games": args.games,
        "wins": wins,
        "win_rate_percent": round((wins / args.games) * 100, 2) if args.games else 0.0,
        "average_turns": sum(turns_taken) / len(turns_taken) if turns_taken else 0.0,
        "average_duration_s": sum(durations) / len(durations) if durations else 0.0,
    }
    pd.DataFrame([summary_row]).to_csv(csv_path, index=False)

    print(f"Saved JSONL log to: {jsonl_path}")
    print(f"Saved CSV summary to: {csv_path}")

    return jsonl_path, csv_path


def main() -> None:
    args = parse_args()
    run_benchmark(args)


if __name__ == "__main__":
    main()
