import random

from pygame.sprite import Group
from pygame.sprite import Sprite

import classes.constants as constants
from classes.snake_element import SnakeElement


class Snake(Sprite):
    """Snake consisting of snake elements"""

    def __init__(self, screen, background_image, step_length, grid_size, starting_position_x, starting_position_y,
                 direction, step_images_sets):
        """Initialize snake"""
        super(Snake, self).__init__()
        self.screen = screen
        self.background_image = background_image
        self.step_length = step_length
        self.grid_size = grid_size
        self.step_counter = 0
        self.step_images_sets = step_images_sets
        self.step_images_sets_quantity = len(self.step_images_sets)
        self.direction = direction
        self.steps_quantity = len(self.step_images_sets[0])
        self.new_direction_flag = []
        self.add_body_element_flag = False
        self.snake_head = None
        # Used for checking collision between snake head and another snake elements.
        # Without the second snake element - because of constraint caused by snake turning equal 90 grades.
        self.snake_body = Group()
        # All snake elements used for refreshing animation
        self.all_snake = Group()
        # Used for moving each snake element in proper order
        self.all_snake_list = []
        self._create_head(starting_position_x, starting_position_y)

    def _create_head(self, starting_position_x, starting_position_y):
        """Create snake head"""
        self.snake_head = SnakeElement(self.screen, self.step_length, self._rand_element_skin(), 0,
                                       starting_position_x, starting_position_y, self.direction,
                                       self.steps_quantity)
        self.all_snake.add(self.snake_head)
        self.all_snake_list.append(self.snake_head)

    def _rand_element_skin(self):
        """Rand layout for snake element"""
        return self.step_images_sets[random.randint(0, self.step_images_sets_quantity - 1)]

    def _add_body_element(self):
        """Add new snake element to the snake."""
        last_element = self.all_snake_list[-1]
        last_element_position_x = last_element.rect.x
        last_element_position_y = last_element.rect.y
        last_element_direction = last_element.direction
        last_element_step_number = last_element.step_number
        if last_element_direction == constants.DIRECTION_UP:
            new_element_position_x = last_element_position_x
            new_element_position_y = last_element_position_y + self.grid_size
        elif last_element_direction == constants.DIRECTION_RIGHT:
            new_element_position_x = last_element_position_x - self.grid_size
            new_element_position_y = last_element_position_y
        elif last_element_direction == constants.DIRECTION_DOWN:
            new_element_position_x = last_element_position_x
            new_element_position_y = last_element_position_y - self.grid_size
        elif last_element_direction == constants.DIRECTION_LEFT:
            new_element_position_x = last_element_position_x + self.grid_size
            new_element_position_y = last_element_position_y
        new_element = SnakeElement(self.screen, self.step_length, self._rand_element_skin(), last_element_step_number,
                                   new_element_position_x, new_element_position_y, last_element_direction,
                                   self.steps_quantity)
        self.all_snake.add(new_element)
        self.all_snake_list.append(new_element)
        if len(self.all_snake_list) > 2:
            self.snake_body.add(new_element)

    def increase_body(self):
        """Set flag for snake body incrementation which will be executed during snake update"""
        self.add_body_element_flag = True

    def change_direction(self, new_direction):
        """Set flag for changing snake direction which will be executed during snake update"""
        new_direction_flag_count = len(self.new_direction_flag)
        # Check is new direction allowed
        # Compare with current direction or with direction waiting for implementation in new_direction_flag (stack)
        if (new_direction != self.direction and
                ((new_direction_flag_count == 0
                  and new_direction + self.direction != 0)
                 or (new_direction_flag_count == 1
                     and new_direction + self.new_direction_flag[0] != 0))):
            self.new_direction_flag.append(new_direction)

    def update(self):
        """Update snake - move body and implement changes from previously settled flags"""
        # Apply changes from flags if snake is in the proper position.
        # Changes are constrained by grid size used for floor space management)
        if self.step_counter % self.grid_size == 0:
            # Increase snake body
            if self.add_body_element_flag:
                self._add_body_element()
                self.add_body_element_flag = False
            # Change snake direction
            if (len(self.new_direction_flag) > 0
                    and self.snake_head.is_on_the_screen()):
                self.direction = self.new_direction_flag.pop(0)
            previous_element_direction = self.direction
            for snake_element in self.all_snake_list:
                new_direction = previous_element_direction
                previous_element_direction = snake_element.direction
                snake_element.direction = new_direction
            self.step_counter = 0
        self.all_snake.update()
        self.step_counter += self.step_length

    def draw(self):
        """Draw snake"""
        self.all_snake.clear(self.screen, self.background_image)
        self.all_snake.draw(self.screen)
