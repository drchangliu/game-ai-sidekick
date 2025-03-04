import os
import random
import re
import threading
from enum import Enum
from threading import Timer

import pygame
from firebase_admin.firestore import firestore
from google import genai
from openai import OpenAI, OpenAIError
from openai.types.chat import ChatCompletionMessageParam

from assets.guess_words import GUESS_WORDS
from classes.Button import Button
from classes.LetterButton import LetterButton
from classes.LetterCell import Feedback
from classes.Solver import Solver
from classes.Word import Word
from constants import *
from firebase import add_retries, get_db, initialize_firebase
from utils.calculate_dynamic_widths import calculate_dynamic_widths
from utils.prompts import generate_guess_reasoning, generate_messages
from visuals.config_screen import config_screen
from visuals.end_screen import end_screen
from visuals.man_screen import man_screen
from visuals.start_screen import *


class Status(Enum):
    start = 0
    config = 1
    man = 2
    game = 3
    end = 4


# class to hold the game state
class GameState:
    def __init__(self, show_window: bool = True, disable_animations: bool = False, logging: bool = True):
        self.db: firestore.Client | None = None

        if logging:
            try:
                initialize_firebase()
                self.db = get_db()
                print("Firebase logging initialized")
            except:
                print("Error initializing Firebase")
        else:
            print("Firebase logging disabled")

        self.show_window = show_window
        self.disable_animations = not show_window or disable_animations
        self.screen: pygame.Surface | None = None
        self.clock: pygame.time.Clock | None = None
        self.num_guesses = 6
        self.num_lies = 0
        self.lie_indexes: list[int] = []
        self.actual_word = random.choice(GUESS_WORDS).upper()
        self.word_length = len(self.actual_word)
        self.words = [
            Word(
                self.actual_word,
                self.lie_indexes,
                i,
                self.disable_animations
            ) for i in range(self.num_guesses)
        ]

        self.status = Status.start
        self.success = False
        self.current_word_index = 0
        self.was_valid_guess = False

        self.llm_platform = LLM_PLATFORM
        self.ai_client: OpenAI | None = None
        if self.llm_platform == "openai":
            try:
                self.ai_client = OpenAI()
                self.api_key_valid = True
            except OpenAIError:
                self.api_key_valid = False

        self.gemini_client: genai.Client | None = None
        if self.llm_platform == "gemini":
            try:
                self.gemini_client = genai.Client(
                    api_key=os.getenv("GEMINI_API_KEY", default="")
                )
                self.api_key_valid = True
            except:
                self.api_key_valid = False

        self.game_retries = 0
        self.ai_loading = False
        self.error_message = ""
        self.error_message_visible = False

        self.solver = Solver()
        self.solver_active = False

        self.keyboard: list[list[LetterButton]] | None = None
        self.solve_button: Button | None = None
        self.hint_button: Button | None = None
        self.llm_hint_button: Button | None = None

        if self.show_window:
            pygame.init()
            self.screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.clock = pygame.time.Clock()
            pygame.display.set_caption('Wordle')
            self.keyboard = [
                [LetterButton(i, j, LETTERS[i][j], self.pick_callbacks(
                    i, j)) for j in range(len(LETTERS[i]))]
                for i in range(len(LETTERS))
            ]
            border_offset_x = calculate_dynamic_widths(self.num_guesses)[1]
            self.solve_button = Button(pygame.Rect(
                border_offset_x, LETTER_GRID_HEIGHT + 40,
                (LETTER_GRID_WIDTH - border_offset_x * 2) / 2 - 2, 40
            ), 0, 4, (83, 141, 78), "GIVE UP", 40, (255, 255, 255))
            self.hint_button = Button(pygame.Rect(
                border_offset_x + (LETTER_GRID_WIDTH -
                                   border_offset_x * 2) / 2 + 3, LETTER_GRID_HEIGHT + 40,
                (LETTER_GRID_WIDTH - border_offset_x * 2) / 4 - 3, 40
            ), 0, 4, (83, 141, 78), "HINT", 40, (255, 255, 255))
            bg = (83, 141, 78) if self.api_key_valid else (100, 100, 100)
            tc = (255, 255, 255) if self.api_key_valid else (200, 200, 200)
            self.llm_hint_button = Button(pygame.Rect(
                3 * LETTER_GRID_WIDTH / 4 - border_offset_x / 2 + 5, LETTER_GRID_HEIGHT + 40,
                (LETTER_GRID_WIDTH - border_offset_x * 2) / 4 - 3, 40
            ), 0, 4, bg, "LLM", 40, tc)

    def reset(self):
        if self.show_window:
            # make sure buttons are in correct position
            border_offset_x = calculate_dynamic_widths(self.num_guesses)[1]
            self.solve_button.rect = pygame.Rect(
                border_offset_x, LETTER_GRID_HEIGHT + 40,
                (LETTER_GRID_WIDTH - border_offset_x * 2) / 2 - 2, 40
            )
            self.hint_button.rect = pygame.Rect(
                border_offset_x + (LETTER_GRID_WIDTH -
                                   border_offset_x * 2) / 2 + 3, LETTER_GRID_HEIGHT + 40,
                (LETTER_GRID_WIDTH - border_offset_x * 2) / 4 - 3, 40
            )
            bg = (83, 141, 78) if self.api_key_valid else (100, 100, 100)
            tc = (255, 255, 255) if self.api_key_valid else (200, 200, 200)
            self.llm_hint_button.rect = pygame.Rect(
                3 * LETTER_GRID_WIDTH / 4 - border_offset_x / 2 + 5, LETTER_GRID_HEIGHT + 40,
                (LETTER_GRID_WIDTH - border_offset_x * 2) / 4 - 3, 40
            )
            self.llm_hint_button.color = bg
            self.llm_hint_button.text_color = tc

            for row in self.keyboard:
                for button in row:
                    button.feedback = None

        possible_positions = [i for i in range(WORD_LENGTH)]
        self.lie_indexes.clear()
        for _ in range(self.num_lies):
            index = random.choice(possible_positions)
            self.lie_indexes.append(index)
            possible_positions.remove(index)

        self.status = Status.game
        self.success = False
        self.current_word_index = 0
        self.was_valid_guess = False
        self.actual_word = random.choice(GUESS_WORDS).upper()
        self.words = [
            Word(
                self.actual_word,
                self.lie_indexes,
                i,
                self.disable_animations
            ) for i in range(self.num_guesses)
        ]

        self.game_retries = 0
        self.solver_active = False
        self.solver.reset()

    # helper function to set the correct callback function for each key

    def pick_callbacks(self, row: int, col: int):
        def handle_add_letter(letter: str):
            self.add_letter(letter)

        def handle_enter(_: str):
            self.handle_check_word()

        def handle_backspace(_: str):
            self.delete_letter()

        if row == 2:  # third row
            if col == 7:  # backspace key
                return handle_backspace

            elif col == 8:  # enter key
                return handle_enter

        # every other key
        return handle_add_letter

    def enter_word_from_solver(self, overload_guess: str | None = None, check: bool = True):
        guess = overload_guess or self.solver.get_guess()
        self.clear_guess()

        for letter in guess:
            self.add_letter(letter)

        if check:
            self.handle_check_word()

    def enter_single_guess_from_solver(self, overload_guess: str | None = None, check: bool = True):
        guess = overload_guess or self.solver.get_guess()
        self.clear_guess()

        letters_to_add = (
            WORD_LENGTH if self.solver.num_possible_guesses(
            ) > MIN_NUM_GUESSES or guess.upper() != self.actual_word else MIN_LETTERS_TO_ADD
        )
        for i in range(letters_to_add):
            self.add_letter(guess[i].upper())

        if letters_to_add == WORD_LENGTH and check:
            self.handle_check_word()

    def enter_word_from_ai(self, messages: list[ChatCompletionMessageParam] | None = None, calls: int = 0):
        self.ai_loading = True

        try:
            messages = messages or generate_messages(
                [word.guessed_word for word in self.words if word.locked],
                [word.get_feedback()
                 for word in self.words if word.locked],
                self.num_lies,
                self.num_guesses - self.num_of_tries()
            )
            org_response = ""

            if LOG_LLM_MESSAGES:
                with open("./llm_chat_log.txt", "a") as f:
                    f.write(str(messages) + "\n")
                    f.close()

            if self.llm_platform == "gemini":
                if not self.gemini_client:
                    return

                contents = "\n".join(map(
                    lambda message: message["content"], messages))
                completion = self.gemini_client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=contents
                )
                org_response = completion.text

            elif self.llm_platform == "openai":
                if not self.ai_client:
                    return

                completion = self.ai_client.chat.completions.create(
                    model=LLM_MODEL,
                    messages=messages,
                )
                org_response = str(
                    completion.choices[0].message.content
                )

            if LOG_LLM_MESSAGES:
                with open("./llm_chat_log.txt", "a") as f:
                    f.write("{" + org_response + "}" + "\n")
                    f.close()

            response = org_response.replace("Guess: ", "")
            response = re.search(r'\b\w{5}\b', response)
            if response:
                completion_message = response.group(0)
            else:
                completion_message = ""

            if len(completion_message) == WORD_LENGTH:
                reasons = self.solver.reason_guess(completion_message)

                if len(reasons) > 0 and calls < MAX_LLM_CONTINUOUS_CALLS and self.num_lies == 0:
                    self.game_retries += 1
                    messages.append(generate_guess_reasoning(reasons))
                    self.enter_word_from_ai(messages, calls + 1)
                else:
                    print(org_response)
                    self.enter_word_from_solver(
                        completion_message, check=(not self.show_window))
            else:
                self.was_valid_guess = False
                print("Error: AI did not return a valid guess")

        except Exception as e:
            self.error_message = str(e)
            self.error_message_visible = True
            Timer(ERROR_MESSAGE_VISIBLE_TIME, lambda: setattr(
                self, "error_message_visible", False)).start()
            if self.show_window:
                print(e)
            else:
                raise e

        self.ai_loading = False

    def set_llm_platform(self, llm: str):
        self.llm_platform = llm
        try:
            if llm == "openai":
                self.ai_client = OpenAI()
                self.api_key_valid = True
            elif llm == "gemini":
                self.gemini_client = genai.Client(
                    api_key=os.getenv("GEMINI_API_KEY", default="")
                )
                self.api_key_valid = True
        except:
            self.api_key_valid = False

    def clear_guess(self):
        for _ in range(WORD_LENGTH):
            self.delete_letter()

    # function to set keyboard feedback from last word feedback
    def apply_keyboard_feedback(self, word: str, feedback: list[Feedback]):
        if not self.show_window:
            return

        if self.num_lies > 0:
            return

        for i in range(len(word)):
            letter = word[i]

            for j in range(len(self.keyboard)):
                for k in range(len(self.keyboard[j])):
                    if self.keyboard[j][k].text == letter:
                        button = self.keyboard[j][k]

                        if i in self.lie_indexes:
                            button.feedback = feedback[i]

                        elif button.feedback == Feedback.present and feedback[i] == Feedback.correct:
                            button.feedback = Feedback.correct

                        elif button.feedback == Feedback.incorrect or button.feedback == None:
                            button.feedback = feedback[i]

    def tick(self, framerate: int):
        if self.show_window:
            self.clock.tick(framerate)

    def draw_board(self):
        if not self.show_window:
            return

        Button.update_cursor()

        match self.status:
            case Status.start:
                goTo = start_screen(self.screen)

                match goTo:
                    case 1:
                        self.status = Status.man
                    case 2:
                        self.status = Status.config
                    case 3:
                        self.reset()

            case Status.config:
                clicked = config_screen(self)

                if clicked:
                    self.reset()

            case Status.man:
                if man_screen(self.screen):
                    self.status = Status.start

            # game and end status
            case _:
                if self.status != Status.game and self.status != Status.end:
                    return

                self.screen.fill((18, 18, 19))

                for word in self.words:
                    word.draw_word(self.screen, self.num_guesses)

                for row in self.keyboard:
                    for button in row:
                        button.draw(self.screen)

                text = f'Beware the {str(self.num_lies) + " lies" if self.num_lies != 1 else "lie"}...'\
                    if self.num_lies > 0 else f'Guess the {WORD_LENGTH} letter word.'

                draw_text('Franklin Gothic', 40, text,
                          (LETTER_GRID_WIDTH / 2, LETTER_GRID_HEIGHT + 15), (58, 58, 60), self.screen)

                if self.solve_button.draw_button(self.screen):
                    self.solver_active = True
                    self.enter_word_from_solver()

                if self.hint_button.draw_button(self.screen):
                    self.enter_single_guess_from_solver(
                        check=(not self.show_window))

                if self.llm_hint_button.draw_button(self.screen):
                    threading.Thread(
                        target=(lambda game: game.enter_word_from_ai()), args=(self,)
                    ).start()

                if self.ai_loading:
                    draw_text('Franklin Gothic', 80, "Loading...",
                              (LETTER_GRID_WIDTH / 2, LETTER_GRID_HEIGHT / 2), (255, 255, 255), self.screen)

                if self.error_message_visible:
                    draw_text('Franklin Gothic', 20, self.error_message,
                              (LETTER_GRID_WIDTH / 2, LETTER_GRID_HEIGHT / 2 + 50), (255, 0, 0), self.screen)

                # Needed inside game because end_screen is on top of game board
                if self.status == Status.end:
                    end_screen(self.screen, self.num_of_tries(),
                               self.num_guesses, self.actual_word, self.success)

        pygame.display.update()

        # disable keyboard buttons if game is over
        for row in self.keyboard:
            for button in row:
                # disable button if game is over
                button.disabled = self.status != Status.game

        # disable button if game is over
        self.solve_button.disabled = self.status != Status.game

        # disable button if game is over
        self.hint_button.disabled = self.status != Status.game

        # disable button if game is over or api key is not valid
        self.llm_hint_button.disabled = (
            self.status != Status.game or not self.api_key_valid or self.ai_loading
        )

    def num_of_tries(self):
        return len([word for word in self.words if word.locked])

    def handle_check_word(self):
        self.error_message_visible = False

        # function to check word after time
        def check_correct():
            current_word = self.words[self.current_word_index]
            word_feedback = current_word.get_feedback()
            internal_word_feedback = current_word.get_internal_feedback()

            self.solver.update_guesses(
                current_word.guessed_word, internal_word_feedback)
            self.apply_keyboard_feedback(
                current_word.guessed_word, word_feedback
            )

            if self.words[self.current_word_index].word_complete():
                if self.game_retries != 0 and self.db:
                    threading.Thread(
                        target=add_retries, args=(self.db, self.game_retries)
                    ).start()
                self.success = True
                self.status = Status.end

            elif self.num_of_tries() == self.num_guesses:
                if self.game_retries != 0 and self.db:
                    threading.Thread(
                        target=add_retries, args=(self.db, self.game_retries)
                    ).start()
                self.status = Status.end

            else:
                self.current_word_index += 1

                if self.solver_active:
                    self.enter_word_from_solver()

        if self.words[self.current_word_index].handle_check_word():
            self.was_valid_guess = True
            delay = (FEEDBACK_DIFF_DURATION * 4 +
                     ANIMATION_DURATION) / 1000 if not self.disable_animations else 0
            Timer(
                delay, check_correct
            ).start()
        else:
            self.was_valid_guess = False

    def add_letter(self, key_pressed: str):
        self.words[self.current_word_index].add_letter(key_pressed)

    def delete_letter(self):
        self.words[self.current_word_index].delete_letter()
