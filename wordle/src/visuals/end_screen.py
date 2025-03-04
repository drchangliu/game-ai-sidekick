import pygame
from utils.visual_utils import draw_text
from constants import *


# draw end screen after game is over
def end_screen(screen: pygame.Surface, num_tries: int, num_guesses: int, actual_word: str, success: bool):
    green = (83, 141, 78)
    red = (255, 0, 0)
    grey = (58, 58, 60)
    white = (255, 255, 255)

    background_fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_fade.set_alpha(150)
    background_fade.fill(white)

    background_rect = pygame.Surface((BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
    background_rect.set_alpha(150)
    background_rect.fill(white)

    screen.blit(background_fade, (0, 0))
    screen.blit(background_rect, (SCREEN_WIDTH / 2 - BACKGROUND_WIDTH / 2,
                SCREEN_HEIGHT / 2 - BACKGROUND_HEIGHT / 2 - BACKGROUND_HEIGHT / 2))

    draw_text('Franklin Gothic', 100, actual_word, (BACKGROUND_WIDTH / 2 + 40,
                                                    (SCREEN_HEIGHT - BACKGROUND_HEIGHT) / 2 - BACKGROUND_HEIGHT / 2 + 60), green if success else red, screen)
    draw_text('Franklin Gothic', 40, f'{num_tries} / {num_guesses}' " Tries! Nice Job" if success else "Better Luck Next Time...",
              (BACKGROUND_WIDTH / 2 + 40, (SCREEN_HEIGHT - BACKGROUND_HEIGHT) / 2 - BACKGROUND_HEIGHT / 2 + 120), grey, screen)
    draw_text('Franklin Gothic', 40, "Press ENTER to play again", (BACKGROUND_WIDTH / 2 + 35,
                                                                   (SCREEN_HEIGHT - BACKGROUND_HEIGHT) / 2 - BACKGROUND_HEIGHT / 2 + 160), grey, screen)
    draw_text('Franklin Gothic', 40, "Press ESC to configure", (BACKGROUND_WIDTH / 2 + 35,
                                                                   (SCREEN_HEIGHT - BACKGROUND_HEIGHT) / 2 - BACKGROUND_HEIGHT / 2 + 200), grey, screen)
