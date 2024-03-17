import pygame.image
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen,):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('./images/ship.bmp') #返回一個surface對象
        self.rect = self.image.get_rect() #像處理rectangular一樣處理ship，這裏返回的rect對象有中心坐標、屏幕上下左右邊緣、矩形左上角xy坐標等屬性，記住這些，便免於計算煩惱
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)
        self.move_right = False
        self.move_left = False

    def blitme(self):
        self.screen.blit(self.image, self.rect) #將image繪製在screen的rect處

    def update(self):
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.move_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center #只能存整數，所以藉由中間變量凑個小數取整.然鵝這一步也讓我迷惑了一陣子，見readme

    def center_ship_after_collide(self):
        self.center = self.screen_rect.centerx