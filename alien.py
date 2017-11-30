import pygame

from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_settings, screen):
        """ 初始化外星人并设置起始位置 """

        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 添加外星人图像，并设置其rect属性
        image = pygame.image.load('images/alien.png').convert_alpha()

        # 压缩图片大小
        self.image = pygame.transform.scale(image, (64, 64))

        # 获取压缩后图片的外接矩形
        self.rect = self.image.get_rect()

        # 每个外星人的最初位置在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确位置
        self.x = float(self.rect.x)

    def blitme(self):
        """ 在指定位置绘制外星人 """
        self.screen.blit(self.image, self.rect)

    def update(self):
        """ 向右移动外星人 """
        self.x += (self.ai_settings.alien_speed * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
