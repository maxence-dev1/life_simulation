import pygame
import sys
import draw

pygame.init()

WIDTH, HEIGHT = 1160,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("life simulation")

#Initiation de draw : 
d = draw.Draw(screen, WIDTH, HEIGHT)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                d.print_background()
        
    pygame.display.flip()



pygame.quit()
sys.exit()