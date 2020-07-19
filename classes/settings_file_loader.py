import json
import pygame


class SettingsFileLoader:
    """Read file with settings and implement it"""

    def implement_settings_for_main_screen(self, settings_file_path):
        """Read file with settings for main screen and implement it"""
        with open(settings_file_path, 'r') as settings_file:
            settings = json.load(settings_file)
            for row in settings:
                if settings[row]["type"] == "screen":
                    return self._set_main_window_properties(settings, row)

    def implement_settings_for_game_screen(self, settings_file_path, game_screen):
        """Read file with game settings and implement it"""
        with open(settings_file_path, 'r') as settings_file:
            settings = json.load(settings_file)
            for row in settings:
                if settings[row]["type"] == "main_game_settings":
                    self._set_game_main_properties(game_screen, settings, row)
                elif settings[row]["type"] == "scoreboard":
                    self._create_scoreboard(game_screen, settings, row)
                elif settings[row]["type"] == "obstacle":
                    self._create_obstacle(game_screen, settings, row)

    def _set_main_window_properties(self, settings, row):
        """Set main window properties"""
        return settings[row]["caption"], (settings[row]["width"], settings[row]["height"])

    def _set_game_main_properties(self, game_screen, settings, row):
        """Set game main properties"""
        game_screen.background_image = pygame.image.load(settings[row]["background_image_path"]).convert()
        game_screen.grid_size = settings[row]["grid_size"]
        game_screen.fps = settings[row]["fps"]

    def _create_scoreboard(self, game_screen, settings, row):
        """Create scoreboard in game screen"""
        game_screen.create_scoreboard(
            settings[row]["image_path"]
            , settings[row]["x"]
            , settings[row]["y"]
            , settings[row]["currency"]
            , settings[row]["text_color_r"]
            , settings[row]["text_color_g"]
            , settings[row]["text_color_b"]
            , settings[row]["font_size"]
            , settings[row]["text_margin_right"])

    def _create_obstacle(self, game_screen, settings, row):
        """Create obstacle in game screen"""
        game_screen.create_obstacle(
            settings[row]["x"]
            , settings[row]["y"]
            , settings[row]["image_path"])
