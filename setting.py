class Settings:
    """ A class to store all the settings for the game"""
    def __init__(self):
        # screen settings
        self.screen_height = 700
        self.screen_width = 1200
        self.bg_color = (230, 230, 230)
        
        # ship speed
        
        self.ship_limit = 3
        
        # bullet speed
        
        self.bullet_width = 500
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 20
        
        # alien setttings
        
        self.fleet_drop_speed = 20
        # fleet direction 1 represents right and -1 respresents left
        
        
        self.speedup_scale = 1.5
        self.score_scale = 1.5
        
        self.alien_points = 50
        
        self.initialize_dynamic_setting()
        
    def initialize_dynamic_setting(self):
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0 
        self.fleet_direction = 1
        
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        # print(self.alien_points)
        