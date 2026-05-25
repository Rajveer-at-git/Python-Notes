"""
Exercise 13-3: Raindrops
A grid of raindrops falls toward the bottom of the screen and disappears.
"""

import sys
import pygame

from settings import Settings
from raindrop import Raindrop


class RainGame:
    """Main class for the Raindrop game (Exercise 13-3)."""

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Raindrops - 13-3")

        self.raindrops = pygame.sprite.Group()
        self._create_grid()

    def _create_grid(self):
        """Create a full grid of raindrops filling the screen."""
        drop_width = self.settings.drop_width
        drop_height = self.settings.drop_height
        spacing_x = 40   # horizontal gap between drops
        spacing_y = 60   # vertical gap between rows

        # Figure out how many columns and rows fit
        cols = self.settings.screen_width // spacing_x
        rows = self.settings.screen_height // spacing_y

        for row in range(rows):
            for col in range(cols):
                x = col * spacing_x + drop_width
                y = row * spacing_y + drop_height
                drop = Raindrop(self, x=x, y=y)
                self.raindrops.add(drop)

    def _update_raindrops(self):
        """Move raindrops down and remove those that fall off screen."""
        self.raindrops.update()

        for drop in self.raindrops.copy():
            if drop.rect.top > self.settings.screen_height:
                self.raindrops.remove(drop)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.raindrops.draw(self.screen)
        pygame.display.flip()

    def run_game(self):
        while True:
            self._check_events()
            self._update_raindrops()
            self._update_screen()
            self.clock.tick(60)


if __name__ == '__main__':
    game = RainGame()
    game.run_game()
