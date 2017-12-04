import sys
from bullet import Bullet
import pygame
from alien import Alien
from time import sleep


def check_event(*, ai_setting, screen, ship, bullets, stats, play_button, aliens, sb, assets):
    """" 响应按键和鼠标事件 """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 退出事件
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标按下事件
            if not stats.game_active:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(stats=stats, play_button=play_button, mouse_x=mouse_x, mouse_y=mouse_y,
                                  ai_settings=ai_setting, screen=screen, ship=ship, aliens=aliens, bullets=bullets,
                                  sb=sb, assets=assets)
            else:  # 查看是是不是左键
                mouse_left, mouse_middle, mouse_right = pygame.mouse.get_pressed()
                if mouse_left:
                    fire_bullet(ai_setting=ai_setting, screen=screen, ship=ship, bullets=bullets, assets=assets)

        elif event.type == pygame.MOUSEMOTION:  # 鼠标移动事件
            if stats.game_active:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                ship.rect.centerx = mouse_x

        elif event.type == pygame.KEYDOWN:
            check_event_key_down(event=event, ship=ship, ai_setting=ai_setting, screen=screen, bullets=bullets,
                                 stats=stats, sb=sb, aliens=aliens, assets=assets)
        elif event.type == pygame.KEYUP:
            check_event_key_up(event=event, ship=ship)


def check_play_button(*, stats, play_button, mouse_x, mouse_y, ai_settings, screen, ship, aliens, bullets, sb, assets):
    """ 单击play开始游戏 """
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
        game_start(ai_settings=ai_settings, stats=stats, sb=sb, aliens=aliens, bullets=bullets, screen=screen,
                   ship=ship, assets=assets)


def game_start(*, ai_settings, stats, sb, aliens, bullets, screen, ship, assets):
    """ 游戏开始 """

    # 重置游戏设置
    ai_settings.initialize_dynamic_settings()

    # 隐藏光标
    pygame.mouse.set_visible(False)
    stats.reset_stats()
    stats.game_active = True

    # 重置记分牌图像
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships(assets=assets)

    #  清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()

    # 创建一群外星人并让飞船居中
    create_fleet(ai_settings=ai_settings, screen=screen, ship=ship, aliens=aliens)


def check_event_key_down(*, event, ship, ai_setting, screen, bullets, stats, sb, aliens, assets):
    """ 键盘按下事件 """
    if event.key == pygame.K_RIGHT:  # 键盘 左
        ship.moving_right = True

    elif event.key == pygame.K_q:  # 键盘Q
        sys.exit()

    elif event.key == pygame.K_LEFT:  # 键盘 右
        ship.moving_left = True

    elif event.key == pygame.K_SPACE:  # 键盘 空格
        fire_bullet(ai_setting=ai_setting, screen=screen, ship=ship, bullets=bullets, assets=assets)

    elif event.key == pygame.K_s:  # 键盘 S
        if not stats.game_active:
            game_start(ai_settings=ai_setting, stats=stats, sb=sb, aliens=aliens, bullets=bullets, screen=screen,
                       ship=ship, assets=assets)


def check_event_key_up(*, event, ship):
    """ 键盘弹起事件 """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False

    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(*, screen, ship, bullets, aliens, play_button, stats, sb, assets):
    """ 更新屏幕上的图像，并切换到新屏幕 """

    # screen.fill(ai_settings.bg_color)  # 更新屏幕
    screen.blit(assets.bg, assets.bg.get_rect())
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # 显示得分
    sb.show_score()

    # 如果游戏处于非活动状态
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def update_bullets(*, bullets, aliens, ai_settings, screen, ship, sb, stats):
    """ 更新子弹的位置，并删除已经消失的子弹 """

    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings=ai_settings, screen=screen, ship=ship, aliens=aliens, bullets=bullets,
                                  sb=sb, stats=stats)


def check_bullet_alien_collisions(*, ai_settings, screen, ship, aliens, bullets, sb, stats):
    """ 响应子弹和外星人的碰撞 """

    # 删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(groupa=bullets, groupb=aliens, dokilla=True, dokillb=True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_point
            sb.prep_score()
        check_high_score(stats=stats, sb=sb)

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()

        # 提高一个等级
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings=ai_settings, screen=screen, aliens=aliens, ship=ship)


def fire_bullet(*, ai_setting, screen, ship, bullets, assets):
    """ 如果没有达到限制就发射一颗子弹 """

    if len(bullets) < ai_setting.bullet_allowed:
        new_bullet = Bullet(ai_setting=ai_setting, screen=screen, ship=ship, assets=assets)
        bullets.add(new_bullet)


def get_number_aliens_x(*, ai_settings, alien_width):
    """  计算每一行可以容纳多少个外星人 """
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(*, ai_settings, screen, aliens, alien_number, row_number):
    """ 创建一个外星人并放在当前行 """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(*, ai_settings, screen, aliens, ship):
    """ 创建外星人群 """

    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings=ai_settings, alien_width=alien.rect.width)
    number_rows = get_number_rows(ai_settings=ai_settings, ship_height=ship.rect.height, alien_height=alien.rect.height)

    # 创建一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # 创建一个外星人并加入当前行
            create_alien(ai_settings=ai_settings, screen=screen, aliens=aliens, alien_number=alien_number,
                         row_number=row_number)


def update_aliens(*, ai_settings, aliens, ship, stats, screen, bullets, sb):
    """ 更新所有外星人的位置 """

    # 检测是否有外星人到达了屏幕底端
    check_aliens_bottom(ai_settings=ai_settings, stats=stats, screen=screen, ship=ship, aliens=aliens, bullets=bullets,
                        sb=sb)

    check_fleet_edges(ai_settings=ai_settings, aliens=aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings=ai_settings, stats=stats, screen=screen, ship=ship, aliens=aliens, bullets=bullets, sb=sb)


def check_fleet_edges(*, ai_settings, aliens):
    """ 有外星人到达边缘时采取相应的措施 """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings=ai_settings, aliens=aliens)
            break


def change_fleet_direction(*, ai_settings, aliens):
    """ 将整群外星人下移，并改变它们的方向 """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(*, ai_settings, stats, screen, ship, aliens, bullets, sb):
    """ 响应被外星人撞到的飞船 """
    # 将ships_left减1
    if stats.ships_left > 0:
        stats.ships_left -= 1

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 更新计分牌
        sb.prep_ships()

        # 创建一群新的外星人，并将飞船放到屏幕底部中央
        create_fleet(ai_settings=ai_settings, screen=screen, aliens=aliens, ship=ship)
        ship.center_ship()

        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def get_number_rows(*, ai_settings, ship_height, alien_height):
    """ 计算屏幕可容纳多少行外星人 """
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def check_aliens_bottom(*, ai_settings, stats, screen, ship, aliens, bullets, sb):
    """ 检查是否有外星人到了屏幕底端 """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings=ai_settings, stats=stats, screen=screen, ship=ship, aliens=aliens, bullets=bullets,
                     sb=sb)
            break


def check_high_score(*, stats, sb):
    """ 检查是否诞生了新的最高分 """
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
