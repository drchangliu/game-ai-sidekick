from constants import *

def calculate_dynamic_widths(num_guesses: int):
    cell_width = (LETTER_GRID_HEIGHT - 2 * BORDER_OFFSET_Y -
                      (num_guesses - 1) * SPACE_BETWEEN_CELLS) / num_guesses
    border_offset_x = (LETTER_GRID_WIDTH - WORD_LENGTH *
                        cell_width - (WORD_LENGTH - 1) * SPACE_BETWEEN_CELLS) / 2
    
    return (cell_width, border_offset_x)