import random

from pygame.sprite import Group
from pygame.sprite import Sprite

from classes.benefit import Benefit


class Benefits(Sprite):
    """All benefits displayed on the game screen"""

    def __init__(self, screen, background_image, prizes_settings_list, dangers_settings_list, danger_probability,
                 min_lifetime, max_lifetime, benefit_quantity):
        """Initialize main variables and objects for benefits management"""
        super(Benefits, self).__init__()
        self.screen = screen
        self.background_image = background_image
        self.prizes_settings_list = prizes_settings_list
        self.penalties_settings_list = dangers_settings_list
        self.penalty_probability = danger_probability
        self.min_lifetime = min_lifetime
        self.max_lifetime = max_lifetime
        self.benefit_quantity = benefit_quantity
        self.prizes_settings_quantity = len(self.prizes_settings_list)
        self.penalties_settings_quantity = len(self.penalties_settings_list)
        self.benefits = Group()

    def _kill_benefits_with_lifetime_runned_out(self):
        """Kill benefit if its lifetime run out"""
        for benefit in self.benefits:
            if benefit.update() == 0:
                benefit.kill()

    def _create_prize(self, benefit_lifetime, benefit_position_x, benefit_position_y):
        """Rand and create benefit"""
        chosen_prize = random.randint(0, self.prizes_settings_quantity - 1)
        self.benefits.add(Benefit(self.prizes_settings_list[chosen_prize]["image"],
                                  benefit_position_x,
                                  benefit_position_y,
                                  self.prizes_settings_list[chosen_prize]["price"],
                                  False,
                                  benefit_lifetime,
                                  False))

    def _create_penalty(self, benefit_lifetime, benefit_position_x, benefit_position_y):
        """Rand and create danger"""
        chosen_penalty = random.randint(0, self.penalties_settings_quantity - 1)
        self.benefits.add(Benefit(self.penalties_settings_list[chosen_penalty]["image"],
                                  benefit_position_x,
                                  benefit_position_y,
                                  True,
                                  self.penalties_settings_list[chosen_penalty]["speed"],
                                  benefit_lifetime,
                                  True))

    def update(self, free_space_grid):
        """Refresh benefits"""
        self.benefits.clear(self.screen, self.background_image)
        self._kill_benefits_with_lifetime_runned_out()
        # Check how many benefits exist. If too few create new.
        current_benefits_quantity = len(self.benefits)
        while current_benefits_quantity < self.benefit_quantity:
            # Choose free space on the floor for creation benefit
            free_space_grid_quantity = len(free_space_grid.sprites())
            if free_space_grid_quantity < self.benefit_quantity:
                break
            chosen_free_space_grid = random.randint(0, free_space_grid_quantity - 1)
            # Rand common properties for prizes and dangers
            benefit_lifetime = random.randint(self.min_lifetime, self.max_lifetime)
            chosen_free_space_tile = free_space_grid.sprites()[chosen_free_space_grid]
            benefit_position_x = chosen_free_space_tile.rect.x
            benefit_position_y = chosen_free_space_tile.rect.y
            chosen_free_space_tile.kill()
            # Create benefit
            if random.random() <= self.penalty_probability:
                self._create_penalty(benefit_lifetime, benefit_position_x, benefit_position_y)
            else:
                self._create_prize(benefit_lifetime, benefit_position_x, benefit_position_y)
            current_benefits_quantity += 1
        self.benefits.draw(self.screen)
