from enum import Enum

import pygame

from classes.AnimationObject import AnimationObject
from constants import *
from utils.calculate_dynamic_widths import calculate_dynamic_widths
from utils.visual_utils import draw_text


# enum to hold feedback values for LetterCells
class Feedback(Enum):
    incorrect = "incorrect"  # letter is not present in word
    present = "present"  # letter is present in the word, but in different spot
    correct = "correct"  # letter is in correct spot in the word


# Class to hold the information of every letter typed by user
class LetterCell(AnimationObject):
    def __init__(self, position: int):
        super().__init__()
        self.value: str | None = None
        self.position = position
        self.feedback: Feedback | None = None
        self.internal_feedback: Feedback | None = None

    def draw_cell(self, screen: pygame.Surface, verticlePos: int, num_guesses: int):
        # colors used to display LetterCells
        grey = (58, 58, 60)
        yellow = (181, 159, 59)
        green = (83, 141, 78)
        white = (255, 255, 255)

        cell_width, border_offset_x = calculate_dynamic_widths(num_guesses)

        y = self.update_animation_frame()
        # change border width and color of cell based on feedback
        border = int(cell_width / 23.3)
        color = grey
        if (self.feedback == Feedback.incorrect):
            border = 0
        elif (self.feedback == Feedback.present):
            border = 0
            color = yellow
        elif (self.feedback == Feedback.correct):
            border = 0
            color = green

        # conditional offsets used to render all cells to the screen
        x_offset = border_offset_x if self.position == 0 else SPACE_BETWEEN_CELLS
        y_offset = BORDER_OFFSET_Y if verticlePos == 0 else SPACE_BETWEEN_CELLS
        x_added_offset = 0 if self.position == 0 else x_offset * \
            self.position - (SPACE_BETWEEN_CELLS - border_offset_x)
        y_added_offset = 0 if verticlePos == 0 else y_offset * \
            verticlePos - (SPACE_BETWEEN_CELLS - BORDER_OFFSET_Y)
        x_pos = x_added_offset + x_offset + cell_width * self.position
        y_pos = y_added_offset + y_offset + cell_width * verticlePos
        x_pos_centered = x_pos + cell_width / 2
        y_pos_centered = y_pos + cell_width / 2

        # rectangle component to be rendered for each LetterCell
        cell_rect = pygame.Rect(x_pos, y_pos + y, cell_width, cell_width)

        pygame.draw.rect(screen, color, cell_rect,
                         border, 2)  # draw LetterCell

        # generate text to display the letters
        draw_text('Franklin Gothic', int(cell_width),
                  self.value if self.value else "",
                  (x_pos_centered, y_pos_centered + y - 1), white, screen)
