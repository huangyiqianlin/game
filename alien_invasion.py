import pygame
from settings import Setting
from ship import Ship
from scoreboard import Scoreboard
import game_function as gf
from pygame.sprite import Group
from game_stat import GameStats
from button import Button


def run_game():
    # 初始化一个游戏并创建一个游戏屏幕对象
    pygame.init()
    ai_setting = Setting()

    screen = pygame.display.set_mode((ai_setting.screen_width, ai_setting.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 创建Play按钮
    play_button = Button(ai_setting, screen, "Play")

    # 创建一个用于统计游戏信息的实例，并创建计分牌
    stats = GameStats(ai_settings=ai_setting)
    sb = Scoreboard(ai_settings=ai_setting, screen=screen, stats=stats)

    # 创建一艘飞船
    ship = Ship(screen=screen, setting=ai_setting)

    # 创建一个用于子弹的编组
    bullets = Group()

    # 创建外星人编组
    aliens = Group()
    gf.create_fleet(ai_settings=ai_setting, screen=screen, aliens=aliens, ship=ship)

    # 开始游戏的主循环
    while True:
        # 监视鼠标事件
        gf.check_event(ai_setting=ai_setting, screen=screen, ship=ship, bullets=bullets, stats=stats,
                       play_button=play_button, aliens=aliens)

        if stats.game_active:
            ship.update()
            bullets.update()

            # 删除已经消失的子弹
            gf.update_bullets(bullets=bullets, aliens=aliens, ai_settings=ai_setting, screen=screen, ship=ship, sb=sb,
                              stats=stats)
            gf.update_aliens(ai_setting, aliens, ship, stats, screen, bullets)

        gf.update_screen(ai_settings=ai_setting, screen=screen, ship=ship, bullets=bullets, aliens=aliens,
                         play_button=play_button, stats=stats, sb=sb)
