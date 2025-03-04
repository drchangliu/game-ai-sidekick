import random

from assets.guess_words import GUESS_WORDS
from classes.LetterCell import Feedback
from constants import WORD_LENGTH


class Solver:
    def __init__(self):
        self.possible_guesses = GUESS_WORDS
        self.starting_guess = "arise"
        self.possible_letters: list[str] = [
            "QWERTYUIOPASDFGHJKLZXCVBNM" for _ in range(WORD_LENGTH)
        ]
        self.present_letters = ""

    @staticmethod
    def filter_guesses(possible_guess: str, possible_letters: list[str], present_letters: str):
        for i in range(len(possible_guess)):
            if possible_guess[i] not in possible_letters[i]:
                return False

        for i in range(len(present_letters)):
            if present_letters[i] not in possible_guess:
                return False

        return True

    def reason_guess(self, guess: str):
        reasons = []
        guess = guess.upper()

        for i, guess_letter in enumerate(guess):
            if len(self.possible_letters[i]) == 1 and \
                    guess_letter not in self.possible_letters[i]:
                reasons.append(
                    ("SBC", guess_letter, self.possible_letters[i])
                )
            elif guess_letter not in self.possible_letters[i]:
                reasons.append(
                    ("NP", guess_letter, self.possible_letters[i])
                )

        for present_letter in self.present_letters:
            if present_letter not in guess:
                reasons.append(("SBP",  None, present_letter))

        return reasons

    def num_possible_guesses(self):
        return len(self.possible_guesses)

    def reset(self):
        self.possible_guesses = GUESS_WORDS
        self.possible_letters = [
            "QWERTYUIOPASDFGHJKLZXCVBNM" for _ in range(WORD_LENGTH)
        ]
        self.present_letters = ""

    def get_guess(self):
        if len(self.possible_guesses) > 0:
            if len(self.possible_guesses) == len(GUESS_WORDS):
                return self.starting_guess

            return random.choice(self.possible_guesses)

        raise Exception("No Possible Words")

    def update_guesses(self, word: str, feedback_list: list[Feedback]):
        for i in range(len(word)):
            match feedback_list[i]:
                case Feedback.correct:
                    self.possible_letters[i] = word[i]
                case Feedback.present:
                    self.possible_letters[i] = self.possible_letters[i].replace(
                        word[i].upper(), ""
                    )
                    if self.present_letters.find(word[i].upper()) == -1:
                        self.present_letters += word[i].upper()
                case Feedback.incorrect:
                    self.possible_letters[i] = self.possible_letters[i].replace(
                        word[i].upper(), ""
                    )
                    letters_present = False
                    for j in range(len(word)):
                        if word[i] == word[j] and feedback_list[j] == Feedback.present:
                            letters_present = True
                            break

                    if not letters_present:
                        for j in range(len(word)):
                            if word[j] != word[i]:
                                self.possible_letters[j] = self.possible_letters[j].replace(
                                    word[i].upper(), ""
                                )

        self.possible_guesses = list(filter(lambda x: self.filter_guesses(
            x.upper(), self.possible_letters, self.present_letters), self.possible_guesses)
        )
