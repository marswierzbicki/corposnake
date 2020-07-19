import pygame
from pygame.sprite import Sprite


class Obstacle(Sprite):
    """Single obstacle in game screen."""

    def __init__(self, x, y, image_path):
        """Initialize obstacle"""
        super(Obstacle, self).__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
