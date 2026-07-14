import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button

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

        # Create instance to store game statistics
        # and crate a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.stars = pygame.sprite.Group()
        self._create_starfield()
        self.ship = Ship(self)
        # Group is like a list in pygame, which allows different images/structures to move
        # simultaneously without looping through every object separately
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.game_active = False
        self._create_fleet()

        # Make the play button
        self.play_button = Button(self, "Play")   


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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)       

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Move the ship to the left
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self.stats.save_high_score()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            if not self.game_active:
                self._start_game()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks play button."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos) 
        if button_clicked and not self.game_active:
            self._start_game()            

    def _start_game(self):
        # Reset the game statistics.
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self.game_active = True

        # Get rid of any remaining bullets and aliens.
        self.bullets.empty()
        self.aliens.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

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

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.start_new_level()


    def start_new_level(self):
            """Increase the level."""
            self.stats.level += 1
            self.sb.prep_level()


    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for any alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for the aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

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
            # Decrement ships_left, and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()

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
            pygame.mouse.set_visible(True)

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

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()



if __name__ == '__main__':
    # Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()
