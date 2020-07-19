import pygame


class FinalScore:
    """Object for storing and displaying final score"""

    def __init__(self, description, currency, y, text_color_r, text_color_g, text_color_b, font_size):
        """Initialize FinalScore"""
        self.description = description
        self.currency = currency
        self.y = y
        self.text_color = (text_color_r, text_color_g, text_color_b)
        self.font_size = font_size
        self.font = pygame.font.SysFont(None, font_size)

    def draw(self, screen, score):
        """Draw final score in the screen"""
        score_to_display = self.description + ("{:.2f}".format(score)) + self.currency
        score_value_image = self.font.render(score_to_display, True, self.text_color)
        score_rect = score_value_image.get_rect()
        score_rect.y = self.y
        score_rect.centerx = screen.get_rect().centerx
        screen.blit(score_value_image, score_rect)
