import pygame
from settings import Setting
import sys

pygame.init()
ai_settings = Setting()

screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
pygame.display.set_caption("Alien Invasion")

# 加载飞船图像并获取其外形接矩形
alien_image = pygame.image.load('images/bullet.png')
new_bullet_img = pygame.transform.scale(alien_image, (10, 20))
new_bullet_rect = new_bullet_img.get_rect()
screen_rect = screen.get_rect()

new_bullet_rect.centerx = screen_rect.centerx
new_bullet_rect.bottom = screen_rect.bottom
while True:
    screen.fill(ai_settings.bg_color)
    screen.blit(new_bullet_img, new_bullet_rect)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
