import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, screen, setting):
        """ 初始化飞船并设定其初始位置 """
        super(Ship,self).__init__()

        self.screen = screen

        # 加载飞船图像并获取其外形接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘新的飞船放在底部中央
        self.rect.centerx = self.screen_rect.centerx
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
