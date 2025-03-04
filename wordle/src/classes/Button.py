import pygame

from utils.visual_utils import draw_text


# class to make buttons that are clickable
class Button:
    instances = []  # static variable to keep track of instances

    def __init__(self, rect: pygame.Rect, border: int, border_radius: int,
                 color: tuple[int, int, int], text: str, font_size: int, text_color: tuple[int, int, int]):
        self.rect = rect
        self.border = border
        self.border_radius = border_radius
        self.color = color
        self.text = text
        self.clicked = False
        self.font_size = font_size
        self.text_color = text_color
        self.disabled = False
        Button.instances.append(self)  # add new button to static list

    def __del__(self):
        Button.instances.remove(self)

    @staticmethod
    def update_cursor():
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw_button(self, screen: pygame.Surface):
        action = False
        pos = pygame.mouse.get_pos()

        # button is clicked
        if self.rect.collidepoint(pos):
            if not self.disabled:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True

        # reset click status
        if not pygame.mouse.get_pressed()[0]:
            if self.clicked:
                action = True

            self.clicked = False
        # draw button
        pygame.draw.rect(
            screen,
            self.color,
            self.rect,
            self.border,
            self.border_radius
        )
        # Prints the letters to the screen
        draw_text('Franklin Gothic', self.font_size, self.text, (self.rect.centerx,
                                                                 self.rect.centery), self.text_color, screen)

        return not self.disabled and action
