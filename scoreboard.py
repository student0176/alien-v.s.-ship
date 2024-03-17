import pygame
from pygame.sprite import Group

from ship import Ship

"""相當於儀表盤，即玩游戲時一眼看到的這些圖形、數字等等"""
class ScoreBoard():
    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        self.text_color = 30, 30, 30,
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()
        self.prep_top_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self): #初始化后一直是0，這個原來更新要顯示的數字
        rounded_score = round(self.stats.score, -1) #round指的是小數點后多少位，如果是-1，將按10，100等凑整數，這裏就是凑10
        score_str = "{:,}".format(rounded_score) #將1000變成1,000的小trick
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.ai_settings.bg_color)  # 文本轉化爲圖像存放于mag_image
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20  # 固定右邊距、上邊距
        self.score_rect.top = 20
    def prep_top_score(self):
        top_score = round(self.stats.top_score, -1) #round指的是小數點后多少位，如果是-1，將按10，100等凑整數，這裏就是凑10
        top_score_str = "{:,}".format(top_score) #將1000變成1,000的小trick
        self.top_score_image = self.font.render(top_score_str, True, self.text_color,
                                            self.ai_settings.bg_color)  # 文本轉化爲圖像存放于mag_image
        self.top_score_rect = self.top_score_image.get_rect()
        self.top_score_rect.centerx = self.screen_rect.centerx
        self.top_score_rect.top = self.screen_rect.top
    def prep_level(self):
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color,
                                                self.ai_settings.bg_color)  # 文本轉化爲圖像存放于mag_image
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.top_score_image, self.top_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)


    def prep_ships(self):
        self.ships = Group() #這裏爲什麽不能放到最前面？花了半個小時發現初始化這個class時候要跑一下這個函數，所以自帶兩個ship.而且還沒這麽容易，由於一開始是2個元素，但是碰撞后會加進來一個新的，這個新的坐標從最左邊算，所以三個alien重曡了！
        for ship_number in range(self.stats.ships_left - 1): #關於這裏的減1，假設有2條命，前面函數説明碰兩次結束游戲，所以上面畫的要少一個
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
