# Empty objects needed for ErrorScreen
debug_mode = 0
screen = None

# Try pygame import necessary for visual windows of applications
try:
    import pygame
except ImportError as e:
    print(e)
    exit()

# Main error handling
try:
    import json
    import traceback
    from classes.game_screen import GameScreen
    from classes.start_screen import StartScreen
    from classes.error_screen import ErrorScreen
    import classes.constants as constants

    # Load application settings
    SETTINGS_FILE_PATH = 'settings/settings.json'
    settings = json.load(open(SETTINGS_FILE_PATH, 'r'))

    # Initialize application
    screen_caption = settings['corposnake']['screen']['caption']
    screen_size = (settings['corposnake']['screen']['width'], settings['corposnake']['screen']['height'])
    debug_mode = settings['debug']['mode']

    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption(screen_caption)

    # Application main loop
    score = constants.FIRST_RUN
    while True:
        game_screen = GameScreen(screen, settings)
        start_screen = StartScreen(screen, settings, game_screen)
        start_screen.show_screen(score)
        score = game_screen.play_game()
except SystemExit:
	pass
except:
    if debug_mode == 1:
        traceback.print_exc()
    else:
        error_screen = ErrorScreen(screen)
