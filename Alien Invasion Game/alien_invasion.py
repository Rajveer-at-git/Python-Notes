import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import Game_Stats
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star

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

        # Create instance to store game statistics.
        self.stats = Game_Stats(self)

        self.stars = pygame.sprite.Group()
        self._create_starfield()
        self.ship = Ship(self)
        # Group is like a list in pygame, which allows different images/structures to move
        # simultaneously without looping through every object separately
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.game_active = True
        self._create_fleet()   
        


    def run_game(self):
        """Start the main loop for the game"""
        while True:
            
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _create_starfield(self):
        """Scatter stars randomly across the background."""
        for _ in range(100):  # tweak number to your liking
            star = Star(self)
            self.stars.add(star)

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

        self._check_alien_bullet_collisions()

    def _check_alien_bullet_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove the bullets that have collided.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for any alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for the aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

        if not self.aliens:
            # Destroy the existing bullets and create a new fleet.
            self.bullets.empty()
            self._create_fleet()


    def _create_fleet(self):
        """ Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left
        # Spacing between aliens is one alien width and one alien height
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 5 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            
            # Finished a row; reset x value, increment y value
            current_x = alien_width
            current_y += 1.5 * alien_height

    def _check_fleet_edges(self):
        """Respond appropriately if an alien hits the edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""    
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _ship_hit(self):
        """Respond to the ship hit by the alien."""
        if self.stats.ships_left > 0:
            # Decrement ships left
            self.stats.ships_left -= 1

            # Get rid of any remaining bullets or aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and recenter the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause the game
            sleep(0.5)

        else:
            self.game_active = False

    def _check_aliens_bottom(self):
        """Check if any alien had reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this same as the ship got hit
                self._ship_hit()
                break

    def _update_screen(self):
        """Update images to the screen and flip to the new screen."""
        # Redraw the screen through each loop
        self.screen.fill(self.settings.bg_color)

        # Draw stars behind everything
        for star in self.stars.sprites():
            star.draw_star(self.screen)

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
