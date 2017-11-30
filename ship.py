import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, screen, setting, assets):
        """ 初始化飞船并设定其初始位置
            由于需要碰撞检测，继承Sprite类的类需要一个rect对象来定位
        """
        super(Ship, self).__init__()

        self.screen = screen

        self.image = assets.ship

        # 获取外接矩形 Rect对象，获取Rect对象之后可以很方便的获取坐标
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘新的飞船放在底部中央
        self.rect.centerx = self.screen_rect.centerx  # 获取屏幕中心的x坐标
        self.rect.bottom = self.screen_rect.bottom

        # 移动标志
        self.moving_right = False
        self.moving_left = False

        # 移动速度
        self.speed = setting.ship_speed

    def update(self):
        """ 根据移动标志来调整飞船位置 """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx += self.speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.rect.centerx -= self.speed

    def blitme(self):
        """ 在指定位置绘制飞船 """
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """ 让飞船居中 """
        self.center = self.screen_rect.centerx
