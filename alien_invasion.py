import pygame
from pygame.sprite import Group

import game_funcs as gf
from button import Button
from game_stats import GameStates
from scoreboard import ScoreBoard

from settings import Settings
from ship import Ship

def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height)) #是一個屏幕對象，會變化
    pygame.display.set_caption(('外星人入侵'))
    play_button = Button(ai_settings, screen, "Play")

    ship = Ship(ai_settings,screen) #要是放到loop裏面，每次循環創建一個ship
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, aliens, ship)

    stats = GameStates(ai_settings)
    sb = ScoreBoard(ai_settings, screen, stats)

    while True:

        gf.check_events(ship, aliens, bullets,ai_settings,screen, play_button, stats,sb)

        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets, ai_settings, screen, aliens,ship,stats,sb)
            gf.update_aliens(stats, ai_settings, screen, aliens, ship, bullets, sb)

        gf.update_screen(ai_settings,screen,ship,aliens,bullets,stats, sb, play_button)



run_game()