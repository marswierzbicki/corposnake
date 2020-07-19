import pygame
from pygame.sprite import Group
from pygame.locals import *
import classes.constants as constants
import sys

from classes.scoreboard import Scoreboard
from classes.obstacle import Obstacle
from classes.snake import Snake
from classes.floor_grid import FloorGrid
from classes.benefits import Benefits


class GameScreen:
    """Main screen with the game"""

    def __init__(self, screen, settings):
        """Game main properties and objects"""
        self.running = True
        self.background_image = pygame.image.load(
            settings['game_screen']['main_game_settings']['background_image_path']).convert()
        self.grid_size = settings['game_screen']['main_game_settings']['grid_size']
        self.fps = settings['game_screen']['main_game_settings']['fps']
        self.screen = screen
        self.scoreboard = Scoreboard(
            settings['game_screen']['scoreboard']['image_path'],
            settings['game_screen']['scoreboard']['x'],
            settings['game_screen']['scoreboard']['y'],
            settings['game_screen']['scoreboard']['currency'],
            settings['game_screen']['scoreboard']['text_color_r'],
            settings['game_screen']['scoreboard']['text_color_g'],
            settings['game_screen']['scoreboard']['text_color_b'],
            settings['game_screen']['scoreboard']['font_size'],
            settings['game_screen']['scoreboard']['text_margin_right'])
        self.benefits = self._create_benefits(settings)
        self.obstacles = Group()
        self._create_obstacles(settings)
        self.floor_grid = FloorGrid(self.screen, self.grid_size, self.obstacles, self.scoreboard)
        self.snake = self._create_snake(settings)

    def _create_snake(self, settings):
        """Create snake from settings"""
        # Create list with snake elements images for animation
        step_images_sets = []
        for row_element in settings['game_screen']['snake']['snake_elements']:
            steps_for_element = []
            for row_step in settings['game_screen']['snake']['snake_elements'][row_element]:
                steps_for_element.append(
                    pygame.image.load(settings['game_screen']['snake']['snake_elements'][row_element][row_step]))
            step_images_sets.append(steps_for_element)

        # Translate starting snake direction from settings to game constants
        if settings['game_screen']['snake']['direction'] == "up":
            direction = constants.DIRECTION_UP
        elif settings['game_screen']['snake']['direction'] == "right":
            direction = constants.DIRECTION_RIGHT
        elif settings['game_screen']['snake']['direction'] == "down":
            direction = constants.DIRECTION_DOWN
        elif settings['game_screen']['snake']['direction'] == "left":
            direction = constants.DIRECTION_LEFT

        return Snake(
            self.screen,
            self.background_image,
            settings['game_screen']['snake']['step_length'],
            self.grid_size,
            settings['game_screen']['snake']['starting_position_x'],
            settings['game_screen']['snake']['starting_position_y'],
            direction,
            step_images_sets
        )

    def _create_benefits(self, settings):
        """Create benefits from settings"""
        prizes_settings_list = []
        penalties_settings_list = []
        for row in settings['game_screen']['benefits']['prizes_list']:
            prizes_settings_list.append(
                {"image": pygame.image.load(settings['game_screen']['benefits']['prizes_list'][row]['image']),
                 "price": settings['game_screen']['benefits']['prizes_list'][row]['price']})
        for row in settings['game_screen']['benefits']['penalties_list']:
            penalties_settings_list.append(
                {"image": pygame.image.load(settings['game_screen']['benefits']['penalties_list'][row]['image']),
                 "speed": settings['game_screen']['benefits']['penalties_list'][row]['speed']})
        return Benefits(
            self.screen,
            self.background_image,
            prizes_settings_list,
            penalties_settings_list,
            settings['game_screen']['benefits']['penalty_probability'],
            settings['game_screen']['benefits']['min_lifetime'],
            settings['game_screen']['benefits']['max_lifetime'],
            settings['game_screen']['benefits']['benefit_quantity'], )

    def _create_obstacles(self, settings):
        """Create obstacle from settings and add to obstacles group"""
        for row in settings['game_screen']['obstacles']:
            obstacle = Obstacle(
                settings['game_screen']['obstacles'][row]['x'],
                settings['game_screen']['obstacles'][row]['y'],
                settings['game_screen']['obstacles'][row]['image_path'])
            self.obstacles.add(obstacle)

    def _check_input_events(self):
        """Check key down events and invoke proper action.
        Constants like DIRECTION_LEFT contain numbers used by Snake
        for arithmetic checking is this direction change allowed."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.snake.change_direction(constants.DIRECTION_LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction(constants.DIRECTION_RIGHT)
                elif event.key == pygame.K_UP:
                    self.snake.change_direction(constants.DIRECTION_UP)
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction(constants.DIRECTION_DOWN)

    def _check_snake_head_collisions(self):
        """Check collisions between snake head and other object and invoke proper action"""
        # snake_body
        if len(pygame.sprite.spritecollide(self.snake.snake_head, self.snake.snake_body, False)) > 0:
            self.running = False
        # obstacles
        if len(pygame.sprite.spritecollide(self.snake.snake_head, self.obstacles, False)) > 0:
            self.running = False
        # benefits
        for benefit in pygame.sprite.spritecollide(self.snake.snake_head, self.benefits.benefits, True):
            if benefit.is_penalty:
                self.fps *= benefit.speed_multiplier
            else:
                self.scoreboard.update(self.screen, benefit.price)
                self.snake.increase_body()

    def draw_board(self):
        """Draw board"""
        self.screen.blit(self.background_image, [0, 0])
        self.obstacles.draw(self.screen)
        self.scoreboard.draw(self.screen)

    def play_game(self):
        """Main game loop"""
        clock = pygame.time.Clock()

        self.draw_board()

        while self.running:
            self.snake.draw()
            pygame.display.update()

            self._check_input_events()

            self.snake.update()

            free_space_grid = self.floor_grid.get_free_space_grid(self.snake.all_snake, self.benefits.benefits)
            self.benefits.update(free_space_grid)

            self._check_snake_head_collisions()

            clock.tick(self.fps)
        return self.scoreboard.score
