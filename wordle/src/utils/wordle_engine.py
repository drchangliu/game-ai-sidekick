from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import List, Sequence, Tuple

from src.assets.guess_words import GUESS_WORDS


LEGAL_GUESSES = tuple(word.upper() for word in GUESS_WORDS)


@dataclass
class WordleState:
    answer: str
    rng: random.Random = field(default_factory=random.Random)
    guesses: List[str] = field(default_factory=list)
    feedback: List[str] = field(default_factory=list)
    max_turns: int = 6

    def record_turn(self, guess: str, feedback: str) -> None:
        self.guesses.append(guess)
        self.feedback.append(feedback)


def new_game(seed: int | None = None) -> WordleState:
    rng = random.Random(seed)
    answer = rng.choice(LEGAL_GUESSES)
    return WordleState(answer=answer, rng=rng)


def step(state: WordleState, guess: str) -> Tuple[WordleState, str]:
    guess = guess.upper()
    feedback = _evaluate_guess(state.answer, guess)
    state.record_turn(guess, feedback)
    return state, feedback


def is_solved(state: WordleState) -> bool:
    return bool(state.guesses) and state.guesses[-1] == state.answer


def legal_guesses() -> Sequence[str]:
    return LEGAL_GUESSES


def _evaluate_guess(answer: str, guess: str) -> str:
    greens = ["B"] * len(answer)
    remaining = list(answer)

    # First pass for greens.
    for idx, (g_char, a_char) in enumerate(zip(guess, answer)):
        if g_char == a_char:
            greens[idx] = "G"
            remaining[idx] = None

    # Second pass for yellows.
    for idx, g_char in enumerate(guess):
        if greens[idx] == "G":
            continue
        if g_char in remaining:
            greens[idx] = "Y"
            first_index = remaining.index(g_char)
            remaining[first_index] = None

    return "".join(greens)
