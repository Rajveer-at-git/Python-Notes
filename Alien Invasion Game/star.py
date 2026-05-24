import pygame
from pygame.sprite import Sprite
from random import randint

class Star(Sprite):
    """A class to represent a single star in the background."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        screen_rect = ai_game.screen.get_rect()

        # Create a small rect for the star
        size = randint(2, 5)
        self.rect = pygame.Rect(0, 0, size, size)

        # Place it at a random position on screen
        self.rect.x = randint(0, screen_rect.width)
        self.rect.y = randint(0, screen_rect.height)

        # Random brightness (white-ish)
        brightness = randint(150, 255)
        self.color = (brightness, brightness, brightness)

    def draw_star(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)