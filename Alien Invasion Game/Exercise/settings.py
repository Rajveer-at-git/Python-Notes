class Settings:
    """A class to store all settings for the Raindrop game."""

    def __init__(self):
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (15, 25, 40)  # dark night-sky blue

        # Raindrop settings
        self.drop_speed = 2.0
        self.drop_width = 3
        self.drop_height = 15
        self.drop_color = (100, 180, 255)  # light blue
