import pygame
from settings import Setting
from ship import Ship
from alien import Alien
import game_function as gf
from pygame.sprite import Group


def run_game():
    # 初始化一个游戏并创建一个游戏屏幕对象
    pygame.init()
    ai_setting = Setting()

    screen = pygame.display.set_mode((ai_setting.screen_width, ai_setting.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 创建一艘飞船
    ship = Ship(screen, ai_setting)

    # 创建一个用于子弹的编组
    bullets = Group()

    # 创建外星人编组
    aliens = Group()
    gf.create_fleet(ai_setting, screen, aliens)

    # 开始游戏的主循环
    while True:
        # 监视鼠标事件
        gf.check_event(ai_setting, screen, ship, bullets)
        ship.update()
        bullets.update()

        # 删除已经消失的子弹
        gf.update_bullets(bullets, aliens, ai_setting, screen, ship)
        gf.update_aliens(ai_setting, aliens, ship)
        gf.update_screen(ai_setting, screen, ship, bullets, aliens)
