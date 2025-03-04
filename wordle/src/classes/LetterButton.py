import pygame
from classes.Button import Button
from typing import Callable
from classes.LetterCell import Feedback
from constants import *


class LetterButton(Button):
    def __init__(self, row: int, col: int, letter: str, on_click: Callable[[str], None]):
        self.on_click = on_click
        self.feedback: Feedback | None = None
        x, y = self.find_pos(row, col)
        width = LETTER_BUTTON_WIDTH if row != 2 or (
            col != 7 and col != 8) else LETTER_BUTTON_WIDTH * 1.5 + LETTER_BUTTON_SPACING / 2
        rect = pygame.Rect(x, y, width, LETTER_BUTTON_WIDTH)
        font_size = 40 if row != 2 or not (col == 7 or col == 8) else 30

        super().__init__(rect, 0, 4, (58, 58, 60),
                         letter.upper(), font_size, (255, 255, 255))

    # helper function to get position of button based on row and col of keyboard
    @staticmethod
    def find_pos(row: int, col: int):
        if row == 1:  # second row
            initial_offset = (LETTER_BUTTON_WIDTH + LETTER_BUTTON_SPACING) / 2
        elif row == 2 and col != 8:  # third row and no enter
            initial_offset = (
                (LETTER_BUTTON_WIDTH + LETTER_BUTTON_SPACING) * 3 / 2
            )
        else:  # first row or enter
            initial_offset = 0

        if row == 2 and col == 8:  # enter key
            x_pos = LETTER_BUTTON_OFFSET_X
        else:  # every other key
            x_pos = LETTER_BUTTON_OFFSET_X + initial_offset + \
                (LETTER_BUTTON_WIDTH + LETTER_BUTTON_SPACING) * col

        y_pos = LETTER_GRID_HEIGHT + LETTER_BUTTON_OFFSET_Y_TOP + \
            (LETTER_BUTTON_WIDTH + LETTER_BUTTON_SPACING) * row

        return (x_pos, y_pos)

    def draw(self, screen: pygame.Surface):
        # colors to use
        grey = (58, 58, 60)
        light_grey = (129, 131, 132)
        yellow = (181, 159, 59)
        green = (83, 141, 78)

        # change color of cell based on feedback
        color = light_grey
        if (self.feedback == Feedback.incorrect):
            color = grey
        elif (self.feedback == Feedback.present):
            color = yellow
        elif (self.feedback == Feedback.correct):
            color = green

        self.color = color

        # draw button and call callback function if clicked
        if self.draw_button(screen):
            self.on_click(self.text)
