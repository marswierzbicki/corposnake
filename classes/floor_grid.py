import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group

from classes.floor_grid_element import FloorGridElement


class FloorGrid(Sprite):
    """Grid with free space for placing benefits"""

    def __init__(self, screen, grid_size, obstacles, scoreboard):
        """Initialize floor grid"""
        super(FloorGrid, self).__init__()
        self.grid = Group()
        self._create_basic_grid(screen, grid_size)
        self._remove_obstacles_from_grid(obstacles, scoreboard)

    def _create_basic_grid(self, screen, grid_size):
        """Create grid covering all floor"""
        x_i = 0
        y_i = 0
        screen_rect = screen.get_rect()
        while x_i <= screen_rect.width:
            while y_i <= screen_rect.height:
                self.grid.add(FloorGridElement(x_i, y_i, grid_size))
                y_i += grid_size
            y_i = 0
            x_i += grid_size

    def _remove_obstacles_from_grid(self, obstacles, scoreboard):
        """Clear obstacles from floor grid with free space"""
        for obstacle in obstacles:
            pygame.sprite.spritecollide(obstacle, self.grid, True)
        pygame.sprite.spritecollide(scoreboard, self.grid, True)

    def get_free_space_grid(self, snake, benefits):
        """Remove current position of snake and benefits from floor grid free space"""
        free_space_grid = self.grid.copy()
        for snake_element in snake:
            for grid_element in pygame.sprite.spritecollide(snake_element, free_space_grid, False):
                grid_element.remove(free_space_grid)
        for benefit in benefits:
            for grid_element in pygame.sprite.spritecollide(benefit, free_space_grid, False):
                grid_element.remove(free_space_grid)
        return free_space_grid
