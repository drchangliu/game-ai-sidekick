import pygame

from classes.GameState import GameState, Status


def handle_events(game: GameState):
    if not game.show_window:
        return False

    # check all events posted by pygame
    for event in pygame.event.get():

        # return true if quit event detected
        if event.type == pygame.QUIT:
            return True

        # check keystrokes
        elif event.type == pygame.KEYDOWN:
            key_pressed: str = event.unicode.upper()
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if game.status == Status.end:
                    game.reset()
                elif game.status == Status.game:
                    game.handle_check_word()
            elif event.key == pygame.K_ESCAPE \
                    and (game.status == Status.game
                         or game.status == Status.end):
                game.status = Status.config
            elif event.key == pygame.K_BACKSPACE:
                game.delete_letter()
            elif key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and key_pressed != "":
                game.add_letter(key_pressed)

    return False
