"""
Exercise 13-4: Steady Rain
When a row disappears off the bottom, a new row appears at the top.
This creates a continuous, steady rain effect.
"""

import sys
import pygame

from settings import Settings
from raindrop import Raindrop


class SteadyRain:
    """Main class for Steady Rain (Exercise 13-4)."""

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Steady Rain - 13-4")

        self.raindrops = pygame.sprite.Group()

        # Track spacing so we know when to add a new row
        self.spacing_x = 40
        self.spacing_y = 60

        # y position where the next new row will be spawned (above screen top)
        # We'll track how far the topmost row has fallen
        self._next_row_y = -self.settings.drop_height  # starts just above screen

        self._create_initial_grid()

    def _create_initial_grid(self):
        """Fill the screen with the starting grid of raindrops."""
        cols = self.settings.screen_width // self.spacing_x
        rows = self.settings.screen_height // self.spacing_y

        for row in range(rows):
            y = row * self.spacing_y + self.settings.drop_height
            self._add_row(y)

        # Next new row should appear above the screen
        self._next_row_y = -self.settings.drop_height

    def _add_row(self, y):
        """Add a full horizontal row of raindrops at the given y position."""
        cols = self.settings.screen_width // self.spacing_x
        for col in range(cols):
            x = col * self.spacing_x + self.settings.drop_width
            drop = Raindrop(self, x=x, y=y)
            self.raindrops.add(drop)

    def _update_raindrops(self):
        """Move drops down, remove off-screen ones, add new rows at top."""
        self.raindrops.update()

        # Remove drops that have fallen off the bottom
        for drop in self.raindrops.copy():
            if drop.rect.top > self.settings.screen_height:
                self.raindrops.remove(drop)

        # Check if the highest remaining drop has fallen enough
        # that a gap of spacing_y has opened at the top
        if self.raindrops:
            # Find the topmost drop (smallest y value)
            highest_drop = min(self.raindrops.sprites(), key=lambda d: d.rect.y)

            # If the topmost drop has fallen one spacing_y below where new row should be
            if highest_drop.rect.y >= self._next_row_y + self.spacing_y:
                self._add_row(self._next_row_y)
                # Move the spawn point down for the NEXT future row
                self._next_row_y += self.spacing_y
                # Keep next_row_y cycling: once it goes on screen, reset above
                if self._next_row_y > 0:
                    self._next_row_y = -self.settings.drop_height
        else:
            # All drops gone, recreate everything
            self._next_row_y =- self.settings.drop_height
            self._create_initial_grid()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                # Speed up/slow down with UP/DOWN arrows
                elif event.key == pygame.K_UP:
                    self.settings.drop_speed += 0.5
                elif event.key == pygame.K_DOWN:
                    self.settings.drop_speed = max(0.5, self.settings.drop_speed - 0.5)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.raindrops.draw(self.screen)

        # Show speed on screen
        font = pygame.font.SysFont(None, 30)
        speed_text = font.render(
            f"Speed: {self.settings.drop_speed:.1f}  (UP/DOWN to change, Q to quit)",
            True, (180, 180, 180)
        )
        self.screen.blit(speed_text, (10, 10))

        pygame.display.flip()

    def run_game(self):
        while True:
            self._check_events()
            self._update_raindrops()
            self._update_screen()
            self.clock.tick(60)


if __name__ == '__main__':
    game = SteadyRain()
    game.run_game()
