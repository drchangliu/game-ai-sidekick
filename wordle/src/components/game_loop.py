import pygame

from classes.GameState import GameState
from components.event_handler import *
from constants import DEFAULT_FRAMERATE
from visuals.end_screen import *


def game_loop(game: GameState):
    """! Starts the game and displays the current board
        @param GameState - a default game that has not been played yet 
        @return void - returns nothing - quits pygame
    """
    run = True  # holds game state

    # loop through the game, stop loop if quit detected
    while run:
        # draw main game board
        game.draw_board()

        # check for any events from user
        if handle_events(game):
            run = False

        # ensure proper framerate is set
        game.tick(DEFAULT_FRAMERATE)

    pygame.quit()
