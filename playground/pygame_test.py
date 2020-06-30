import array
import math

import cairosvg
import pygame

WIDTH = 512
HEIGHT = 512

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))

screen = pygame.display.get_surface()
# image = pygame.image.frombuffer(data.tostring(), (WIDTH, HEIGHT),"ARGB")
# screen.blit(image, (0, 0)) 
screen.fill((50,50,50))
pygame.display.flip() 

while True:
    cmd = input('> ')
    if 'exit' in cmd:
        pygame.quit()
        break

print('Thanks for playing :)')