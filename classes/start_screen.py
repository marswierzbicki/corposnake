import pygame
from pygame.locals import *
import sys

import classes.constants as constants
from classes.final_score import FinalScore


class StartScreen:
    """Start screen displayed before the game"""

    def __init__(self, screen, settings, game_screen):
        """Initialize start screen"""
        self.screen = screen
        self.game_screen = game_screen
        self.fps = settings['start_screen']['fps']
        self.curtain = self._create_curtain(screen, settings)
        self.first_run_images = self._load_images(settings, 'first_run_images')
        self.next_run_images = self._load_images(settings, 'next_run_images')
        self.running = True
        self.final_score = self._create_final_score(settings)

    def _create_final_score(self, settings):
        """Create FinalScore object"""
        return FinalScore(
            settings['start_screen']['final_score']['description'],
            settings['start_screen']['final_score']['currency'],
            settings['start_screen']['final_score']['y'],
            settings['start_screen']['final_score']['text_color_r'],
            settings['start_screen']['final_score']['text_color_g'],
            settings['start_screen']['final_score']['text_color_b'],
            settings['start_screen']['final_score']['font_size'])

    def _create_curtain(self, screen, settings):
        """Draw curtain (transparent)"""
        curtain_color_r = settings['start_screen']['curtain']['color_r']
        curtain_color_g = settings['start_screen']['curtain']['color_g']
        curtain_color_b = settings['start_screen']['curtain']['color_b']
        curtain_alpha = settings['start_screen']['curtain']['alpha']
        curtain_width, curtain_height = self.screen.get_size()
        curtain = pygame.Surface((curtain_width, curtain_height))
        curtain.fill((curtain_color_r, curtain_color_g, curtain_color_b))
        curtain.set_alpha(curtain_alpha)
        return curtain

    def _load_images(self, settings, key):
        """Load images (displayed in StartScreen) from setting file"""
        images = []
        for row in settings['start_screen'][key]:
            images.append(
                {"image": pygame.image.load(settings['start_screen'][key][row]['image_path']),
                 "x": settings['start_screen'][key][row]['x'],
                 "y": settings['start_screen'][key][row]['y']})
        return images

    def _check_input_events(self):
        """Check events and invoke proper action."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == pygame.K_s:
                    self.running = False

    def show_screen(self, score):
        """Check is it first run of the StartScreen and display it with proper configuration"""
        if score == constants.FIRST_RUN:
            self.game_screen.draw_board()
        self.screen.blit(self.curtain, (0, 0))
        if score == constants.FIRST_RUN:
            for image in self.first_run_images:
                self.screen.blit(image['image'], (image['x'], image['y']))
        else:
            for image in self.next_run_images:
                self.screen.blit(image['image'], (image['x'], image['y']))
                self.final_score.draw(self.screen, score)
        pygame.display.update()
        clock = pygame.time.Clock()
        while self.running:
            self._check_input_events()
            clock.tick(self.fps)
