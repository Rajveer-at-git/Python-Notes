import sys

import pygame

from settings1 import Settings

class Blue_game:
    """Overall class for managing overall game assets and behavior."""

    def __init__(self):
        """Initialize the game and related resources"""
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Blue Game")

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            
            self._check_events()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        # Watch for keyboard and mouse movements
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

    def _update_screen(self):
        """Update images to the screen and flip to the new screen."""
        # Redraw the screen through each loop
        self.screen.fill(self.settings.bg_color)

        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    game = Blue_game()
    game.run_game()