import pygame
from pygame.sprite import Sprite


class Scoreboard(Sprite):
    """Scoreboard for presenting game score"""

    def __init__(self, background_image_path, x, y, currency,
                 text_color_r, text_color_g, text_color_b, font_size, text_margin_right):
        """Initialize Scoreboard"""
        super(Scoreboard, self).__init__()
        self.background_image = pygame.image.load(background_image_path)
        self.rect = self.background_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.currency = currency
        self.text_color = (text_color_r, text_color_g, text_color_b)
        self.font = pygame.font.SysFont(None, font_size)
        self.score = 0.00
        self.text_margin_right = text_margin_right

    def draw(self, screen):
        """"Join score value and background and blit to the screen"""
        score_to_display = str("{:.2f}".format(self.score)) + self.currency
        score_value_image = self.font.render(score_to_display, True, self.text_color)
        score_rect = score_value_image.get_rect()
        score_rect.right = self.rect.right - self.text_margin_right
        score_rect.centery = self.rect.centery
        screen.blit(self.background_image, self.rect)
        screen.blit(score_value_image, score_rect)

    def update(self, screen, points_to_addition):
        """Add points to score and invoke _draw function"""
        self.score += points_to_addition
        self.draw(screen)
