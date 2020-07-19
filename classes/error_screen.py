import pygame
import sys


class ErrorScreen:
    """Screen with error message"""

    def __init__(self, screen):
        """Initialize start screen"""
        # Main properties are hardcoded for avoid errors caused by settings parsing
        background_color = (0, 47, 84)
        text_color = (255, 255, 255)
        fps = 2
        message_text = 'There is an error. Sorry :('
        font_size = 60
        screen_size = (960, 600)
        screen_caption = ':('
        self._show_screen(screen, background_color, text_color, fps, message_text, font_size, screen_size,
                          screen_caption)

    def _check_input_events(self):
        """Check events and invoke proper action."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _show_screen(self, screen, background_color, text_color, fps, message_text, font_size, screen_size,
                     screen_caption):
        """Display screen with error and wait for user action"""
        if screen is None:
            pygame.init()
            screen = pygame.display.set_mode(screen_size)
            pygame.display.set_caption(screen_caption)

        font = pygame.font.SysFont(None, font_size)
        screen.fill(background_color)
        message_image = font.render(message_text, True, text_color)
        message_rect = message_image.get_rect()
        message_rect.centery = screen.get_rect().centery
        message_rect.centerx = screen.get_rect().centerx
        screen.blit(message_image, message_rect)
        pygame.display.update()
        clock = pygame.time.Clock()
        while True:
            self._check_input_events()
            clock.tick(fps)
