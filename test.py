import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Alien Invasion")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            left, middle, right = pygame.mouse.get_pressed()


    pygame.display.flip()
