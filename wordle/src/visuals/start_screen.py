import pygame

from classes.Button import Button
from constants import *
from utils.visual_utils import draw_text, view_with_buttons

BACKGROUND_WIDTH = SCREEN_WIDTH - 2 * 40
BACKGROUND_HEIGHT = 200


def generate_buttons():
    buttons: list[Button] = []

    buttons.append(Button(pygame.Rect(
        SCREEN_WIDTH / 2 - (SCREEN_WIDTH - 80) /
        2, LETTER_GRID_HEIGHT - 140, SCREEN_WIDTH - 80, 40
    ), 0, 4, (58, 58, 60), "API Manual", 40, (255, 255, 255)))

    buttons.append(Button(pygame.Rect(
        SCREEN_WIDTH / 2 - (SCREEN_WIDTH - 80) /
        2, LETTER_GRID_HEIGHT - 90, SCREEN_WIDTH - 80, 40
    ), 0, 4, (58, 58, 60), "Configure", 40, (255, 255, 255)))

    buttons.append(Button(pygame.Rect(
        SCREEN_WIDTH / 2 - (SCREEN_WIDTH - 80) /
        2, LETTER_GRID_HEIGHT - 40, SCREEN_WIDTH - 80, 40
    ), 0, 4, (83, 141, 78), "Play", 40, (255, 255, 255)))

    return buttons


@view_with_buttons(generate_buttons())
def start_screen(screen: pygame.Surface, **kwargs):
    font_size = 55
    tile_margin = 7
    tile_size = ((SCREEN_WIDTH - tile_margin * 10) / 6,
                 font_size)
    letters = "WORDLE"

    white = (255, 255, 255)
    goTo = 0
    man_button: Button = kwargs['buttons'][0]
    config_button: Button = kwargs['buttons'][1]
    start_button: Button = kwargs['buttons'][2]

    # Calculate the total width of the "WORDLE" text
    total_width = (tile_size[0] * len(letters)) + \
        (tile_margin * (len(letters) - 1))
    # Start so that "WORDLE" is centered
    start_x = (SCREEN_WIDTH - total_width) / 2

    screen.fill(white)

    for i, letter in enumerate(letters):
        position = (start_x + (tile_size[0] + tile_margin)
                    * i, (SCREEN_HEIGHT - tile_size[1]) / 3)
        # Pass `screen` as an argument to `draw_tile`
        draw_tile(screen, position, letter)

    draw_text('Franklin Gothic', 45, "Guess the 5 letter word!", (BACKGROUND_WIDTH / 2 + 40,
                                                                  (SCREEN_HEIGHT - BACKGROUND_HEIGHT) / 2 - BACKGROUND_HEIGHT / 2 + 200), (58, 58, 60), screen)

    if man_button.draw_button(screen):
        goTo = 1

    if config_button.draw_button(screen):
        goTo = 2

    if start_button.draw_button(screen):
        goTo = 3

    return goTo


def draw_tile(screen: pygame.Surface, position, letter):
    font_size = 55
    tile_margin = 7  # Margin between tiles
    tile_size = ((SCREEN_WIDTH - tile_margin * 10) / 6,
                 font_size)  # Dynamically calculate size
    font = pygame.font.SysFont(None, font_size)
    tile_color = (83, 141, 78)  # Dark gray
    text_color = (255, 255, 255)  # White
    tile_size = ((SCREEN_WIDTH - tile_margin * 10) / 6,
                 font_size)  # Dynamically calculate size

    # Draw the tile
    tile_rect = pygame.Rect(
        position[0], position[1], tile_size[0], tile_size[1])
    pygame.draw.rect(screen, tile_color, tile_rect)

    # Render the letter text
    text_surf = font.render(letter, True, text_color)
    text_rect = text_surf.get_rect(center=tile_rect.center)
    screen.blit(text_surf, text_rect)
