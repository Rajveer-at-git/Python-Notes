import pygame
from pygame.sprite import Sprite


class Raindrop(Sprite):
    """A class to represent a single raindrop."""

    def __init__(self, game, x=None, y=None):
        """Initialize the raindrop and set its starting position."""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        # Draw the raindrop as a thin rectangle (no image file needed!)
        self.image = pygame.Surface(
            (self.settings.drop_width, self.settings.drop_height),
            pygame.SRCALPHA
        )
        self.image.fill(self.settings.drop_color)
        self.rect = self.image.get_rect()

        # Position: use provided x/y or default to top-left
        self.rect.x = x if x is not None else self.rect.width
        self.rect.y = y if y is not None else self.rect.height

        # Store exact vertical position as float for smooth movement
        self.y = float(self.rect.y)

    def update(self):
        """Move the raindrop downward."""
        self.y += self.settings.drop_speed
        self.rect.y = self.y
