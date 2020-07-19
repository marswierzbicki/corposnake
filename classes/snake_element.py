import pygame
from pygame.sprite import Sprite
import classes.constants as constants


class SnakeElement(Sprite):
    """Single snake element containing stored by object snake"""

    def __init__(self, screen, step_length, step_images, step_number,
                 starting_position_x, starting_position_y, direction, steps_quantity):
        """Initialize Snake Element"""
        super(SnakeElement, self).__init__()
        self.screen = screen
        self.step_length = step_length
        self.step_images = step_images[:]
        self.step_number = step_number
        self.image = step_images[self.step_number]
        self.rect = self.image.get_rect()
        self.rect.x = starting_position_x
        self.rect.y = starting_position_y
        self.screen_rect = screen.get_rect()
        self.direction = direction
        self.steps_quantity = steps_quantity

    def _transfer_when_snake_is_out_of_the_screen(self):
        """When snake element came out of the screen bring it back to the opposite screen side"""
        if self.rect.top >= self.screen_rect.bottom:
            self.rect.y -= self.screen_rect.height + self.rect.height
        elif self.rect.bottom <= self.screen_rect.top:
            self.rect.y += self.screen_rect.height + self.rect.height
        elif self.rect.left >= self.screen_rect.right:
            self.rect.x -= self.screen_rect.width + self.rect.width
        elif self.rect.right <= self.screen_rect.left:
            self.rect.x += self.screen_rect.width + self.rect.width

    def update(self):
        """Update position of Snake Element on the game screen"""
        # Move and rotate Snake Element - image with Snake Element is always facing up so it should rotated
        if self.direction == constants.DIRECTION_UP:
            self.rect.y = self.rect.y - self.step_length
            transform_angle = 0
        elif self.direction == constants.DIRECTION_RIGHT:
            self.rect.x = self.rect.x + self.step_length
            transform_angle = -90
        elif self.direction == constants.DIRECTION_DOWN:
            self.rect.y = self.rect.y + self.step_length
            transform_angle = 180
        elif self.direction == constants.DIRECTION_LEFT:
            self.rect.x = self.rect.x - self.step_length
            transform_angle = 90
        # Change Snake Element image for animation effect
        if self.step_number == self.steps_quantity - 1:
            self.step_number = 0
        else:
            self.step_number += 1
        self.image = self.step_images[self.step_number]
        self.image = pygame.transform.rotate(self.image, transform_angle)
        self._transfer_when_snake_is_out_of_the_screen()

    def is_on_the_screen(self):
        """Check is snake element on the screen"""
        if (self.rect.top >= self.screen_rect.top
                and self.rect.bottom <= self.screen_rect.bottom
                and self.rect.right <= self.screen_rect.right
                and self.rect.left >= self.screen_rect.left):
            return True
        else:
            return False
