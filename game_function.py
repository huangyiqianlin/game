import sys
from bullet import Bullet
import pygame


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


def update_screen(ai_settings, screen, ship, bullets):
    """ 更新屏幕上的图像，并切换到新屏幕 """

    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    pygame.display.flip()


def update_bullets(bullets):
    """ 更新子弹的位置，并删除已经消失的子弹 """

    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def fire_bullet(ai_setting, screen, ship, bullets):
    """ 如果没有达到限制就发射一颗子弹 """

    if len(bullets) < ai_setting.bullet_allowed:
        new_bullet = Bullet(ai_setting, screen, ship)
        bullets.add(new_bullet)
