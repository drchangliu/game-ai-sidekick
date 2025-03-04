import random
from collections import defaultdict
from threading import Timer

import pygame

from assets.valid_words import VALID_WORDS
from classes.LetterCell import Feedback, LetterCell
from constants import *


# Class to hold each line of letters typed by user
class Word:
    def __init__(self, actual_word: str, lie_indexes: list[int], position: int, disable_animation: bool = False):
        self.actual_word = actual_word.upper()
        self.guessed_word = ""
        self.word_length = len(actual_word)
        self.locked = False
        self.lie_indexes = lie_indexes
        self.position = position
        self.letters = [LetterCell(i) for i in range(self.word_length)]
        self.disable_animation = disable_animation

    def draw_word(self, screen: pygame.Surface, num_guesses: int):
        for letter in self.letters:
            letter.draw_cell(screen, self.position, num_guesses)

    def check_word(self):
        # function that is used to dispatch the feedback asynchronously
        def apply_feedback(letter: LetterCell, feedback: Feedback, internal_feedback: Feedback):
            letter.feedback = feedback
            letter.internal_feedback = internal_feedback
            if not self.disable_animation:
                letter.start_jump_animation(
                    ANIMATION_JUMP_HEIGHT, ANIMATION_DURATION
                )

        # create frequency map of letters from user inputted word
        freq_map = defaultdict(int)
        for letter in self.actual_word:
            freq_map[letter] += 1

        # loop through all user inputted letters and set feedback accordingly
        for i in range(self.word_length):
            letter = self.letters[i]
            internal_feedback: Feedback | None = None

            if freq_map[letter.value] > 0:
                # letter is in correct position
                if letter.value == self.actual_word[i]:
                    internal_feedback = Feedback.correct
                    freq_map[letter.value] -= 1
                else:
                    num_future_correct = 0

                    # check future positions for correctness to take precedence
                    for j in range(i + 1, self.word_length):
                        future_letter = self.letters[j]

                        if future_letter.value == self.actual_word[j] and future_letter.value == letter.value:
                            num_future_correct += 1

                    if freq_map[letter.value] > num_future_correct:  # letter is present
                        internal_feedback = Feedback.present
                        freq_map[letter.value] -= 1
                    else:  # letter is present, but correct for every letter to the right of it -> show incorrect
                        internal_feedback = Feedback.incorrect
            else:
                internal_feedback = Feedback.incorrect

            if i in self.lie_indexes:
                possible_feedbacks = [Feedback.incorrect,
                                      Feedback.present, Feedback.correct]
                possible_feedbacks.remove(internal_feedback)
                temp_feedback = random.choice(possible_feedbacks)
            else:
                temp_feedback = internal_feedback

            # create and run timer to dispatch feedback asynchronously
            delay = FEEDBACK_DIFF_DURATION / 1000 * i if not self.disable_animation else 0
            Timer(
                delay,
                apply_feedback, (letter, temp_feedback, internal_feedback)
            ).start()

    def length(self):
        """! Goes through and gets the length of the word
        @param self   The object self reference of type Word
        @return  int - Length of the current word being typed
        """
        num = 0
        for letter in self.letters:
            if letter.value != None:
                num += 1

        return num

    # return a list of feedback from guessed word
    def get_feedback(self):
        feeback: list[Feedback] = []

        for letter in self.letters:
            if letter.feedback:
                feeback.append(letter.feedback)

        return feeback

    # return a list of feedback from guessed word
    def get_internal_feedback(self):
        feeback: list[Feedback] = []

        for letter in self.letters:
            if letter.internal_feedback:
                feeback.append(letter.internal_feedback)

        return feeback

    def word_complete(self):
        """! Checks if the word is complete and correct
        @param self   The object self reference of type Word
        @return  boolean - True if word is complete and correct, False otherwise
        """

        return self.guessed_word == self.actual_word

    def handle_check_word(self):
        if self.locked:
            return False

        # check that word is in english dictionary
        if self.guessed_word.lower() in VALID_WORDS:
            self.check_word()
            self.locked = True

            return True

        # if word is complete but doesn't exist -> shake
        if self.length() == self.word_length:
            for letter in self.letters:
                letter.start_shaking_animation(
                    ANIMATION_SHAKE_HEIGHT, ANIMATION_DURATION, NUM_SHAKES
                )

        return False

    def add_letter(self, key_pressed: str):
        """! makes sure the length of the word is not too long and places it on the screen
        @param self   The object self reference of type Word
        @param key_pressed  The key that is pressed on the keyboard
        @return void
        """
        if self.length() < self.word_length and not self.locked:
            self.letters[self.length()].value = key_pressed.upper()
            self.guessed_word += key_pressed.upper()

    def delete_letter(self):
        if self.length() > 0 and not self.locked:
            self.letters[self.length() - 1].value = None
            self.guessed_word = self.guessed_word[0:len(self.guessed_word) - 1]
