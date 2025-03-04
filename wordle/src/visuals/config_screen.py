import typing

import pygame

from classes.Button import Button
from constants import *
from utils.visual_utils import draw_text, view_with_buttons

if typing.TYPE_CHECKING:
    from classes.GameState import GameState


def generate_buttons():
    buttons: list[Button] = []
    total_width = SCREEN_WIDTH - 200
    cell_width = int((total_width - 4 * 8) / 6)

    for i in range(6):
        buttons.append(Button(pygame.Rect(
            100 + (cell_width + 8) * i,
            250, cell_width, cell_width
        ), 0, 3, (58, 58, 60), str(i), 65, (255, 255, 255)))

    for i in range(6, 10):
        buttons.append(Button(pygame.Rect(
            100 + (cell_width + 8) + (cell_width + 8) * (i - 6),
            425, cell_width, cell_width
        ), 0, 3, (58, 58, 60), str(i), 65, (255, 255, 255)))

    for i, llm in enumerate(["openai", "gemini"]):
        buttons.append(Button(pygame.Rect(
            100 + (total_width / 2 + 8) * i,
            600, total_width / 2 - 4, cell_width
        ), 0, 3, (58, 58, 60), llm.upper(), 65, (255, 255, 255)))

    buttons.append(Button(pygame.Rect(100, 700, total_width, 60),
                   0, 3, (83, 141, 78), "Play", 65, (255, 255, 255)))

    return buttons


@view_with_buttons(generate_buttons())
def config_screen(game: 'GameState', **kwargs):
    game.screen.fill((255, 255, 255))

    quit = False

    lie_buttons: list[Button] = kwargs['buttons'][0:6]
    guess_buttons: list[Button] = kwargs['buttons'][6:10]
    llm_buttons: list[Button] = kwargs['buttons'][10:12]
    play_button: Button = kwargs['buttons'][12]

    title = "CONFIG"
    total_width = SCREEN_WIDTH - 80
    cell_width = int((total_width - (len(title) - 1) * 8) / len(title))

    for i in range(len(title)):
        x = 40 + (cell_width + 8) * i
        y = 80

        pygame.draw.rect(game.screen, (83, 141, 78), pygame.Rect(
            x, y, cell_width, cell_width), 0, 3)
        draw_text('Franklin Gothic', 80,
                  title[i], (x + cell_width / 2, y + cell_width / 2), (255, 255, 255), game.screen)

    draw_text('Franklin Gothic', 65, 'Number of Lies',
              (SCREEN_WIDTH / 2, 200), (58, 58, 60), game.screen)
    draw_text('Franklin Gothic', 65, 'Number of Guesses',
              (SCREEN_WIDTH / 2, 375), (58, 58, 60), game.screen)
    draw_text('Franklin Gothic', 65, 'LLM Platform',
              (SCREEN_WIDTH / 2, 550), (58, 58, 60), game.screen)

    for button in lie_buttons:
        button.color = (181, 159, 59) if int(
            button.text) == game.num_lies else (58, 58, 60)
        if button.draw_button(game.screen):
            lies = int(button.text)
            pygame.display.set_caption(
                f"Wordle{'*' if lies > 0 else ''}{lies if lies != 0 else ''}")
            game.num_lies = lies

    for button in guess_buttons:
        button.color = (181, 159, 59) if int(
            button.text) == game.num_guesses else (58, 58, 60)
        if button.draw_button(game.screen):
            guesses = int(button.text)
            game.num_guesses = guesses

    for button in llm_buttons:
        button.color = (
            181, 159, 59) if button.text.lower() == game.llm_platform else (58, 58, 60)
        if button.draw_button(game.screen):
            llm_platform = button.text.lower()
            game.set_llm_platform(llm_platform)

    if play_button.draw_button(game.screen):
        quit = True

    return quit
