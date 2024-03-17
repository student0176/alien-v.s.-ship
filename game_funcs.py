import sys
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet


def check_events(ship, aliens, bullets,ai_settings,screen, play_button, stats,sb): #本來只是退出游戲，現在還要listen飛船移動，故多了個輸入參數
    for event in pygame.event.get():  # 監聽鼠標鍵盤
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(ship,bullets,event,ai_settings,screen)
        elif event.type == pygame.KEYUP:
            check_keyup_events(ship, event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(play_button, stats, mouse_x, mouse_y, ai_settings, screen, bullets, aliens, ship,sb)
def check_play_button(play_button, stats, mouse_x, mouse_y, ai_settings, screen, bullets, aliens, ship,sb):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active: #相當每局游戲的於初始化了
        pygame.mouse.set_visible(False)
        ai_settings.initialize_dynamic_settings()

        stats.reset_stats() #初始化ship和分數
        sb.prep_score()
        sb.prep_top_score()
        sb.prep_level()
        sb.prep_ships()

        stats.game_active = True

        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship_after_collide()

def check_keydown_events(ship,bullets,event,ai_settings,screen): #本來只是退出游戲，現在還要listen飛船移動，故多了個輸入參數
    if event.key == pygame.K_q:
        sys.exit()
    if event.key == pygame.K_RIGHT:
        ship.move_right = True
    if event.key == pygame.K_LEFT:
        ship.move_left = True
    if event.key == pygame.K_SPACE:
        fire_bullet(bullets,ai_settings,screen,ship)
def check_keyup_events(ship, event): #本來只是退出游戲，現在還要listen飛船移動，故多了個輸入參數
    if event.key == pygame.K_RIGHT:
        ship.move_right = False
    if event.key == pygame.K_LEFT:
        ship.move_left = False


def fire_bullet(bullets,ai_settings,screen,ship):
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
def update_bullets(bullets, ai_settings, screen, aliens, ship,stat,sb): # for循環中不應該改變在循環著的東西，所以操作副本。也可認爲是約定俗成
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.top <= 0:
            bullets.remove(bullet)
    # print(len(group)) #確認子彈在變少就注釋掉，畢竟將輸出寫入到終端而花費的時間比將圖形繪製到游戲窗口所需時間還
    check_bullet_alien_collisions(bullets, ai_settings, screen, aliens, ship, stat,sb)
def check_bullet_alien_collisions(bullets, ai_settings, screen, aliens,ship,stat,sb):
    collisions = pygame.sprite.groupcollide(bullets, aliens,False,True) #true的意思是重叠后要不要消失
    if collisions:
        for aliens in collisions.values():
            stat.score += ai_settings.alien_score * len(aliens) #這裏是每個子彈對應被它擊中的alien的列表
            sb.prep_score()
        check_high_score(stat,sb)

    if len(aliens) == 0:
        bullets.empty()

        stat.level += 1
        sb.prep_level()

        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, aliens,ship)

def check_high_score(stats,sb):
    if stats.score > stats.top_score:
        stats.top_score = stats.score
        sb.prep_top_score()
def get_number_aliens_x(ai_settings, alien_width):
    avaliable_space_x = ai_settings.screen_width - 2 * alien_width
    number_alien_x = int(avaliable_space_x / (2 * alien_width))
    return number_alien_x
def gey_number_rows(ai_settings, ship_height,alien_height, ):
    avaliable_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    number_rows = int(avaliable_space_y / (2 * alien_height))
    return  number_rows
def create_fleet(ai_settings, screen, aliens,ship):
    ship_height = ship.rect.height
    alien = Alien(ai_settings,screen) #工具外星人，不加入編組中，只是防止反復調用rect，用他得到數值
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien_col_num = get_number_aliens_x(ai_settings, alien_width)
    alien_row_num = gey_number_rows(ai_settings, ship_height,alien_height, )
    for j in range(alien_row_num):
        for i in range(alien_col_num):
            create_aliens(aliens, ai_settings,alien_width,alien_height, screen, i, j)
def create_aliens(aliens, ai_settings,alien_width,alien_height, screen, i, j):
    alien = Alien(ai_settings, screen)
    alien.x = alien_width + 2 * alien_width * i
    alien.y = alien_height + 2 * alien_height * j
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)

def check_fleet_edges(aliens, ai_settings):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(aliens,ai_settings)
            break #這個break確保只碰一下，可以注釋掉試試看。愚以爲要是注釋掉，那就是統計完所有外星人狀態后乘上1或-1，這就跟外星人數目有關（4*9個），所以是1。所以只要找到第一個碰到的就行了
def change_fleet_direction(aliens,ai_settings ):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_aliens(stats, ai_settings, screen, aliens, ship, bullets, sb):
    check_fleet_edges(aliens, ai_settings)
    aliens.update()
    check_alien_ship_collides(stats, ai_settings, screen, aliens, ship, bullets, sb)
    check_aliens_bottom(stats, ai_settings, screen, aliens, ship, bullets, sb)
def check_alien_ship_collides(stats, ai_settings, screen, aliens, ship, bullets, sb):
    if pygame.sprite.spritecollideany(ship, aliens):  # 注意這裏順序不能錯，前參人少，后參人多，否則報錯。
        ship_hit(stats, ai_settings, screen, aliens, ship, bullets, sb)
def check_aliens_bottom(stats, ai_settings, screen, aliens, ship, bullets, sb):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(stats, ai_settings, screen, aliens, ship, bullets, sb)
            break
def ship_hit(stats, ai_settings, screen, aliens, ship, bullets, sb):
    stats.ships_left -= 1
    sb.prep_ships()
    sb.show_score()
    if stats.ships_left > 0:
        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship_after_collide()

        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)



def update_screen(ai_settings,screen,ship,aliens,bullets,stats,sb,play_button): #畫屏幕畫船更新
    screen.fill(ai_settings.bg_color)

    for bullet in bullets.sprites(): #由bullet對象組成的列表
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()

    if not stats.game_active: #儅這個是false時候，按鈕就會出現
        play_button.draw_button()


    pygame.display.flip()  # 更新新屏幕




