
class Settings:
    """存儲游戲所有數據的class"""

    def __init__(self):
        self.screen_height = 800
        self.screen_width = 1200
        self.bg_color = (230,230,245)

        self.ship_limit = 3

        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        self.bullet_width = 30
        self.bullet_height = 15
        self.bullet_color = 60,60,80
        self.bullet_allowed = 3

        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        self.alien_score = 50

        self.speedup_scale = 1.1
        self.score_scale = 1.5
    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_score = int(self.alien_score * self.score_scale)

        # print(self.alien_score) #測試用，確保alien的分數在上升，游戲結束後下一輪復原

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.alien_score = 50
