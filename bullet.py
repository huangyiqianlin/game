import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """ 一个对飞船子弹速度管理类 """

    def __init__(self, ai_setting, screen, ship):
        """ 在飞船所处的位置创建一个子弹对象 """
        super().__init__()
        self.screen = screen

        # 在（0 0）处创建一个表示子弹的矩形，再设置正确的位置
        # self.rect = pygame.Rect(0, 0, ai_setting.bullet_width, ai_setting.bullet_height)
        # self.rect.centerx = ship.rect.centerx
        # self.rect.top = ship.rect.top

        self.alien_image = pygame.image.load('images/bullet.png')
        self.new_bullet_img = pygame.transform.scale(self.alien_image, (10, 20))

        self.rect = self.new_bullet_img.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)

        # self.color = ai_setting.bullet_color
        self.speed_factor = ai_setting.bullet_speed

    def update(self):
        """ 向上移动子弹 """
        # 更新表示子弹位置的小数值
        self.y -= self.speed_factor
        # 更新表示子弹的rect位置
        self.rect.y = self.y

    def draw_bullet(self):
        """ 在屏幕上绘制子弹 """
        # pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.new_bullet_img, self.rect)
