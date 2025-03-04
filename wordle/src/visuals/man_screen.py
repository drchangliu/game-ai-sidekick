import pygame

from classes.Button import Button
from constants import SCREEN_WIDTH
from utils.visual_utils import draw_text
from utils.visual_utils import view_with_buttons

cmds = [
    "******* Use terminal to input commands *******",
    "new-game",
    "guess <word>",
    "config lies <number>",
    "config guesses <number>",
    "<Ctrl + C> to exit"
]


def generate_buttons():
    buttons: list[Button] = []
    total_width = SCREEN_WIDTH - 200

    buttons.append(Button(pygame.Rect(100, 700, total_width, 60),
                   0, 3, (83, 141, 78), "Back", 65, (255, 255, 255)))

    return buttons


@view_with_buttons(generate_buttons())
def man_screen(screen: pygame.Surface, **kwargs):
    screen.fill((255, 255, 255))

    back_button: Button = kwargs['buttons'][0]

    title = "COMMANDS"
    total_width = SCREEN_WIDTH - 80
    cell_width = int((total_width - (len(title) - 1) * 8) / len(title))

    for i, letter in enumerate(title):
        x = 40 + (cell_width + 8) * i
        y = 80

        pygame.draw.rect(screen, (83, 141, 78), pygame.Rect(
            x, y, cell_width, cell_width), 0, 3)
        draw_text('Franklin Gothic', 80,
                  letter, (x + cell_width / 2, y + cell_width / 2), (255, 255, 255), screen)

    # draw commands
    for i, cmd in enumerate(cmds):
        if i == 0:
            draw_text('Franklin Gothic', 30, cmd, (SCREEN_WIDTH / 2, 200), (0, 0, 0), screen)
        else:
            draw_text('Franklin Gothic', 30, cmd, (40, 200 + 40 * i), (0, 0, 0), screen, False)

    if back_button.draw_button(screen):
        return True

    return False
