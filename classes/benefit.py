from pygame.sprite import Sprite


class Benefit(Sprite):
    """A single Benefit stored by object Benefits"""

    def __init__(self, image, position_x, position_y, price, speed_multiplier, lifetime, is_penalty):
        """Initialize Benefit"""
        super(Benefit, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = position_x
        self.rect.y = position_y
        self.price = price
        self.speed_multiplier = speed_multiplier
        self.lifetime = lifetime
        self.is_penalty = is_penalty

    def update(self):
        """Decrease Benefit lifetime"""
        self.lifetime -= 1
        return self.lifetime
