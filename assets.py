import pygame


class Assets:
    def __init__(self):
        """ 加载资源 """
        bullet_image = pygame.image.load('images/bullet.png').convert_alpha()
        ship_image = pygame.image.load('images/ship.png').convert_alpha()
        alien_image = pygame.image.load('images/alien.png').convert_alpha()
        bg_image = pygame.image.load('images/bg.jpg').convert()

        self.alien = pygame.transform.scale(alien_image, (64, 64))
        self.bullet = pygame.transform.scale(bullet_image, (15, 30))
        self.ship = pygame.transform.scale(ship_image, (64, 64))
        self.bg = pygame.transform.scale(bg_image, (1200, 800))
