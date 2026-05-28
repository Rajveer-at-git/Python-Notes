class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = self._load_high_score()   # load instead of 0
    
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def _load_high_score(self):
        try:
            with open('high_score.txt', 'r') as f:
                return int(f.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        with open('high_score.txt', 'w') as f:
            f.write(str(self.high_score))