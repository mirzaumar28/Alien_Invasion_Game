class GameStats:
# track statistics for alien invasion
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        
        self.high_score = 0
     
    def reset_stats(self):
        # initialize stats thats can change during the game 
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
