import pygame


def view_with_buttons(buttons):
    def decorator(func):
        buttons_list = buttons

        def wrapper(*args, **kwargs):

            kwargs['buttons'] = buttons_list
            result = func(*args, **kwargs)

            return result
        return wrapper
    return decorator


def draw_text(font_name: str, font_size: int, text: str,
              position: tuple[float, float], text_color: tuple[int, int, int], screen: pygame.Surface, centered=True):
    font = pygame.font.SysFont(font_name, font_size)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect()

    screen.blit(
        text_surface,
        (
            position[0] - text_rect.width / 2 if centered else position[0],
            position[1] - text_rect.height / 2 +
            int(font_size / 15) if centered else position[1]
        ),
    )
    return text_rect
