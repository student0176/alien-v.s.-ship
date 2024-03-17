import pygame.font
"""此文件用於收集游戲過程中的數據，但是不在init裏面，而是在reset裏面，init初始化時候調用它。
   爲何？因爲一局游戲要這個class一個足矣，init裏面是實例化時候調用的，沒必要，放在reset中方便改動。所以這裏就儅這個class是一個存儲的容器就行了"""

class GameStates():
    def __init__(self, ai_settings):
        self.top_score = 0 #任何情況下都不能重置最高記錄，所以初始化時候就寫定下來

        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit #剩餘ship數
        self.score = 0
        self.level = 1

