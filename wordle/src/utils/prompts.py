from collections.abc import Iterable

from openai.types.chat import ChatCompletionMessageParam

from classes.LetterCell import Feedback
from constants import WORD_LENGTH

default_prompt: ChatCompletionMessageParam = {
    "role": "system",
    "content": f"You will guess a {WORD_LENGTH} letter word based off previous guesses "
    "and feedback in the form of correct: correct place, "
    "present: letter is present but not in correct spot, "
    "and incorrect: letter is not present in the word. "
    "There may be more than one lies, meaning one or more feedbacks will be incorrect."
    "Assume there are no lies unless otherwise stated."
    f"Respond with the {WORD_LENGTH} letter word and then the reason why you chose that word, nothing else!"
    "If no feedback is provided, you must guess the word without feedback."
    "You only have a certain amount of tries to get the word."
}


def generate_messages(guesses: list[str], feedback: list[list[Feedback]], num_lies: int, tries_left: int):
    if len(guesses) != len(feedback):
        raise ValueError(
            "Error: the number of guessess should equal the length of guess feedback.")

    messages: Iterable[ChatCompletionMessageParam] = []

    messages.append(default_prompt)

    if num_lies > 0:
        messages.append({
            "role": "user",
            "content": f"There are {num_lies} lies in this word."
        })

    for guess, fb in zip(guesses, feedback):
        feedback_strings = [
            f"{char}: {feedback_type.value}" for char, feedback_type in zip(guess, fb)
        ]
        feedback_content = "\n".join(feedback_strings)

        messages.append({
            "role": "user",
            "content": f"Guess: {guess}\nFeedback:\n{feedback_content}"
        })

    messages.append({
        "role": "user",
        "content": f"You have {tries_left} tries remaining."
    })

    return messages


def generate_guess_reasoning(reasons: list[tuple[str, str | None, str]]):
    reasoning = ""

    for reason in reasons:
        if reason[0] == "SBC":
            reasoning += f"'{reason[1]}' is not a possible letter for this spot, the valid letter should be: {reason[2]}\n"
        elif reason[0] == "NP":
            reasoning += f"'{reason[1]}' is not a possible letter for this spot, valid letters are: {reason[2]}\n"
        elif reason[0] == "SBP":
            reasoning += f"'{reason[2]}' must be in the word\n"

    return {
        "role": "system",
        "content": reasoning
    }
