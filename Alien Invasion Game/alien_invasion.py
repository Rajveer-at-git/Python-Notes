import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class for managing overall game assets and behavior."""
 
    def __init__(self):
        """Initialize the game and related resources"""
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()  

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        # Group is like a list in pygame, which allows different images/structures to move
        # simultaneously without looping through every object separately
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()   
        


    def run_game(self):
        """Start the main loop for the game"""
        while True:
            
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        # Watch for keyboard and mouse movements
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                
                

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Move the ship to the left
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            # created shortcut for quitting the game by pressing q.
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
                """Update the position of bullets and get rid of old bullets."""
                # Update bullet positions.
                self.bullets.update()

                # Get rid of the bullets that have disappeared.
                for bullet in self.bullets.copy():
                    if bullet.rect.bottom < 0:
                        self.bullets.remove(bullet)

    def _create_fleet(self):
        """ Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left
        # Spacing between aliens is one alien width
        # Make an alien.
        alien = Alien(self)
        alien_width = alien.rect.width

        current_x = alien_width
        while current_x < (self.settings.screen_width - 2 * alien_width):
            new_alien = Alien(self)
            new_alien.x = current_x
            new_alien.rect.x = current_x
            self.aliens.add(new_alien)
            current_x += 2 * alien_width

    def _update_screen(self):
        """Update images to the screen and flip to the new screen."""
        # Redraw the screen through each loop
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Make the most recently drawn screen visible.
        pygame.display.flip()



if __name__ == '__main__':
    # Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()
