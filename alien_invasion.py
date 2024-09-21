import sys
from time import sleep
import pygame 
from setting import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        
        # create an instance to store game stats
        self.stats = GameStats(self)
        
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        
        self.bullets = pygame.sprite.Group()
        
        self.aliens = pygame.sprite.Group()
        
        self.create_fleet()
        
        # start in an active state
        self.game_active = False
        
        # make the play button
        self.play_button = Button(self, "Play")
        
        

    def run_game(self):
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets() 
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)
            
    def _check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    
                elif event.type == pygame.KEYDOWN:
                    self.check_keydown_events(event)
                          
                elif event.type == pygame.KEYUP:
                    self.check_keyup_events(event)
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.check_play_button(mouse_pos)
                    
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet() 
        
        self.ship.blitime()
        self.aliens.draw(self.screen)
        
        self.sb.show_score()
        
        if not self.game_active:
            self.play_button.draw_button()
        
        pygame.display.flip()
        
    def check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
                        
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        
        elif event.key == pygame.K_q:
            sys.exit
        
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()
            
    def check_keyup_events(self, event): 
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
                            
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False



    def fire_bullet(self):
        # create a new bullet and add it to the bullets group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet  )
        

    def _update_bullets(self):
        # update position of bullets and get rid of bullets
        # updates the position of the bullet
        self.bullets.update()
        
            # removes old bullets 
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            # print(len(self.bullets))
            
        self.check_bullet_alien_collision()
        
        
    def check_bullet_alien_collision(self):    
            collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
            
            if collisions:
                for aliens in collisions.values():
                    self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()
            
            if not self.aliens:
                # destroy existing bullets and create new fleet
                self.bullets.empty()
                self.create_fleet()
                self.settings.increase_speed()
                
                self.stats.level += 1
                self.sb.prep_level()
                
    def create_fleet(self):
        # create a fleet of alien
        # make an alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 4 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self.create_alien(current_x, current_y)
                current_x += 2 * alien_width
                
            current_x = alien_width
            current_y += 2 * alien_height
    
    def create_alien(self, x_position, y_position):
        # create and alien and place it in the row
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
        
    
        
    def _update_aliens(self):
        # update teh position of the aliens
        self.check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit()
            
        self.check_alien_bottom()
        
    
    def check_fleet_edges(self):
        # resond appropriately if any aliens have reched the edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break
        
    def change_fleet_direction(self):
        # drop the entire fleet and change fleet's direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
    def ship_hit(self):
        #  respord to the ship being hit by an alien
        # decrement ships_left -= 1
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            
            self.sb.prep_ships()
            self.bullets.empty()
            self.aliens.empty()
            
            self.create_fleet()
            self.ship.center_ship()
            # pause
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
        
    def check_alien_bottom(self):
        # check if any aliens have reached the bottom of the screen
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # treat this the same as ship hit
                self.ship_hit()
                break
            
            
    def check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_setting()
            
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            
            self.game_active = True
            self.bullets.empty()
            self.aliens.empty()
                
            self.create_fleet()
            self.ship.center_ship()
            
            pygame.mouse.set_visible(False)
        
        
        
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()      