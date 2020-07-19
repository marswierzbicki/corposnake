import pygame
from pygame.sprite import Sprite


class FloorGridElement(Sprite):
    """A single floor grid element stored by object Floor Grid"""

    def __init__(self, position_x, position_y, grid_size):
        """Initialize floor grid element"""
        super(FloorGridElement, self).__init__()
        self.rect = pygame.Rect(position_x, position_y, grid_size, grid_size)
