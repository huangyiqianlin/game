import sys
from bullet import Bullet
import pygame
from alien import Alien


def check_event(ai_setting, screen, ship, bullets):
    """" 响应按键和鼠标事件 """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_event_key_down(event, ship, ai_setting, screen, bullets)
        elif event.type == pygame.KEYUP:
            check_event_key_up(event, ship)


def check_event_key_down(event, ship, ai_setting, screen, bullets):
    """ 键盘按下事件 """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_setting, screen, ship, bullets)


def check_event_key_up(event, ship):
    """ 键盘弹起事件 """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(ai_settings, screen, ship, bullets, aliens):
    """ 更新屏幕上的图像，并切换到新屏幕 """

    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    pygame.display.flip()


def update_bullets(bullets, aliens, ai_settings, screen, ship):
    """ 更新子弹的位置，并删除已经消失的子弹 """

    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    """ 响应子弹和外星人的碰撞 """

    # 删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, aliens)


def fire_bullet(ai_setting, screen, ship, bullets):
    """ 如果没有达到限制就发射一颗子弹 """

    if len(bullets) < ai_setting.bullet_allowed:
        new_bullet = Bullet(ai_setting, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """  计算每一行可以容纳多少个外星人 """
    available_spacex = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_spacex / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number):
    """ 创建一个外星人并放在当前行 """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    aliens.add(alien)


def create_fleet(ai_settings, screen, aliens):
    """ 创建外星人群 """

    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)

    # 创建一行外星人
    for alien_number in range(number_aliens_x):
        # 创建一个外星人并加入当前行
        create_alien(ai_settings, screen, aliens, alien_number)


def update_aliens(ai_settings, aliens, ship):
    """ 更新所有外星人的位置 """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        print('hit!!!!')


def check_fleet_edges(ai_settings, aliens):
    """ 有外星人到达边缘时采取相应的措施 """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """ 将整群外星人下移，并改变它们的方向 """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
